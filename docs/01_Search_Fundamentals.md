# 01 - Search Fundamentals & BM25

Before AI, search was primarily about **Inverted Indexes** and **Keyword Frequency**. This document explains how engines like Elasticsearch and Vespa decide which document is "best" for a keyword query.

## 1. The Inverted Index
Imagine a book. Instead of reading every page to find "Vespa", you look at the index at the back.
- **Search engines do the same:** They store a list of every word (token) and which document IDs contain it.
- **Complexity:** O(1) to find a word, rather than O(N) to scan everything.

## 2. BM25 (Best Matching 25)
Both Elasticsearch and Vespa use **BM25** as their default ranking algorithm for text. It improved upon the older TF-IDF (Term Frequency-Inverse Document Frequency).

BM25 calculates a score based on three main factors:
1.  **Term Frequency (TF):** How many times does the word appear in the document? (More is better, but with "diminishing returns"—appearing 100 times isn't 100x better than 1).
2.  **Inverse Document Frequency (IDF):** How rare is this word across the whole index? (The word "The" is common and worthless; the word "Vespa" is rare and highly relevant).
3.  **Document Length:** A word appearing in a 10-word title is more significant than that same word buried in a 5,000-word essay.

## 3. Limitations
BM25 only knows about **keywords**. If you search for "automobile", it will not find a document that only says "car". This is why we move toward **Semantic Search**.
