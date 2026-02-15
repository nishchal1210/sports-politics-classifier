# ⚡ Sports or Politics Classifier

> *A binary text classifier for distinguishing sports from politics articles — built entirely from scratch in NumPy.*

![Python](https://img.shields.io/badge/Python-3.8+-00d9a3?style=flat-square&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-From_Scratch-e85d4a?style=flat-square&logo=numpy&logoColor=white)
![Accuracy](https://img.shields.io/badge/Accuracy-98.75%25-f5c842?style=flat-square)
![Dataset](https://img.shields.io/badge/Dataset-Wikinews-6b7a99?style=flat-square)

---

## 📊 Results Matrix

**9 Experiments** · 3 Feature Representations × 3 Classifiers · Test Set = 80 articles (40 Sports + 40 Politics)

|  | **Logistic Regression** | **LinearSVC** | **Random Forest** |
|---|:---:|:---:|:---:|
| **BoW (Unigram)** | ✅ **98.75%** | ✅ **98.75%** | ✅ **98.75%** |
| | F1 = 0.9875 | F1 = 0.9875 | F1 = 0.9875 |
| **TF-IDF (Unigram)** | 95.00% | ✅ **98.75%** | ✅ **98.75%** |
| | F1 = 0.9500 | F1 = 0.9875 | F1 = 0.9875 |
| **TF-IDF (1–3-gram)** | 95.00% | 93.75% | ✅ **98.75%** |
| | F1 = 0.9500 | F1 = 0.9380 | F1 = 0.9875 |

### 🏆 Winner

**Random Forest** achieves **98.75%** accuracy across **all three feature sets**  
*(200 estimators, max_depth=None, default sklearn settings)*

**Key Insight:** Raw token counts (BoW) perform as well as or better than TF-IDF for LogisticRegression on this task. The high discriminative power of absolute word frequencies ("football" appears 20× in sports articles) outweighs the benefits of TF-IDF normalisation.

---

## 🚀 Setup & Usage

### Prerequisites

```bash
pip install numpy requests tqdm scikit-learn
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

### Expected Terminal Output

```terminal
Step 1: fetch category titles for Sports and Politics (API).
Listing Category:Sports: 100%|████████████| 200/200 [00:01<00:00, 186.22titles/s]
Listing Category:Politics:   0%|          |   0/200 [00:00<?, ?titles/s]
Found titles -> Sports: 200, Politics: 0
No category members found for Politics — falling back to search('politics').
Search 'politics': 100%|████████████████| 200/200 [00:01<00:00, 120.86titles/s]
Final counts -> Sports: 200, Politics: 200
Downloading Sports:   100%|████████████| 200/200 [02:22<00:00,  1.40it/s]
Downloading Politics: 100%|████████████| 200/200 [03:59<00:00,  1.20s/it]
Downloaded articles -> Sports: 198, Politics: 199
Using 198 articles per class (balanced).
Building unigram vocabulary and feature matrices (from scratch)...
Building ngram (1-3) vocabulary and TF-IDF...

Evaluating feature: bow_unigram   shape=(396, 11665)
 LogisticRegression → acc=0.9875  f1=0.9875
 LinearSVC          → acc=0.9875  f1=0.9875
 RandomForest       → acc=0.9875  f1=0.9875
...
Saved results to outputs/results_summary_wikinews.csv
```

⏱️ **Total runtime:** ~7–8 minutes (network-bound)

---

## 🧮 Feature Representations

All three representations are built **entirely from scratch** in pure NumPy — no `CountVectorizer` or `TfidfVectorizer`.

### Feature 01 · **Bag-of-Words**
**Vocabulary:** 11,665 tokens  
**Description:** Raw token counts. `X[i][j] = count(vⱼ, dᵢ)`. No normalisation. Simplest baseline — but performs on par with TF-IDF for LogReg and RF.

### Feature 02 · **TF-IDF Unigram**
**Vocabulary:** 11,665 tokens  
**Description:** TF × smooth IDF. Weights discriminative words higher, suppresses common noise. Same vocab as BoW — different weighting scheme.

### Feature 03 · **TF-IDF 1–3-gram**
**Vocabulary:** 177,913 tokens  
**Description:** Unigrams + bigrams + trigrams. Captures "won the match", "prime minister of". ~15× larger vocabulary than unigram alone.

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

### 🌲 Random Forest wins every feature configuration
All three feature sets → 98.75%. Its 200-tree ensemble handles both the 11K sparse unigram and the 177K n-gram space without degradation — no tuning required.

### 📦 Raw counts (BoW) ≥ TF-IDF for Logistic Regression
LogReg drops 98.75% → 95.00% switching from BoW to TF-IDF. For this task, *absolute frequency* is more discriminative — "football" appearing 20× is a strong signal that TF-IDF normalisation dilutes.

### 📉 More n-grams ≠ better for LinearSVC
LinearSVC falls 98.75% → 93.75% on the 177K n-gram space. The explosion of correlated bigram/trigram features makes max-margin harder to optimise within the fixed `max_iter=5000` budget.

### 🎯 Task is inherently easy — even the worst config achieves 93.75%
Sports and Politics have extremely distinct vocabularies (team names, scores vs. government terminology, party names). The ceiling effect limits differences between configurations to a few percentage points.

---

## ⚠️ Limitations

### 01 · Label Noise
**Search-API Politics labels**  
`Category:Politics` was empty. Search-based titles may include articles that only mention politics tangentially.

### 02 · Scale
**Small test set (80 articles)**  
One misclassification = 1.25% accuracy change. High variance — cross-validation would give more reliable estimates.

### 03 · Preprocessing
**No stop-word removal or stemming**  
Function words inflate vocabulary without discriminative signal. Porter stemming would reduce sparsity.

### 04 · Memory
**Dense 177K-feature matrix ≈ 563 MB**  
Dense NumPy arrays don't scale. `scipy.sparse.csr_matrix` would be needed for larger corpora.

### 05 · Vocabulary
**No min-df threshold**  
Single-occurrence tokens (hapax legomena) add noise to the vocabulary without generalisation benefit.

### 06 · Domain
**Wikinews prose style only**  
Short, neutral encyclopaedic articles. Likely degrades on social media, blogs, or other writing styles.

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

<div align="center">

**B23CM1053**  
*NLP Assignment · Problem 4 · Binary Text Classification on Wikinews*

</div>
