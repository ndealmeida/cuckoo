# 03 - Embeddings & Compute Strategy

Semantic search relies on turning text into numbers (vectors) that represent "meaning."

## 1. How Embeddings Work
We use **SBERT (Sentence-BERT)**. It takes a sentence and maps it to a point in high-dimensional space (in our case, 384 dimensions).
- **The Magic:** Two sentences with similar meanings (e.g., "how to build AI" and "creating machine learning systems") will be physically close to each other in this 384-D space, even if they share zero words.

## 2. Choosing the Model: `all-MiniLM-L6-v2`
In this playground, we use the `all-MiniLM-L6-v2` model.
- **Why?** It's a good choice for local development. It is small (~80MB), very fast, and surprisingly accurate for its size.
- **Dimensions:** It produces 384 dimensions. Larger models (like `all-mpnet-base-v2`) produce 768 dimensions but are 5x slower and 10x larger.

## 3. CPU vs. GPU Intensity
You'll notice the initial "Generatings embeddings..." step in our logs can be slow on CPU.

### Local (CPU)
- **Status:** CPU-intensive. Generating embeddings for 3 documents is fast, but for 1,000,000 it would take days on a laptop.
- **Why?** Matrix multiplications (the core of AI) are calculated sequentially or in small parallel batches on a CPU.

### Production (GPU)
- **Status:** GPU-intensive.
- **Why?** GPUs (NVIDIA/Apple MPS) can do thousands of matrix multiplications at the exact same time. In a production pipeline, we would send batches of text to a GPU cluster, making the process 50x-100x faster.
- **Note:** In this playground, we optimize for **low memory footprint** so the whole stack (ES, Vespa, Python) can run on a single machine.
