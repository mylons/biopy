__author__ = 'mikelyons'

from biopy.vcfutil.io import *
from biopy.bedutil.io import *


#assumes beds are sorted
def bed_search(beds, pos):

    def helper(start, stop):
        middle = stop / 2

        if pos < beds[middle].start():
            helper(start, middle - 1)

        elif pos > beds[middle].stop():
            helper(middle, stop)

        elif (pos >= beds[middle].start()) and (pos < beds[middle].stop()):
            return beds[middle]

        else:
            return None

    return helper(0, len(beds))

def compare_bed_and_vcf(vcf, bed):
    reader = BedReader(bed, BedBuilder.annotated_bed)
    beds = [b for b in reader.beds()]
    reader = VCFReader(vcf)

    for vcf in reader.vcfs():
        bed = bed_search(beds, vcf.pos())
        if bed is not None:
            print "=================================================================="
            print str(vcf)
            print str(bed)
            print "=================================================================="


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='check if vcf is inside a bed range')
    parser.add_argument('-v', help='vcf', required=True)
    parser.add_argument('-b', help='bed', required=True )

    args = vars(parser.parse_args())

    compare_bed_and_vcf(args['v'], args['b'])

