__author__ = 'mikelyons'
from biopy.bedutil.io import *

class UniqueAnnotations(object):

    def __init__(self, annotated_bed_file):
        self.reader = BedReader(annotated_bed_file, BedBuilder.annotated_bed)

    def get_beds(self):
        """
        picks first annotation it finds, returns dictionary
        """
        d = {}
        for bed in self.reader.beds():
            if bed.annotation() not in d:
                d[bed.annotation()] = bed
        return d

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='get unsorted unique beds by annotation')
    parser.add_argument('-b', '--bed', help='minimum 4 column annotated bed file, extra columns are ignored', required=True)
    args = vars(parser.parse_args())

    u = UniqueAnnotations(args['bed'])
    beds = u.get_beds()
    for b in beds:
        print str(beds[b])



