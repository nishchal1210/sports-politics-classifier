
"""
b23cm1053_prob4_fixed_search_fallback.py

Wikinews Sports vs Politics classification pipeline (from-scratch features).
This version includes a robust fallback: if a Category:... has no members,
it will use the MediaWiki 'search' API to find candidate pages containing the keyword.

Features:
 - Scrape article titles using MediaWiki API (categorymembers).
 - Fallback to API 'search' when a category returns few/no pages.
 - Extract article text, preprocess, build features from scratch (BoW, TF-IDF, ngrams).
 - Train three classifiers (LogisticRegression, LinearSVC, RandomForest) on each representation.
 - Save results to CSV.

Usage:
    python b23cm1053_prob4_fixed_search_fallback.py --articles-per-class 200
"""

import argparse
import requests
import time
import math
import re
from urllib.parse import quote
from collections import Counter, defaultdict
from typing import List
import numpy as np
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# ---------------------------
# Config / constants
# ---------------------------
API_ENDPOINT = "https://en.wikinews.org/w/api.php"
BASE_PAGE_URL = "https://en.wikinews.org/wiki/"
HEADERS = {"User-Agent": "Wikinews-Scraper/1.0 (contact: you@example.com)"}

# ---------------------------
# MediaWiki helpers
# ---------------------------
def fetch_category_members(category_title: str, max_items: int = 200, delay: float = 0.3) -> List[str]:
    """
    Fetch page titles from a category using MediaWiki API.
    Returns list of page titles (strings).
    """
    titles = []
    session = requests.Session()
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category_title,   # e.g. "Category:Sports"
        "cmnamespace": 0,            # articles only
        "cmlimit": "max",
        "format": "json"
    }
    cont = {}
    pbar = tqdm(total=max_items, desc=f"Listing {category_title}", unit="titles")
    try:
        while True:
            if cont:
                params.update(cont)
            r = session.get(API_ENDPOINT, params=params, headers=HEADERS, timeout=20)
            r.raise_for_status()
            data = r.json()
            cms = data.get("query", {}).get("categorymembers", [])
            for item in cms:
                title = item.get("title")
                if title and len(titles) < max_items:
                    titles.append(title)
                    pbar.update(1)
                if len(titles) >= max_items:
                    break
            if "continue" in data and len(titles) < max_items:
                cont = data["continue"]
            else:
                break
            time.sleep(delay)
    except Exception as e:
        # network or API hiccup; return whatever we have
        # print a small warning
        print(f"Warning: categorymembers API issue: {e}")
    pbar.close()
    return titles[:max_items]


def search_wikinews(query: str, max_items: int = 200, delay: float = 0.3) -> List[str]:
    """
    Use MediaWiki 'search' API to return pages that match the query.
    Returns list of page titles.
    """
    titles = []
    session = requests.Session()
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": 0,
        "srlimit": "max",
        "format": "json"
    }
    cont = {}
    pbar = tqdm(total=max_items, desc=f"Search '{query}'", unit="titles")
    try:
        while True:
            if cont:
                params.update(cont)
            r = session.get(API_ENDPOINT, params=params, headers=HEADERS, timeout=20)
            r.raise_for_status()
            data = r.json()
            results = data.get("query", {}).get("search", [])
            for item in results:
                title = item.get("title")
                if title and len(titles) < max_items:
                    titles.append(title)
                    pbar.update(1)
                if len(titles) >= max_items:
                    break
            if "continue" in data and len(titles) < max_items:
                cont = data["continue"]
            else:
                break
            time.sleep(delay)
    except Exception as e:
        print(f"Warning: search API issue: {e}")
    pbar.close()
    return titles[:max_items]

# ---------------------------
# Title -> URL and fetch article
# ---------------------------
def title_to_url(title: str) -> str:
    return BASE_PAGE_URL + quote(title.replace(" ", "_"), safe="/:_")

