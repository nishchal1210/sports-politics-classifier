# ⚡ Sports or Politics Classifier

> *A binary text classifier for distinguishing sports from politics articles — built entirely from scratch in NumPy.*

![Python](https://img.shields.io/badge/Python-3.8+-00d9a3?style=flat-square&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-From_Scratch-e85d4a?style=flat-square&logo=numpy&logoColor=white)
![Accuracy](https://img.shields.io/badge/Accuracy-100%25-f5c842?style=flat-square)
![Dataset](https://img.shields.io/badge/Dataset-Wikinews-6b7a99?style=flat-square)

---

## 📊 Results Matrix

**9 Experiments** · 3 Feature Representations × 3 Classifiers · Test Set = 80 articles (40 Sports + 40 Politics)

|  | **Logistic Regression** | **LinearSVC** | **Random Forest** |
|---|:---:|:---:|:---:|
| **BoW (Unigram)** | ✅ 98.75% | ✅ **100.00%** | 97.50% |
| | F1 = 0.9875 | F1 = 1.0000 | F1 = 0.9750 |
| **TF-IDF (Unigram)** | 97.50% | ✅ 98.75% | ✅ 98.75% |
| | F1 = 0.9750 | F1 = 0.9875 | F1 = 0.9875 |
| **TF-IDF (1–3-gram)** | 95.00% | 95.00% | 97.50% |
| | F1 = 0.9499 | F1 = 0.9499 | F1 = 0.9750 |

### 🏆 Winner

**LinearSVC on BoW Unigram** achieves **perfect 100% accuracy**  
*(C=1.0, max_iter=5000, default sklearn settings)*

**Key Insight:** Raw token counts (BoW) with LinearSVC achieve perfect classification. The linear decision boundary in the high-dimensional sparse BoW space perfectly separates the two classes, demonstrating that Sports and Politics articles have completely distinct vocabularies on this dataset.

---

## 🚀 Setup & Usage

### Prerequisites

```bash
pip install numpy requests tqdm scikit-learn beautifulsoup4
```

**No external NLP libraries.** All feature engineering (BoW, TF-IDF, n-grams) is implemented from scratch in pure NumPy.

### Running the Pipeline

```bash
python B23CM1053_prob4.py \
  --articles-per-class  200   # articles to fetch per class   (default: 200)
  --min-words           50    # discard shorter articles      (default: 50)
  --test-size           0.2   # fraction held out for test    (default: 0.2)
  --delay               0.3   # seconds between API requests  (default: 0.3)
```
---

# 🖥️ Interactive Classification Mode

After training all 9 configurations and printing the evaluation results, the script automatically enters **interactive mode**.

This allows you to:

- Select a feature representation
- Select a trained classifier
- Provide a `.txt` document from your local directory
- Obtain a prediction (Sports / Politics) with confidence score

---

## 🔄 How It Works

After results are displayed, you will see:

```terminal
Interactive classification mode.

Available feature representations:
  1. bow_unigram
  2. tfidf_unigram
  3. tfidf_1_3gram

Select feature (enter number, e.g. 1):

Available trained models:
  1. LogisticRegression
  2. LinearSVC
  3. RandomForest

Select model (enter number, e.g. 2):

Enter path to a text file to classify (or type 'quit' to exit):

### Expected Terminal Output

```terminal
Step 1: fetch category titles for Sports and Politics (API).
Listing Category:Sports: 100%|████████████| 200/200 [00:01<00:00, 198.67titles/s]
Listing Category:Politics:   0%|          |   0/200 [00:00<?, ?titles/s]
Found titles -> Sports: 200, Politics: 0
No category members found for Politics — falling back to search('politics').
Search 'politics': 100%|████████████████| 200/200 [00:01<00:00, 115.90titles/s]
Search returned 200 titles for 'politics'.
Final counts -> Sports titles: 200, Politics titles: 200
Downloading Sports:   100%|████████████| 200/200 [02:27<00:00,  1.36it/s]
Downloading Politics: 100%|████████████| 200/200 [02:29<00:00,  1.34it/s]
Downloaded articles -> Sports: 198, Politics: 199
Using 198 articles per class (balanced).
Building unigram vocabulary and feature matrices (from scratch)...
Building ngram (1-3) vocabulary and TF-IDF...

Evaluating feature: bow_unigram   shape=(396, 11687)
 LogisticRegression → acc=0.9875  f1=0.9875
 LinearSVC          → acc=1.0000  f1=1.0000
 RandomForest       → acc=0.9750  f1=0.9750

Evaluating feature: tfidf_unigram shape=(396, 11687)
 LogisticRegression → acc=0.9750  f1=0.9750
 LinearSVC          → acc=0.9875  f1=0.9875
 RandomForest       → acc=0.9875  f1=0.9875

Evaluating feature: tfidf_1_3gram shape=(396, 178465)
 LogisticRegression → acc=0.9500  f1=0.9499
 LinearSVC          → acc=0.9500  f1=0.9499
 RandomForest       → acc=0.9750  f1=0.9750

Saved results to outputs/results_summary_wikinews.csv
```

⏱️ **Total runtime:** ~7–8 minutes (network-bound)

---

## 🧮 Feature Representations

All three representations are built **entirely from scratch** in pure NumPy — no `CountVectorizer` or `TfidfVectorizer`.

### Feature 01 · **Bag-of-Words**
**Vocabulary:** 11,687 tokens  
**Description:** Raw token counts. `X[i][j] = count(vⱼ, dᵢ)`. No normalisation. Achieves perfect 100% accuracy with LinearSVC — demonstrates that absolute word frequencies are maximally discriminative for this task.

### Feature 02 · **TF-IDF Unigram**
**Vocabulary:** 11,687 tokens  
**Description:** TF × smooth IDF. Weights discriminative words higher, suppresses common noise. Same vocab as BoW — different weighting scheme. Achieves 98.75% with LinearSVC and Random Forest.

### Feature 03 · **TF-IDF 1–3-gram**
**Vocabulary:** 178,465 tokens  
**Description:** Unigrams + bigrams + trigrams. Captures "won the match", "prime minister of". ~15× larger vocabulary than unigram alone. Achieves 97.50% with Random Forest.

### IDF Formula (implemented from scratch)

```python
# compute_idf() — pure Python/NumPy, no sklearn
def compute_idf(vocab, docs_tokens):
    N = len(docs_tokens)
    df = defaultdict(int)
    for tokens in docs_tokens:
        for t in set(tokens):
            df[t] += 1
    return {t: math.log((N+1) / (df.get(t,0)+1)) + 1.0
            for t in vocab}    # smooth IDF: ln((N+1)/(df+1)) + 1
```

---

## 💡 Key Findings

### 🎯 LinearSVC on raw BoW achieves perfect separation (100%)
The maximum-margin hyperplane in the 11,687-dimensional BoW space achieves zero test error. Sports and Politics articles are linearly separable without requiring TF-IDF normalisation or n-gram features.

### 📦 TF-IDF normalisation slightly reduces performance
Logistic Regression drops from 98.75% (BoW) to 97.50% (TF-IDF unigram). For this task, raw count magnitudes carry more signal than normalised weights — "football" appearing 20× is more discriminative than its TF-IDF score.

### 📉 N-grams provide minimal benefit
Adding bigrams and trigrams increases vocabulary 15× (11,687 → 178,465) but does not improve accuracy. Best n-gram result is 97.50% (Random Forest), worse than the 100% achieved with simple unigrams. The explosion of correlated features adds noise without capturing additional discriminative patterns.

### 🌲 Random Forest is robust but not optimal
Random Forest achieves consistent 97.50–98.75% across all features but never reaches 100%. Its ensemble averaging smooths out predictions, preventing perfect separation that LinearSVC's hard margin achieves.

### ✅ Task is maximally separable
The 100% accuracy confirms that Sports and Politics have zero vocabulary overlap on discriminative features. Team names, scores, match results vs. government terms, policy language, party names create perfect linear separability.

---

## ⚠️ Limitations

### 01 · Label Noise
**Search-API Politics labels**  
`Category:Politics` was empty. Search-based titles may include articles that only mention politics tangentially, introducing label noise.

### 02 · Scale
**Small test set (80 articles)**  
One misclassification = 1.25% accuracy change. High variance — cross-validation would give more reliable estimates.

### 03 · Preprocessing
**No stop-word removal or stemming**  
Function words inflate vocabulary without discriminative signal. Porter stemming would reduce sparsity and potentially improve generalisation.

### 04 · Memory
**Dense 178K-feature matrix ≈ 563 MB**  
Dense NumPy arrays don't scale. `scipy.sparse.csr_matrix` would be needed for larger corpora or production systems.

### 05 · Vocabulary
**No min-df threshold**  
Single-occurrence tokens (hapax legomena) add noise to the vocabulary without generalisation benefit. A min-df filter would reduce dimensionality.

### 06 · Domain
**Wikinews prose style only**  
Short, neutral encyclopaedic articles. Likely degrades on social media, blogs, or other writing styles due to vocabulary shift and informal language.

### 07 · Overfitting Risk
**Perfect test accuracy may not generalise**  
100% on 80 articles could indicate overfitting to this specific test set. K-fold cross-validation would verify robustness.

---

## 📁 Project Structure

```
sports-politics-classifier/
│
├── B23CM1053_prob4.py               ← main pipeline
│
├── outputs/
│   └── results_summary_wikinews.csv  ← all 9 experiment results
│
├── B23CM1053_prob4_report.pdf        ← full 12-page LaTeX report
│
└── README.md                         ← you are here
```

---

## 📈 Full Results Table

| Feature | Classifier | Train | Test | Features | Accuracy | Precision | Recall | F1 |
|---------|-----------|-------|------|----------|----------|-----------|--------|-----|
| BoW Unigram | LogisticRegression | 316 | 80 | 11,687 | 0.9875 | 0.9878 | 0.9875 | 0.9875 |
| BoW Unigram | LinearSVC | 316 | 80 | 11,687 | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| BoW Unigram | RandomForest | 316 | 80 | 11,687 | 0.9750 | 0.9762 | 0.9750 | 0.9750 |
| TF-IDF Unigram | LogisticRegression | 316 | 80 | 11,687 | 0.9750 | 0.9762 | 0.9750 | 0.9750 |
| TF-IDF Unigram | LinearSVC | 316 | 80 | 11,687 | 0.9875 | 0.9878 | 0.9875 | 0.9875 |
| TF-IDF Unigram | RandomForest | 316 | 80 | 11,687 | 0.9875 | 0.9878 | 0.9875 | 0.9875 |
| TF-IDF 1–3-gram | LogisticRegression | 316 | 80 | 178,465 | 0.9500 | 0.9545 | 0.9500 | 0.9499 |
| TF-IDF 1–3-gram | LinearSVC | 316 | 80 | 178,465 | 0.9500 | 0.9545 | 0.9500 | 0.9499 |
| TF-IDF 1–3-gram | RandomForest | 316 | 80 | 178,465 | 0.9750 | 0.9762 | 0.9750 | 0.9750 |

---

<div align="center">

**B23CM1053**  
*NLP Assignment · Problem 4 · Binary Text Classification on Wikinews*

</div>
