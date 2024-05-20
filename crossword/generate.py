import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == variable.DOWN else 0)
                j = variable.j + (k if direction == variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for key, values in self.domains.items():
            removing = set()
            for value in values:
                if len(value) != key.length:
                    removing.add(value)

            for value in removing:
                self.domains[key].remove(value)

        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        key = (x, y)
        do_changed = False
        keeping = set()
        shared_place = self.crossword.overlaps[key]
        if shared_place is None:
            return False
        for word1 in self.domains[x]:
            for word2 in self.domains[y]:
                if word1[shared_place[0]] == word2[shared_place[1]]:
                    keeping.add(word1)
                    break
        if self.domains[x] != keeping:
            self.domains[x] = keeping
            do_changed = True

        return do_changed
        # raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = []
        changed = False
        if arcs is None:
            queue = list(self.domains.keys())

        else:
            if len(arcs) == 0:
                return False
            queue = list(arcs)
        while True:
            arc = queue.pop(0)
            neighbors = self.crossword.neighbors(arc)
            for neighbor in neighbors:
                if neighbor in self.domains.keys():
                    if self.revise(arc, neighbor) is True:
                        changed = True
                        if len(self.domains[neighbor]) == 0:
                            return False
                        for neighbor2 in neighbors:
                            if neighbor2 not in queue:
                                queue.append(neighbor2)
            if len(queue) == 0:
                break

        return changed
        # raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for value in assignment.values():
            if type(value) is list or type(value) is set:
                if len(value) != 1:
                    return False
            else:
                if value is None:
                    return False

        return True
        # raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for key, words in assignment.items():
            for word in words:
                if key.length != len(word):
                    return False
        if self.ac3(assignment) is False:
            return True

        return False
        # raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        words_counter = dict()
        neighbors = self.crossword.neighbors(var)
        for word in self.domains[var]:
            count = 0
            for variable, words in assignment.items():
                if variable == var:
                    continue
                if word in words:
                    count += 1
                if variable in neighbors:
                    key = (var, variable)
                    shared_place = self.crossword.overlaps[key]
                    for word2 in words:
                        if word[shared_place[0]] != word2[shared_place[1]]:
                            count += 1
            words_counter[word] = count

        sorted_words = sorted(words_counter.keys(), key=lambda x: words_counter[x])
        return sorted_words
        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        min_words = 0
        variable = None
        for key, value in assignment.items():
            if key in self.domains.keys():
                if min_words == 0:
                    min_words = len(value)
                    variable = key
                else:
                    if min_words > len(value):
                        min_words = len(value)
                        variable = key
                    elif min_words == len(value):
                        if self.crossword.neighbors(key) > self.crossword.neighbors(variable):
                            min_words = len(value)
                            variable = key

        return variable
        # raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        assignment = self.domains
        result = dict()
        for key in self.domains.keys():
            result[key] = None
        while not self.assignment_complete(result):
            variable = self.select_unassigned_variable(assignment)
            sorted_words = self.order_domain_values(variable, assignment)
            del assignment[variable]
            if len(sorted_words) != 0:
                result[variable] = sorted_words[0]
            for words in assignment.values():
                if len(sorted_words) != 0:
                    if sorted_words[0] in words:
                        words.remove(sorted_words[0])
            self.ac3(assignment.keys())
            for words in assignment.values():
                if len(words) == 0:
                    return None

        return result
        # raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
