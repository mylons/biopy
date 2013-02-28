__author__ = 'mikelyons'

from biopy.bedutil.io import *


class AverageFeatureSize(object):

    def __init__(self, bed_file, bed_builder_func='basic_bed'):
        self.reader = BedReader(bed_file, getattr(BedBuilder, bed_builder_func))

    def average_beds(self):
        if self.reader.closed():
            self.reader.open()
        #sum(b.length() for b in self.reader.beds())
        the_sum = 0
        total_beds = 0
        for b in self.reader.beds():
            total_beds += 1
            the_sum += b.length()
        return float(the_sum) / float(total_beds)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='count bases in bed file')
    parser.add_argument('-b', '--bed', help='bed file to count', required=True)
    parser.add_argument('-t', '--type', help='bed file types supported: [basic_bed, coverage_depth_bed, annotated_bed]', )
    args = vars(parser.parse_args())

    bed_type = (args['type'] if args['type'] else 'basic_bed')

    print AverageFeatureSize(args['bed'], bed_type).average_beds()

