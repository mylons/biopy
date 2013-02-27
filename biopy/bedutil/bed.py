from biopy.bedutil.exception import MalformedBedError

__author__ = 'mikelyons'


BED_DELIM = "\t"

class Bed(object):


    def __init__(self, bed_line):
        """
        default constructor for bed
        """
        self._tokens = bed_line.strip().split(BED_DELIM)
        self._chrom = self._tokens[0]
        self._start = int(self._tokens[1])
        self._end = int(self._tokens[2])

    def __str__(self):
        return "%s\t%d\t%d" % (self._chrom, self._start, self._end)


    def chrom(self):
        return self._chrom

    def start(self):
        return self._start

    def end(self):
        return self._end

    def length(self):
        return (self._end - 1) - self._start

class AnnotatedBed(Bed):

    def __init__(self, bed_line):
        Bed.__init__(self,bed_line)
        self._annotation = self._tokens[3]

    def annotation(self):
        return self._annotation

    def __str__(self):
        return "%s\t%d\t%d\t%s" % (self.chrom(), self.start(), self.end(), self.annotation())


class CoverageDepthBed(AnnotatedBed):

    def __init__(self, bed_line):
        """
        Bed from output of coverageBed
        """
        AnnotatedBed.__init__(self, bed_line)
        if len(self._tokens) < 6:
            raise MalformedBedError, "not enough fields to be a CoverageBed: %s" % self._tokens
        self._position_in_feature = int(self._tokens[4])
        self._depth_at_position = int(self._tokens[5])

    def position_in_feature(self):
        return self._position_in_feature

    def depth_at_position(self):
        return self._depth_at_position

    def is_uncovered(self):
        return self.depth_at_position() == 0

    def __str__(self):
        return "%s\t%d\t%d\t%s\t%d\t%d" % (self.chrom(), self.start(), self.end(), self.annotation(), self.position_in_feature(), self.depth_at_position())






class ThreeWayBed(AnnotatedBed):

    def __init__(self, bed_line):
        AnnotatedBed.__init__(self, bed_line)
        #make target bed
        refgene_bed_line = BED_DELIM.join(self._tokens[4:8]) #doesn't include 8
        self._refgene_bed = AnnotatedBed(refgene_bed_line)
        #make refgene bed
        primer_bed_line = BED_DELIM.join(self._tokens[8:]) #rest of the list
        self._primer_bed = AnnotatedBed(primer_bed_line)

    def primer(self):
        return self._primer_bed

    def refgene(self):
        return self._refgene_bed

    def target(self):
        return self


class BedUtil(object):
    @staticmethod
    def overlap_bases(bed1, bed2):
        overlap_start = 1
        overlap_end = 2
        if bed1.start() > bed2.start():
            overlap_start = bed1.start()
        else:
            overlap_start = bed2.start()

        if bed1.end() > bed2.end():
            overlap_end = bed2.end()
        else:
            overlap_end = bed1.end()

        return (overlap_end - 1) - overlap_start

    @staticmethod
    def overlap_percentage(bed1, bed2):
        return 100 * (float(BedUtil.overlap_bases(bed1, bed2)) / bed1.length())
