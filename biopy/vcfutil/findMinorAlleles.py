__author__ = 'mikelyons'

from io import VCFReader


def hash_string(vcf):
    return "%s-%s" % (vcf.chrom, vcf.pos)


def make_vcfs(vcf_file):

    reader = VCFReader(vcf_file)
    vcfs = {}
    for vcf in reader.vcfs():
        vcfs[hash_string(vcf)] = vcf
    return vcfs


def compare_minor_allele_records(dbsnp, experiment):
    for key in dbsnp:
        if key in experiment:
            print "%s" % str(experiment[key])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='find minor alleles in vcf')
    parser.add_argument('-d', help='dbsnp vcf', required=True)
    parser.add_argument('-v', help='analysis vcf', required=True )
    args = vars(parser.parse_args())

    d = make_vcfs(args['d'])
    v = make_vcfs(args['v'])
    compare_minor_allele_records(d, v)

