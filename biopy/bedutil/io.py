from biopy.bedutil.exception import NoSuchBedError

__author__ = 'mikelyons'

from bed import *


class Util(object):
    @staticmethod
    def hash_bed(bed):
        return "%s-%d-%d" % (bed.chrom(), bed.start(), bed.end())
    @staticmethod
    def hash_annotated_bed(bed):
        return "%s-%s-%d-%d" % (bed.annotation(), bed.chrom(), bed.start(), bed.end())

class BedBuilder(object):
    @staticmethod
    def basic_bed(bed_line):
        return Bed(bed_line)
    @staticmethod
    def coverage_depth_bed(bed_line):
        return CoverageDepthBed(bed_line)
    @staticmethod
    def triple_annotated_bed(bed_line):
        return ThreeWayBed(bed_line)
    @staticmethod
    def annotated_bed(bed_line):
        return AnnotatedBed(bed_line)


class BedReader(object):
        def __init__(self, file_name, make_bed_func=BedBuilder.basic_bed):
            self._file = open(file_name)
            self._make_func = make_bed_func

        def beds(self):
            for bed_line in self._file:
                if bed_line[0] == '#':
                    #skip comments
                    continue
                yield self._make_func(bed_line.strip())


class BedDictionary(object):
    def __init__(self, beds, hash_func=Util.hash_bed):
        self._beds = dict()
        self._hash_func = hash_func
        for bed in beds:
            self._beds[hash_func(bed)] = bed

    def contains(self, bed):
        return self._beds.has_key( self._hash_func(bed) )

    def get(self, bed):
        if self.contains(bed):
            return self._beds[self._hash_func(bed)]
        else:
            raise NoSuchBedError, "bed %s is not in the dictionary" % str(bed)

    def keys(self):
        return self._beds.keys()