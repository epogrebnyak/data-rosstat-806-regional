import os
import sys
import unittest



# COMMENT: 
#         suggested change: rename 'etalon' to 'reference'
#         must import sample retions from test.sampleregions* (will need __init__.py in test)
#         suggested change: rename 'test' to 'sample_regions', test is ususally reserved for tests in package
#         make names uniform, not sample_regions1 and sample_regions_3, pick one style


from reference_region_names import reference_region_names

# test data samples in one dict(key=source_xls_filename, value=list of raw titles )
from  sample_regions_tests import test_regions_dict

# function to tests
from filter_raw_sidenames import filter_raw_sidenames

class TestStringMethods(unittest.TestCase):

  def test_match(self):
    for key,sample in test_regions_dict.items():
      print("From file: ", key)
      test = {filter_raw_sidenames(r,reference_region_names) for r in sample}
      self.assertEqual(set(reference_region_names), test)
      print("\tOk")


if __name__ == '__main__':
  print("testing filter_raw_sidenames() for region titles\n")
  unittest.main()

