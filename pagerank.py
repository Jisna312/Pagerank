
import os
import random
import re
import sys

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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_dist = {page_name : 0 for page_name in corpus}
    if len(corpus[page]) == 0:
        for pages in prob_dist:
            prob_dist[pages] = 1/len(corpus)
        return prob_dist
    else:
        for pages in prob_dist:
            if pages in corpus[page]:
                prob_dist[pages] = damping_factor*1/len(corpus[page]) + (1-damping_factor)*1/len(corpus)
            elif pages not in corpus[page]:
                prob_dist[pages] = (1-damping_factor)*1/len(corpus)
        return prob_dist

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    visit = {page_name: 0 for page_name in corpus}

    curr_page = random.choice(list(visit))
    visit[curr_page] += 1

    for i in range(n-1):
        model = transition_model(corpus, curr_page, damping_factor)
        next_page = random.choices(list(model.keys()), weights=list(model.values()), k=1)[0]
        visit[next_page]+=1
        curr_page = next_page
    pagerank = {page_name: 0 for page_name in corpus}
    for pages in pagerank:
        pagerank[pages] = visit[pages]/n
    return pagerank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    random_prob = (1- damping_factor)/len(corpus)
    pagerank = {page_name:1/len(corpus) for page_name in corpus}
    newrank = {page_name: None for page_name in corpus}
    max_rank_change = .5
    iterations = 0
    while max_rank_change>.001:
        iterations += 1
        max_rank_change = 0
        for page_name in corpus:
            surf_choice_prob = 0
            for other_page in corpus:
                if len(corpus[other_page]) == 0:
                    surf_choice_prob += pagerank[other_page] * 1/len(corpus)
                elif page_name in corpus[other_page]:
                    surf_choice_prob += pagerank[other_page] / len(corpus[other_page])

            newrank[page_name] =random_prob + damping_factor*surf_choice_prob


        for page in corpus:
            rank_change = abs(newrank[page] - pagerank[page])
            max_rank_change = max(max_rank_change,rank_change)
        for page in pagerank:
            pagerank[page] = newrank[page]
    return pagerank











if __name__ == "__main__":
    main()
