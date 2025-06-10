# PageRank Algorithm Implementation

## Overview

This project implements the **PageRank algorithm** for ranking web pages based on the link structure of a corpus of HTML files. The algorithm models the behavior of a "random surfer" and estimates the importance of each page by analyzing incoming and outgoing links using two approaches:

- **Sampling-based PageRank estimation** (Monte Carlo simulation of random walks)  
- **Iterative PageRank computation** (power iteration method until convergence)

This implementation captures key concepts in information retrieval, graph theory, and Markov chains and is suitable for educational purposes or foundational research projects in search algorithms.

---

## Features

- **Corpus Crawling:**  
  Parses a directory of HTML files, extracting hyperlinks and building a graph representation of pages and their outgoing links.

- **Transition Model:**  
  Computes the probability distribution over next pages to visit from a given current page, incorporating the damping factor (random jump probability).

- **Sampling-based PageRank:**  
  Approximates PageRank by simulating `n` random surfer steps according to the transition model.

- **Iterative PageRank Calculation:**  
  Uses repeated rank updates until convergence to a tolerance level, efficiently computing PageRank values for the entire corpus.

- **Dangling Page Handling:**  
  Pages with no outbound links are treated as linking to every page in the corpus, avoiding sink states in the Markov chain.

---

## Usage

### Running the Program

```bash
python pagerank.py /path/to/corpus
````

* The program expects a command-line argument — the path to a directory containing `.html` files.
* Outputs PageRank values computed via sampling and iteration.

### Output Example

```
PageRank Results from Sampling (n = 10000)
  1.html: 0.2187
  2.html: 0.1035
  3.html: 0.1824
  ...
PageRank Results from Iteration
  1.html: 0.2213
  2.html: 0.1019
  3.html: 0.1802
  ...
```

---

## Implementation Details

### Key Constants

* `DAMPING = 0.85` — Probability of following a link from the current page.
* `SAMPLES = 10000` — Number of samples used in the sampling method.

### Core Components

#### `crawl(directory) -> dict`

* Parses all HTML files in the directory.
* Returns a dictionary mapping each page to the set of pages it links to (filtered to corpus pages only).

#### `transition_model(corpus, page, damping_factor) -> dict`

* Computes the probability distribution over which page to visit next.
* Combines link-following with a random jump to any page.

#### `sample_pagerank(corpus, damping_factor, n) -> dict`

* Simulates a random surfer for `n` steps starting at a random page.
* Returns estimated PageRank values as the normalized visit counts.

#### `iterate_pagerank(corpus, damping_factor) -> dict`

* Iteratively updates PageRank values until convergence within a threshold (0.001).
* Handles dangling pages by assigning them links to all pages.
* Returns final PageRank values.

---

## Algorithmic Explanation

PageRank models a Markov chain where each page is a state and the surfer transitions based on outbound links. The damping factor models the probability the surfer will jump to a random page instead of following a link.

* **Sampling Approach:**
  Mimics the random surfer via repeated probabilistic steps, gathering empirical visit frequencies.

* **Iterative Approach:**
  Uses the power method to compute the stationary distribution of the Markov chain formed by the link structure.

---

## Dependencies

* Standard Python 3.x modules only. No external dependencies.

---

## Author and Contact

**Author:** Sandrin Muramutsa & CS50

---

## References

* Page, L., Brin, S., Motwani, R., & Winograd, T. (1999). The PageRank Citation Ranking: Bringing Order to the Web. *Stanford InfoLab*.
* Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.

---
