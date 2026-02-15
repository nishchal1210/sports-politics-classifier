
"""
B23CM1053_prob4.py

Wikinews Sports vs Politics classification pipeline (from-scratch features).
Added interactive step: after training & evaluation, user can choose a
feature representation and a trained model, then provide a text file
(path) to classify using the selected model+feature.


"""

import argparse
import requests
import time
import math
import re
from urllib.parse import quote
from collections import Counter, defaultdict
from typing import List, Tuple
import numpy as np
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
import os
import sys

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
    titles = []
    session = requests.Session()
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category_title,
        "cmnamespace": 0,
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
        print(f"Warning: categorymembers API issue: {e}")
    pbar.close()
    return titles[:max_items]


def search_wikinews(query: str, max_items: int = 200, delay: float = 0.3) -> List[str]:
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
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.find("div", {"class": "mw-parser-output"})
        if not content:
            content = soup.find("div", {"id": "mw-content-text"})
        if not content:
            return ""
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
# Utility: convert decision output to pseudo-probabilities
# ---------------------------
def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def softmax(arr):
    ex = np.exp(arr - np.max(arr))
    return ex / ex.sum()

def get_prediction_and_confidence(model, X_single: np.ndarray) -> Tuple[int, float]:
    """
    Return (predicted_label, confidence_score_in_[0,1]).
    Tries predict_proba(); if not available, uses decision_function().
    """
    # ensure 2D array
    if X_single.ndim == 1:
        X_single = X_single.reshape(1, -1)

    try:
        probs = model.predict_proba(X_single)
        probs = np.asarray(probs).ravel()
        pred = int(np.argmax(probs))
        conf = float(np.max(probs))
        return pred, conf
    except Exception:
        # fallback to decision_function
        try:
            df = model.decision_function(X_single)
            df = np.asarray(df)
            # binary case: df is shape (1,) -> map with sigmoid to [0,1]
            if df.ndim == 1:
                score = float(df.ravel()[0])
                prob_pos = sigmoid(score)
                probs_arr = np.array([1.0 - prob_pos, prob_pos])
                pred = int(np.argmax(probs_arr))
                conf = float(np.max(probs_arr))
                return pred, conf
            else:
                # multiclass: softmax over df vector
                arr = df.ravel()
                probs_arr = softmax(arr)
                pred = int(np.argmax(probs_arr))
                conf = float(np.max(probs_arr))
                return pred, conf
        except Exception:
            # last resort: predict and set confidence 1.0
            pred = int(model.predict(X_single).ravel()[0])
            return pred, 1.0

# ---------------------------
# Main pipeline (returns trained models and feature artifacts)
# ---------------------------
def pipeline(articles_per_class=200, min_words=50, test_size=0.2, delay=0.3):
    print("Step 1: fetch category titles for Sports and Politics (API).")
    sports_titles = fetch_category_members("Category:Sports", max_items=articles_per_class, delay=delay)
    politics_titles = fetch_category_members("Category:Politics", max_items=articles_per_class, delay=delay)

    print(f"Found titles -> Sports: {len(sports_titles)}, Politics: {len(politics_titles)}")

    if len(politics_titles) == 0:
        print("No category members found for Politics — falling back to search('politics').")
        politics_titles = search_wikinews("politics", max_items=articles_per_class, delay=delay)
        print(f"Search returned {len(politics_titles)} titles for 'politics'.")

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

    if len(sports_titles) < 2 or len(politics_titles) < 2:
        raise SystemExit("Not enough page titles for both classes. Try increasing network reliability or reducing articles-per-class.")

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

    n_per_class = min(len(sports_texts), len(politics_texts), articles_per_class)
    print(f"Using {n_per_class} articles per class (balanced).")
    sports_texts = sports_texts[:n_per_class]
    politics_texts = politics_texts[:n_per_class]

    texts = sports_texts + politics_texts
    labels = [0] * n_per_class + [1] * n_per_class  # 0=sports,1=politics

    token_docs_unigram = [tokenize(t) for t in texts]
    token_docs_ngram = []
    for tokens in token_docs_unigram:
        grams = tokens[:]
        grams += make_ngrams(tokens, 2)
        grams += make_ngrams(tokens, 3)
        token_docs_ngram.append(grams)

    # Build vocabularies & feature matrices
    print("Building unigram vocabulary and feature matrices (from scratch)...")
    vocab_uni, df_uni = build_vocabulary_and_df(token_docs_unigram)
    X_bow = build_bow_matrix(token_docs_unigram, vocab_uni)
    idf_uni = compute_idf(vocab_uni, token_docs_unigram)
    X_tfidf = build_tfidf_matrix(token_docs_unigram, vocab_uni, idf_uni)

    print("Building ngram (1-3) vocabulary and TF-IDF...")
    vocab_ng, df_ng = build_vocabulary_and_df(token_docs_ngram)
    idf_ng = compute_idf(vocab_ng, token_docs_ngram)
    X_ng = build_tfidf_matrix(token_docs_ngram, vocab_ng, idf_ng)

    features = {
        "bow_unigram": X_bow,
        "tfidf_unigram": X_tfidf,
        "tfidf_1_3gram": X_ng
    }
    y = np.array(labels)

    results = []
    trained_models = {}  # store trained models keyed by (feature_name, classifier_name)
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
            # store trained model for later interactive use
            trained_models[(feat_name, clf_name)] = clf
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
    os.makedirs(outdir, exist_ok=True)
    df_results.to_csv(os.path.join(outdir, "results_summary_wikinews.csv"), index=False)
    print("\nSaved results to outputs/results_summary_wikinews.csv")
    print(df_results)

    # Return artifacts required for interactive classification
    artifacts = {
        "trained_models": trained_models,
        "vocab_uni": vocab_uni,
        "idf_uni": idf_uni,
        "vocab_ng": vocab_ng,
        "idf_ng": idf_ng
    }
    return df_results, artifacts

