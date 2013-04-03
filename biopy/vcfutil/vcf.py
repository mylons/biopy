__author__ = 'mikelyons'

class VCF(object):

    def __init__(self, vcfLine):
        self._tokens = vcfLine.split()
        self._chrom = self._tokens[0]
        self._pos = int(self._tokens[1])
        self._id = self._tokens[2]
        self._ref = self._tokens[3]
        self._alt = self._tokens[4]
        self._qual = float(self._tokens[5])
        self._filter = self._tokens[6]
        #make info
        self._info = {}
        if len(self._tokens) > 6:
            info_tokens = self._tokens.split(";")
            for toke in info_tokens:
                tokes = toke.split("=")
                if len(tokes) > 1:
                    self._info[tokes[0]] = tokes[1]
                else:
                    self._info[tokes[0]] = True

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

    def has_info_key(self, key):
        return key in self._info

    def get_info_field(self, key):
        if key in self._info:
            return self._info[key]
        else:
            return None

    def __str__(self):
        return "\t".join(self._tokens)
