import os
import random
import re
import sys
import collections

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    probability_distribution = collections.defaultdict(int)
    pages_count = len(corpus[page])

    for link in corpus[page]:
        link_follow_prob = damping_factor * (1 / pages_count)
        probability_distribution[link] = link_follow_prob

    all_pages = list(corpus.keys())
    for link in all_pages:
        random_follow_prob = (1 - damping_factor) / (pages_count + 1)
        probability_distribution[link] += random_follow_prob

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pages = list(corpus.keys())
    page_ranks = {page: 0 for page in pages}

    # Initial sample
    start_page = random.choice(pages)
    page_ranks[start_page] += 1
    curr_page = start_page

    for i in range(1, n):
        # Pass previous sample to the transition model
        sample_distribution = transition_model(corpus, curr_page, damping_factor)
        population, weights = list(sample_distribution.keys()), list(
            sample_distribution.values()
        )
        curr_page = random.choices(population=population, weights=weights)[0]

        # Update page_rank
        page_ranks[curr_page] += 1

    page_ranks = {page: rank / n for page, rank in page_ranks.items()}
    print("Sampling", page_ranks)

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pages = list(corpus.keys())

    # Dangling node handling: page with no links should point to all pages in the ecosystem
    for page in corpus.keys():
        if not corpus[page]:
            corpus[page] = pages

    # Assign intial rank of  1 / N
    pages_count = len(pages)
    initial_rank = 1 / pages_count
    page_ranks = {page: initial_rank for page in pages}

    while True:
        new_page_ranks = {}
        for page in pages:

            # Calculate the PageRank of the current page, PR (page)

            # Get pages that link to current page
            parent_pages = []
            for parent_page in pages:
                if page in corpus[parent_page]:
                    parent_pages.append(parent_page)

            # Calculate the random jump probability
            random_jump_prob = (1 - damping_factor) / pages_count

            # Calculate the link-based weighted probability of each possible parent
            rank_contribution_prob_sum = 0
            for parent_page in parent_pages:
                parent_page_rank = page_ranks[parent_page]
                parent_page_num_links = len(corpus[parent_page])
                rank_contribution_prob_sum += parent_page_rank / parent_page_num_links

            rank_contribution_prob = damping_factor * rank_contribution_prob_sum
            new_rank = random_jump_prob + rank_contribution_prob
            new_page_ranks[page] = new_rank

        # Check if we have the desired converge tolerance of 0.001 for all pages
        convergence = True
        for page in pages:
            if abs(page_ranks[page] - new_page_ranks[page]) > 0.001:
                convergence = False

        if convergence:
            return new_page_ranks

        # Update page rank when converge tolerance is still under 0.001
        page_ranks = new_page_ranks


if __name__ == "__main__":
    main()
