import os
import sys
import unittest

from reference_region_names import reference_region_names

# test data samples in one dict(key=source_xls_filename, value=list of raw titles)
from testdata import test_regions_dict

# function to test
from filter_region_name import filter_raw_region_name

class TestStringMethods(unittest.TestCase):

  def test_match(self):
    for key, sample in test_regions_dict.items():
      print("From file: ", key)
      test = {filter_raw_region_name(r) for r in sample}
      self.assertEqual(set(reference_region_names), test)
      print("\tOk")


if __name__ == '__main__':
  print("testing filter_raw_sidenames() for region titles\n")
  unittest.main()

