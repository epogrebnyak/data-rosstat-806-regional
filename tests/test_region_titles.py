import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sample_regions1 import regions as regions_1
from region_titles import etalon_region_titles

from funcs import filter_raw_sidenames

class TestStringMethods(unittest.TestCase):

  def test_match_1(self):
      for row_title, sample_title in regions_1.items():
          self.assertEqual(filter_raw_sidenames(row_title, etalon_region_titles), sample_title)

if __name__ == '__main__':
    unittest.main()

