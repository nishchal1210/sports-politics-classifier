# 📰 Sports vs Politics Text Classifier  
**Binary Text Classification on Wikinews Articles**

---

## 📌 Overview

This project implements a complete end-to-end NLP pipeline to classify news articles as **Sports (0)** or **Politics (1)** using Wikinews data.

The system includes:

- Data collection via MediaWiki API
- HTML scraping using BeautifulSoup
- Text preprocessing
- Feature engineering (implemented from scratch)
- 3 machine learning classifiers
- 9 experimental configurations
- Quantitative comparison with full metrics

📄 Full Report:  
[Download Report (PDF)](report/B23CM1053_prob4.pdf)

---

## 🧠 Problem Statement

Design a binary classifier that reads a text document and classifies it as:

- **Sports**
- **Politics**

Compare:

- 3 Feature Representations
- 3 Machine Learning Models

Total: **9 experimental combinations**

---

## 📊 Dataset

Source: https://en.wikinews.org  
Collected using MediaWiki API.

| Property | Value |
|----------|--------|
| Articles per class | 198 |
| Total Articles | 396 |
| Train/Test Split | 80% / 20% |
| Balanced Dataset | Yes |

---

## ⚙️ Feature Representations (From Scratch)

Implemented manually using NumPy (no sklearn vectorizers).

### 1️⃣ Bag-of-Words (Unigram)
Raw term frequency counts.

### 2️⃣ TF-IDF (Unigram)
TF × Smoothed IDF

### 3️⃣ TF-IDF (1–3 Gram)
Unigrams + Bigrams + Trigrams

Vocabulary sizes:

- Unigram: 11,665
- 1–3 Gram: 177,913

---

## 🤖 Classifiers

- Logistic Regression
- Linear SVC
- Random Forest (200 trees)

---

## 📈 Results

| Feature | Classifier | Accuracy |
|----------|-------------|----------|
| BoW | Random Forest | **98.75%** |
| BoW | Logistic Regression | 98.75% |
| TF-IDF (Unigram) | Linear SVC | 98.75% |
| TF-IDF (1–3gram) | Random Forest | 98.75% |

Worst configuration:

- TF-IDF 1–3gram + LinearSVC → 93.75%

📊 Full results available in:
