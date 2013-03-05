__author__ = 'mikelyons'

from vcf import VCF

class VCFReader(object):

    def __init__(self, fileName):
        self._fileName = fileName
        self._file = open(fileName)

    def open(self):
        if self._file.closed:
            self._file = open(self._fileName)

    def close(self):
        if not self._file.closed:
            self._file.close()

    def closed(self):
        return self._file.closed

    def vcfs(self):
        for vcfLine in self._file:
            if vcfLine[0] == '#':
                #skip comments
                continue
            yield VCF(vcfLine)