# ---------------------------
# Vectorize a single document consistently with training
# ---------------------------
def vectorize_single_document(text: str, feature_name: str, vocab_uni: dict, idf_uni: dict, vocab_ng: dict, idf_ng: dict) -> np.ndarray:
    text_p = preprocess(text)
    tokens = tokenize(text_p)
    if feature_name == "bow_unigram":
        V = len(vocab_uni)
        vec = np.zeros((V,), dtype=float)
        cnt = Counter(tokens)
        for t, c in cnt.items():
            if t in vocab_uni:
                vec[vocab_uni[t]] = c
        return vec
    elif feature_name == "tfidf_unigram":
        V = len(vocab_uni)
        vec = np.zeros((V,), dtype=float)
        cnt = Counter(tokens)
        total = max(1, len(tokens))
        for t, c in cnt.items():
            if t in vocab_uni:
                tf = c / total
                vec[vocab_uni[t]] = tf * idf_uni.get(t, 1.0)
        return vec
    elif feature_name == "tfidf_1_3gram":
        grams = tokens[:]
        grams += make_ngrams(tokens, 2)
        grams += make_ngrams(tokens, 3)
        V = len(vocab_ng)
        vec = np.zeros((V,), dtype=float)
        cnt = Counter(grams)
        total = max(1, len(grams))
        for t, c in cnt.items():
            if t in vocab_ng:
                tf = c / total
                vec[vocab_ng[t]] = tf * idf_ng.get(t, 1.0)
        return vec
    else:
        raise ValueError(f"Unknown feature: {feature_name}")

# ---------------------------
# Interactive selection & classification
# ---------------------------
def interactive_classify(artifacts: dict):
    trained_models = artifacts["trained_models"]
    vocab_uni = artifacts["vocab_uni"]
    idf_uni = artifacts["idf_uni"]
    vocab_ng = artifacts["vocab_ng"]
    idf_ng = artifacts["idf_ng"]

    feature_choices = ["bow_unigram", "tfidf_unigram", "tfidf_1_3gram"]
    model_choices = ["LogisticRegression", "LinearSVC", "RandomForest"]
    label_map = {0: "Sports", 1: "Politics"}

    print("\nInteractive classification mode.")
    print("Available feature representations:")
    for i, f in enumerate(feature_choices, 1):
        print(f"  {i}. {f}")
    feat_sel = input("Select feature (enter number, e.g. 1): ").strip()
    try:
        feat_idx = int(feat_sel) - 1
        feature_name = feature_choices[feat_idx]
    except Exception:
        print("Invalid selection. Exiting interactive mode.")
        return

    print("\nAvailable trained models:")
    for i, m in enumerate(model_choices, 1):
        print(f"  {i}. {m}")
    model_sel = input("Select model (enter number, e.g. 2): ").strip()
    try:
        model_idx = int(model_sel) - 1
        model_name = model_choices[model_idx]
    except Exception:
        print("Invalid selection. Exiting interactive mode.")
        return

    # check that selected model was trained for the selected feature
    key = (feature_name, model_name)
    if key not in trained_models:
        print(f"Selected model {model_name} was not trained for feature {feature_name}. Available keys:")
        print(list(trained_models.keys()))
        return

    model = trained_models[key]
    print(f"\nSelected: Feature='{feature_name}'  Model='{model_name}'")

    # ask for text file path
    while True:
        path = input("\nEnter path to a text file to classify (or type 'quit' to exit): ").strip()
        if path.lower() in ("quit", "exit", "q"):
            print("Exiting interactive classification.")
            break
        if not os.path.isfile(path):
            print("File not found. Try again.")
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print("Failed to read file:", e)
            continue

        vec = vectorize_single_document(text, feature_name, vocab_uni, idf_uni, vocab_ng, idf_ng)
        pred, conf = get_prediction_and_confidence(model, vec)
        print(f"\nPrediction: {label_map.get(pred, str(pred))}  (confidence: {conf:.3f})")
        # show top-k words coverage info
        tokens = tokenize(preprocess(text))
        covered = sum(1 for t in tokens if (t in vocab_uni if feature_name != "tfidf_1_3gram" else t in vocab_ng))
        total = max(1, len(tokens))
        print(f"Vocabulary coverage in this doc: {covered}/{total} tokens ({covered/total:.2%})")
        # loop to allow next file

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

    # Run pipeline (train & evaluate all 9 combinations)
    df_out, artifacts = pipeline(articles_per_class=args.articles_per_class, min_words=args.min_words, test_size=args.test_size, delay=args.delay)

    # After printing results, enter interactive classification mode
    interactive_classify(artifacts)
