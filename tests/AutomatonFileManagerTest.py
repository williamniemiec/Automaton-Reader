import unittest
import sys

sys.path.insert(1, "../src/")
from AutomatonFileManager import AutomatonFileManager


class AutomatonFileManagerTest(unittest.TestCase):
    def testCsvToWordList(self):
        wordList = AutomatonFileManager.csvToWordList("media/words.txt")
        
        self.assertListEqual([['a', 'b', 'c', 'd'], ['s1', 's2', 's3']], wordList)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()