def extract_article_text(url: str, delay: float = 0.3) -> str:
    """
    Download the article page and extract the text inside the main content.
    Returns concatenated paragraph text or empty string on failure.
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.find("div", {"class": "mw-parser-output"})
        if not content:
            content = soup.find("div", {"id": "mw-content-text"})
        if not content:
            return ""
        # remove tables and side boxes that often appear
        for bad in content.find_all(["table", "style", "script", "aside"]):
            bad.decompose()
        paragraphs = content.find_all("p")
        parts = []
        for p in paragraphs:
            t = p.get_text(separator=" ", strip=True)
            if t and len(t) > 30:
                parts.append(t)
        time.sleep(delay)
        return " ".join(parts).strip()
    except Exception:
        return ""

# ---------------------------
# Preprocessing & tokenization
# ---------------------------
def preprocess(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"\[[0-9]+\]", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str):
    return text.split() if text else []

def make_ngrams(tokens, n):
    if n == 1:
        return tokens[:]
    if len(tokens) < n:
        return []
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

# ---------------------------
# Feature builders (from scratch)
# ---------------------------
def build_vocabulary_and_df(docs_tokens, min_df=1, max_df_ratio=1.0):
    N = len(docs_tokens)
    df = defaultdict(int)
    for tokens in docs_tokens:
        seen = set(tokens)
        for t in seen:
            df[t] += 1
    vocab = {}
    idx = 0
    for t, freq in df.items():
        if freq >= min_df and freq <= max_df_ratio * N:
            vocab[t] = idx
            idx += 1
    return vocab, df

def build_bow_matrix(docs_tokens, vocab):
    D = len(docs_tokens)
    V = len(vocab)
    X = np.zeros((D, V), dtype=float)
    for i, tokens in enumerate(docs_tokens):
        cnt = Counter(tokens)
        for t, c in cnt.items():
            if t in vocab:
                X[i, vocab[t]] = c
    return X

def compute_idf(vocab, docs_tokens):
    N = len(docs_tokens)
    df = defaultdict(int)
    for tokens in docs_tokens:
        seen = set(tokens)
        for t in seen:
            df[t] += 1
    idf = {}
    for t in vocab:
        idf[t] = math.log((N + 1) / (df.get(t, 0) + 1)) + 1.0
    return idf

def build_tfidf_matrix(docs_tokens, vocab, idf_map):
    D = len(docs_tokens)
    V = len(vocab)
    X = np.zeros((D, V), dtype=float)
    for i, tokens in enumerate(docs_tokens):
        cnt = Counter(tokens)
        total = max(1, len(tokens))
        for t, c in cnt.items():
            if t in vocab:
                tf = c / total
                X[i, vocab[t]] = tf * idf_map.get(t, 1.0)
    return X

# ---------------------------
# Main pipeline
# ---------------------------
def pipeline(articles_per_class=200, min_words=50, test_size=0.2, delay=0.3):
    print("Step 1: fetch category titles for Sports and Politics (API).")
    sports_titles = fetch_category_members("Category:Sports", max_items=articles_per_class, delay=delay)
    politics_titles = fetch_category_members("Category:Politics", max_items=articles_per_class, delay=delay)

    print(f"Found titles -> Sports: {len(sports_titles)}, Politics: {len(politics_titles)}")

    # If politics_titles is empty, fallback to search API
    if len(politics_titles) == 0:
        print("No category members found for Politics — falling back to search('politics').")
        politics_titles = search_wikinews("politics", max_items=articles_per_class, delay=delay)
        print(f"Search returned {len(politics_titles)} titles for 'politics'.")

    # second fallback: if still empty, try "Category:Political topics" or "Category:Politics_by_country"
    if len(politics_titles) == 0:
        print("Second fallback: trying alternative category names.")
        alternatives = ["Category:Political topics", "Category:Politics by country", "Category:Politics of the United States"]
        for alt in alternatives:
            alt_titles = fetch_category_members(alt, max_items=articles_per_class, delay=delay)
            if len(alt_titles) > 0:
                politics_titles = alt_titles
                print(f"Found {len(alt_titles)} titles in {alt}")
                break

    print(f"Final counts -> Sports titles: {len(sports_titles)}, Politics titles: {len(politics_titles)}")

    # require at least 2 titles per class
    if len(sports_titles) < 2 or len(politics_titles) < 2:
        raise SystemExit("Not enough page titles for both classes. Try increasing network reliability or reducing articles-per-class.")

    # Step 2: download article text
    def fetch_articles_from_titles(titles, label_name):
        texts = []
        for title in tqdm(titles, desc=f"Downloading {label_name}"):
            url = title_to_url(title)
            txt = extract_article_text(url, delay=delay)
            txt = preprocess(txt)
            if txt and len(txt.split()) >= min_words:
                texts.append(txt)
        return texts

    sports_texts = fetch_articles_from_titles(sports_titles, "Sports")
    politics_texts = fetch_articles_from_titles(politics_titles, "Politics")

    print(f"Downloaded articles -> Sports: {len(sports_texts)}, Politics: {len(politics_texts)}")

    # if politics empty, retry with smaller min_words
    if len(politics_texts) == 0:
        print("Retrying politics fetch with min_words=30...")
        politics_texts = []
        for title in tqdm(politics_titles, desc="Downloading politics retry"):
            url = title_to_url(title)
            txt = extract_article_text(url, delay=delay)
            txt = preprocess(txt)
            if txt and len(txt.split()) >= 30:
                politics_texts.append(txt)
        print(f"After retry politics count: {len(politics_texts)}")

    if len(politics_texts) == 0 or len(sports_texts) == 0:
        raise SystemExit("Failed to fetch enough article text for both classes. Try different parameters.")

    # balance dataset
    n_per_class = min(len(sports_texts), len(politics_texts), articles_per_class)
    print(f"Using {n_per_class} articles per class (balanced).")
    sports_texts = sports_texts[:n_per_class]
    politics_texts = politics_texts[:n_per_class]

    texts = sports_texts + politics_texts
    labels = [0] * n_per_class + [1] * n_per_class  # 0=sports,1=politics

    # tokenize unigrams and ngrams
    token_docs_unigram = [tokenize(t) for t in texts]
    token_docs_ngram = []
    for tokens in token_docs_unigram:
        grams = tokens[:]
        grams += make_ngrams(tokens, 2)
        grams += make_ngrams(tokens, 3)
        token_docs_ngram.append(grams)

    # Build vocabularies & feature matrices
    print("Building unigram vocabulary and feature matrices (from scratch)...")
    vocab_uni, df_uni = build_vocabulary_and_df(token_docs_unigram := token_docs_unigram)
    X_bow = build_bow_matrix(token_docs_unigram, vocab_uni)
    idf_uni = compute_idf(vocab_uni, token_docs_unigram)
    X_tfidf = build_tfidf_matrix(token_docs_unigram, vocab_uni, idf_uni)

    print("Building ngram (1-3) vocabulary and TF-IDF...")
    vocab_ng, df_ng = build_vocabulary_and_df(token_docs_ngram := token_docs_ngram)
    idf_ng = compute_idf(vocab_ng, token_docs_ngram)
    X_ng = build_tfidf_matrix(token_docs_ngram, vocab_ng, idf_ng)

    # Evaluate classifiers on each feature set
    features = {
        "bow_unigram": X_bow,
        "tfidf_unigram": X_tfidf,
        "tfidf_1_3gram": X_ng
    }
    y = np.array(labels)

    results = []
    for feat_name, X in features.items():
        print(f"\nEvaluating feature: {feat_name} shape={X.shape}")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y, random_state=42)
        classifiers = {
            "LogisticRegression": LogisticRegression(max_iter=2000),
            "LinearSVC": LinearSVC(max_iter=5000),
            "RandomForest": RandomForestClassifier(n_estimators=200)
        }
        for clf_name, clf in classifiers.items():
            print(f"Training {clf_name} on {feat_name} ...")
            clf.fit(X_train, y_train)
            ypred = clf.predict(X_test)
            acc = accuracy_score(y_test, ypred)
            prec, rec, f1, _ = precision_recall_fscore_support(y_test, ypred, average="macro", zero_division=0)
            print(f" -> acc={acc:.4f} f1={f1:.4f}")
            results.append({
                "feature": feat_name,
                "classifier": clf_name,
                "n_train": X_train.shape[0],
                "n_test": X_test.shape[0],
                "n_features": X.shape[1],
                "accuracy": float(acc),
                "precision_macro": float(prec),
                "recall_macro": float(rec),
                "f1_macro": float(f1)
            })

    df_results = pd.DataFrame(results)
    outdir = "outputs"
    import os
    os.makedirs(outdir, exist_ok=True)
    df_results.to_csv(os.path.join(outdir, "results_summary_wikinews.csv"), index=False)
    print("\nSaved results to outputs/results_summary_wikinews.csv")
    print(df_results)
    return df_results

# ---------------------------
# Small helpers (wrapped to avoid repetition)
# ---------------------------
from collections import defaultdict
def build_vocabulary_and_df(docs_tokens):
    df = defaultdict(int)
    for tokens in docs_tokens:
        seen = set(tokens)
        for t in seen:
            df[t] += 1
    vocab = {}
    idx = 0
    for t, freq in df.items():
        vocab[t] = idx
        idx += 1
    return vocab, df

def build_bow_matrix(docs_tokens, vocab):
    D = len(docs_tokens)
    V = len(vocab)
    X = np.zeros((D, V), dtype=float)
    for i, tokens in enumerate(docs_tokens):
        cnt = Counter(tokens)
        for t, c in cnt.items():
            if t in vocab:
                X[i, vocab[t]] = c
    return X

def compute_idf(vocab, docs_tokens):
    N = len(docs_tokens)
    df = defaultdict(int)
    for tokens in docs_tokens:
        seen = set(tokens)
        for t in seen:
            df[t] += 1
    idf_map = {}
    for t in vocab:
        idf_map[t] = math.log((N + 1) / (df.get(t, 0) + 1)) + 1.0
    return idf_map

def build_tfidf_matrix(docs_tokens, vocab, idf_map):
    D = len(docs_tokens)
    V = len(vocab)
    X = np.zeros((D, V), dtype=float)
    for i, tokens in enumerate(docs_tokens):
        cnt = Counter(tokens)
        total = max(1, len(tokens))
        for t, c in cnt.items():
            if t in vocab:
                tf = c / total
                X[i, vocab[t]] = tf * idf_map.get(t, 1.0)
    return X

# ---------------------------
# Entry point
# ---------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--articles-per-class", type=int, default=200)
    parser.add_argument("--min-words", type=int, default=50)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--delay", type=float, default=0.3)
    args = parser.parse_args()

    # Run pipeline
    df_out = pipeline(articles_per_class=args.articles_per_class, min_words=args.min_words, test_size=args.test_size, delay=args.delay)
