from biopy.bedutil.exception import MalformedBedError

__author__ = 'mikelyons'


BED_DELIM = "\t"

class Bed(object):


    def __init__(self, bed_line):
        """
        default constructor for bed
        """
        self._tokens = bed_line.split(BED_DELIM)
        self._contig_name = self._tokens[0]
        self._start = int(self._tokens[1])
        self._end = int(self._tokens[2])

    def __str__(self):
        return "%s\t%d\t%d" % (self._contig_name, self._start, self._end)

class CoverageBed(Bed):

    def __init__(self, bed_line):
        """
        Bed from output of coverageBed
        """
        Bed.__init__()
        if len(self._tokens) < 7:
            raise MalformedBedError, "not enough fields to be a CoverageBed: %s" % self._tokens
        self._num_b_overlaps = int(self._tokens[3])
        self._num_bases_covered = int(self._tokens[4])
        self._length_of_entry_in_b = int(self._tokens[5])
        self._frac_of_bases_covered = float(self._tokens[6])





