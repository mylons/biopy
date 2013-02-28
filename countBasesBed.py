__author__ = 'mikelyons'

from biopy.bedutil.io import *


class CountBasesBed(object):

    def __init__(self, bed_file, bed_builder_func='basic_bed'):
        self.reader = BedReader(bed_file, getattr(BedBuilder, bed_builder_func))

    def count_bases(self):
        if self.reader.closed():
            self.reader.open()
        return sum(b.length() for b in self.reader.beds())



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='count bases in bed file')
    parser.add_argument('-b', '--bed', help='bed file to count', required=True)
    parser.add_argument('-t', '--type', help='bed file types supported: [basic_bed, coverage_depth_bed, annotated_bed]', )
    args = vars(parser.parse_args())

    bed_type = (args['type'] if args['type'] else 'basic_bed')

    counter = CountBasesBed(args['bed'], bed_type)
    print counter.count_bases()
