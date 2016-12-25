'''Text Generator

Usage:
    generate.py GRAMMAR_FILE
    generate.py GRAMMAR_FILE [-n LINES] [-s FILE_PATH]

Options:
    -h --help    show this
    -n LINES --number=LINES  amount of lines to generate [default: 1]
    -s FILE_PATH --save=FILE_PATH the full path (including name) of the file to save the output to.

'''
from collections import defaultdict
from docopt import docopt
import random


class PCFG(object):
    '''
    Yay docstring!@#!2!
    '''

    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)

    def add_rule(self, lhs, rhs, weight):
        assert (isinstance(lhs, str))
        assert (isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w, l, r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l, r, w)
        return grammar

    def is_terminal(self, symbol):
        return symbol not in self._rules

    def gen(self, symbol):
        if self.is_terminal(symbol):
            return symbol
        else:
            expansion = self.random_expansion(symbol)
            return " ".join(self.gen(s) for s in expansion)

    def random_sent(self):
        return self.gen("ROOT")

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r, w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r


def save_to_file(save_file, sentences):
    if save_file != None:
        with open(save_file, 'w') as output_file:
            output_file.write(sentences)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    # print arguments
    pcfg = PCFG.from_file(arguments['GRAMMAR_FILE'])
    sentences = '\n'.join(pcfg.random_sent() for i in xrange(int(arguments['--number'])))
    print sentences
    save_to_file(arguments['--save'], sentences)
