__author__ = 'mikelyons'

from biopy.bedutil.io import *

class UniquePosition(object):

    def __init__(self, bed_file, bed_builder_func='basic_bed'):
        self.reader = BedReader(bed_file, getattr(BedBuilder, bed_builder_func))

    def get_beds(self):
        d = {}
        for b in self.reader.beds():
            h = Util.hash_bed(b)
            if h not in d:
                d[h] = b
        return d


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='get features by unique genomic coordinates.'
                                                 'greedily chooses features.')
    parser.add_argument('-b', '--bed', help='bed file to count', required=True)
    parser.add_argument('-t', '--type', help='bed file types supported: [basic_bed, coverage_depth_bed, annotated_bed]', )
    args = vars(parser.parse_args())

    bed_type = (args['type'] if args['type'] else 'basic_bed')

    beds = UniquePosition(args['bed'], bed_type).get_beds()
    for b in beds:
        print str(beds[b])

