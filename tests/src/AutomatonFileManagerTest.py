import unittest
import sys

sys.path.insert(1, "../../")
from src.AutomatonFileManager import AutomatonFileManager


class AutomatonFileManagerTest(unittest.TestCase):
    def testCsvToWordList(self):
        wordList = AutomatonFileManager.csvToWordList("words.txt")
        
        self.assertListEqual([['a', 'b', 'c', 'd'], ['s1', 's2', 's3']], wordList)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()