__author__ = 'mikelyons'
import unittest
from biopy.bedutil.io import *
from biopy.bedutil.exception import *

class BedTests(unittest.TestCase):

    chrom = "chr1"
    start_position = 1
    stop_position = 11
    length = (stop_position - 1) - start_position
    annotation = "ANNO1"
    position_in_target = 1
    position_depth = 10

    #bed lines
    basic_bed_line = "%s\t%d\t%s" % (chrom, start_position, stop_position)
    annotated_bed_line = "%s\t%s" % (basic_bed_line, annotation)
    coverage_depth_bed_line = "%s\t%d\t%d" % (annotated_bed_line, position_in_target, position_depth)



    def test_basic_bed(self):
        b = BedBuilder.basic_bed(self.basic_bed_line)
        self.assertEqual(self.chrom, b.chrom())
        self.assertEqual(self.start_position, b.start())
        self.assertEqual(self.stop_position, b.end())
        self.assertEqual(self.length, b.length())
        self.assertEqual(self.length, b.length())

    def test_annotated_bed(self):
        b = BedBuilder.annotated_bed(self.annotated_bed_line)
        self.assertEqual(self.chrom, b.chrom())
        self.assertEqual(self.start_position, b.start())
        self.assertEqual(self.stop_position, b.end())
        self.assertEqual(self.length, b.length())
        self.assertEqual(self.annotation, b.annotation())

    def test_coverage_depth_bed(self):
        self.assertRaises(MalformedBedError, BedBuilder.coverage_depth_bed, self.basic_bed_line)
        b = BedBuilder.coverage_depth_bed(self.coverage_depth_bed_line)
        self.assertEqual(self.chrom, b.chrom())
        self.assertEqual(self.start_position, b.start())
        self.assertEqual(self.stop_position, b.end())
        self.assertEqual(self.length, b.length())
        self.assertEqual(self.annotation, b.annotation())
        self.assertEqual(self.position_in_target, b.position_in_feature())
        self.assertEqual(self.position_depth, b.depth_at_position())
        self.assertEqual(False, b.is_uncovered())

if __name__ == '__main__':
    unittest.main()

