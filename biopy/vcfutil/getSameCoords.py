__author__ = 'mikelyons'

from io import VCFReader, VCF

def hashVCF(vcf):
    return "%s:%d" % (vcf.chrom(), vcf.pos())

def dictifyVCF(vcfFile):
    reader = VCFReader(vcfFile)
    d = {}
    for vcf in reader.vcfs():
        d[hashVCF(vcf)] = vcf
    return d

def compareDicts(iter, d):
    union = {}
    for key in iter:
        if key in d:
            union[key] = iter[key]

    for key in d:
        if key in iter and key not in union:
            union[key] = d[key]

    for key in union:
        print str(union[key])




if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='compare vcfs and find variants with same coordiantes')
    parser.add_argument('-a', help='a vcf', required=True)
    parser.add_argument('-b', help='b vcf', required=True )
    args = vars(parser.parse_args())

    aDict = dictifyVCF(args['a'])
    bDict = dictifyVCF(args['b'])

    if len(aDict) > len(bDict):
        compareDicts(aDict, bDict)
    else:
        compareDicts(bDict, aDict)


