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

    pageDict = {}
    pages = list(corpus.keys())
    pageLinks = corpus[page]
    if len(pageLinks) != 0:
        new_damping_factor = damping_factor/len(pageLinks)

    all_damping_factor = (1 - damping_factor)/len(pages)
    
    for page in pages:
        pageDict[page] = all_damping_factor
    
    for link in pageLinks:
        pageDict[link] += new_damping_factor

    return pageDict
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    choices = []
    pages = list(corpus.keys())
    choice = random.choice(pages)
    choices.append(choice)
    for _ in range(1,n):
        newcorpus = transition_model(corpus, choice, damping_factor)
        pages = list(newcorpus.keys())
        pages_props = list(newcorpus.values())
        choiceList = random.choices(pages, weights=pages_props, k=1)
        choice = choiceList[0]
        choices.append(choice)

    newDict = {}
    for page in pages:
        newDict[page] = choices.count(page)/len(choices)

    return newDict
    #raise NotImplementedError


def less_than(list1, list2):
    for i in range(len(list1)):
        if abs(list1[i] - list2[i]) > 0.001:
            return False
        
    return True

def gives_p(corpus, p):
    links = []
    for key, value in corpus.items():
        if p in value:
            links.append(key)

    return links

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    for page in corpus.keys():
        if not corpus[page]:
            corpus[page] = corpus.keys()

    pages = list(corpus.keys())
    pages_props = []
    for _ in pages:
        pages_props.append(1/len(pages))
    
    props_dict = {}
    for i in range(len(pages)):
        props_dict[pages[i]] = pages_props[i]

    prop = (1-damping_factor)/len(pages)
    while True:
        #print("entered")
        props_dict2 = {}
        pages_props2 = []
        for page in pages:
            prop2 = 0
            links = gives_p(corpus, page)
            for link in links:
                prop2 += props_dict[link]/len(corpus[link])

            prop3 = prop + damping_factor * prop2
            pages_props2.append(prop3)
            props_dict2[page] = prop3
        
        props_dict = props_dict2
        if less_than(pages_props, pages_props2) == True:
            return props_dict
        
        pages_props = pages_props2
    #raise NotImplementedError


if __name__ == "__main__":
    main()
