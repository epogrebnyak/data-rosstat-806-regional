import os
import sys
import unittest


# COMMENT: 
#         suggested change: rename 'etalon' to 'reference'
#         must import sample retions from test.sampleregions* (will need __init__.py in test)
#         suggested change: rename 'test' to 'sample_regions', test is ususally reserved for tests in package
#         make names uniform, not sample_regions1 and sample_regions_3, pick one style

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from region_titles import etalon_region_titles

from sample_regions1 import regions as regions_1
from sample_regions_3 import regions as regions_3


from funcs import filter_raw_sidenames

class TestStringMethods(unittest.TestCase):

  def test_match_1(self):
      for row_title, sample_title in regions_1.items():
          self.assertEqual(filter_raw_sidenames(row_title, etalon_region_titles), sample_title)

  def test_match_3(self):
    for n in range(4,18):
      name = __import__("sample_regions_{}".format(n)).name
      print(n, name)
      raw_regions = __import__("sample_regions_{}".format(n)).regions
      test = {filter_raw_sidenames(r,etalon_region_titles) for r in raw_regions}
      self.assertEqual(set(etalon_region_titles), test)


if __name__ == '__main__':
    unittest.main()

