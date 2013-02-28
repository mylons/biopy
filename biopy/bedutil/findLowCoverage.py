import sys
from biopy.bedutil.io import *

class FindLowCoverage(object):
    def __init__(self, bed_file, depth_max=10, bed_type=BedBuilder.coverage_depth_bed):
        self._bed_file = bed_file
        self.depth_max = depth_max
        self._bed_type = bed_type

    def find_beds(self):
        reader = BedReader(self._bed_file, self._bed_type)
        for bed in reader.beds():
            if bed.depth_at_position() < self.depth_max:
                yield bed

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='find low coverage positions in coverageBed -d bed file')
    parser.add_argument('-b', '--bed', help='bed file', required=True)
    parser.add_argument('-t', '--type', help='bed file types supported: [coverage_depth_bed]', )
    args = vars(parser.parse_args())

    bed_type = (args['type'] if args['type'] else 'coverage_depth_bed')

    f = FindLowCoverage(args['bed'])
    for b in f.find_beds():
        print str(b)


