import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def persons_info(people, one_gene, two_genes, have_trait):
    persons = dict()
    for person in people:
        x = list()
        if person in one_gene:
            x.append(1)
        elif person in two_genes:
            x.append(2)
        else:
            x.append(0)

        if person in have_trait:
            x.append(True)
        else:
            x.append(False)

        persons[person] = x

    return persons


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    # print(people)
    probs = list()
    p = 1
    persons = persons_info(people.keys(), one_gene, two_genes, have_trait)

    for person, info in people.items():
        prob = 0
        if info["mother"] == None and info["father"] == None:
            prob = PROBS["gene"][persons[person][0]] * \
                PROBS["trait"][persons[person][0]][persons[person][1]]
            probs.append(prob)

        else:
            father_gave = PROBS["mutation"] if persons[info["father"]
                                                       ][0] == 0 else 1 - PROBS["mutation"]
            mother_gave = PROBS["mutation"] if persons[info["mother"]
                                                       ][0] == 0 else 1 - PROBS["mutation"]

            if persons[person][0] == 0:
                prob = (1 - father_gave) * (1 - mother_gave)

            elif persons[person][0] == 1:
                prob = (father_gave) * (1 - mother_gave) + (1 - father_gave) * (mother_gave)

            else:
                prob = (father_gave) * (mother_gave)

            prob = prob * PROBS["trait"][persons[person][0]][persons[person][1]]
            probs.append(prob)

    p = 1
    for b in probs:
        p = p * b

    return p
    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    persons = persons_info(probabilities.keys(), one_gene, two_genes, have_trait)
    for person in probabilities.keys():
        probabilities[person]["gene"][persons[person][0]] += p
        probabilities[person]["trait"][persons[person][1]] += p

    # raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        s1 = sum(probabilities[person]["gene"].values())
        for gene in probabilities[person]["gene"].keys():
            probabilities[person]["gene"][gene] = probabilities[person]["gene"][gene]/s1
        s2 = sum(probabilities[person]["trait"].values())
        for trait in probabilities[person]["trait"].keys():
            probabilities[person]["trait"][trait] = probabilities[person]["trait"][trait]/s2

    # raise NotImplementedError


if __name__ == "__main__":
    main()
