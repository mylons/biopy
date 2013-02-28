import sys
from biopy.bedutil.io import *

reader = BedReader("/tmp/coverage.bed", BedBuilder.coverage_depth_bed)

depth_limit = 10

for bed in reader.beds():
    if bed.depth_at_position() < 10:
        print str(bed)

