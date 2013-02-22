__author__ = 'mikelyons'

from bed import Bed, CoverageBed


class BedBuilder(object):
    @staticmethod
    def basic_bed(bed_line):
        return Bed(bed_line)
    @staticmethod
    def coverage_bed(bed_line):
        return CoverageBed(bed_line)


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
