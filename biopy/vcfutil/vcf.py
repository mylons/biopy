__author__ = 'mikelyons'

class VCF(object):

    def __init__(self, vcfLine):
        self._tokens = vcfLine.split()
        self._chrom = tokens[0]
        self._pos = int(tokens[1])
        self._id = tokens[2]
        self._ref = tokens[3]
        self._alt = tokens[4]
        self._qual = float(tokens[5])
        self._filter = tokens[6]

    def chrom(self):
        return self._chrom

    def pos(self):
        return self._pos

    def id(self):
        return self._id

    def ref(self):
        return self._ref

    def alt(self):
        return self._alt

    def qual(self):
        return self._qual

    def filter(self):
        return self._filter

    def __str__(self):
        return "\t".join(self._tokens)
