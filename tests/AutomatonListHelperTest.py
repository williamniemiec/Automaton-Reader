import unittest
import sys

sys.path.insert(1, "../src/")
from AutomatonListHelper import AutomatonListHelper


class AutomatonListHelperTest(unittest.TestCase):
    def testRemoveDuplicates(self):
        array = [2,3,4,3,3,3,3,6]
        arrayNoDuplicates = AutomatonListHelper.removeDuplicates(array)
        
        self.assertListEqual([2,3,4,6], arrayNoDuplicates)
    
    def testLargerSizeList_NotVisited_noAllSameSize(self):
        array = ['a', 'b', 'c', 'abc', 'd', 'e']
        visited = {'c': True, 'd': True}
        stackProcess = []
        largestElement = AutomatonListHelper.largestElementSize_NotVisited(array, visited, stackProcess)
        
        self.assertEqual('abc', largestElement)

    def testLargerSizeList_NotVisited_allSameSize(self):
        array = ['a', 'b', 'c', 'd', 'e']
        visited = {'c': True, 'd': True}
        stackProcess = []
        largestElement = AutomatonListHelper.largestElementSize_NotVisited(array, visited, stackProcess)
        
        self.assertListEqual(['a', 'b', 'e'], stackProcess)
        self.assertEqual(None, largestElement)
        
    def testLargerSizeList_NotVisited_allVisited(self):
        array = ['a', 'b', 'c', 'd', 'e']
        visited = {'a': True, 'b': True, 'c': True, 'd': True, 'e': True}
        stackProcess = []
        largestElement = AutomatonListHelper.largestElementSize_NotVisited(array, visited, stackProcess)
        
        self.assertEqual(None, largestElement)
        self.assertEqual([], stackProcess)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()