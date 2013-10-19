#! /usr/bin/env python
#-*- coding: utf-8 -*-

from recsys.similarity.user_similar import UserSimilar
from recsys.utils.sparse_matrix import DictMatrix
import bsddb
import unittest

class UserSimilarTestCase(unittest.TestCase):  
    def setUp(self):  
        db = bsddb.btopen(None, cachesize = 268435456)
        matrix = DictMatrix(10, 10, db)        
        m1, m2 = ([0, 1, 2, 3], [2, 3, 1, 4])
        for i in range(2):
            for j in range(4):
                if i == 0:
                    matrix[i, j] = m1[j]
                else:
                    matrix[i, j] = m2[j]
        self.similar = UserSimilar(matrix)  
          
    def tearDown(self):  
        self.similar = None  
          
    def testCompute(self):      
        self.assertEqual(True, abs(self.similar.compute(0,1) - 0.166) < 0.01)
    
    def testTopN(self):
        self.assertEqual([1], self.similar.topN(0))

if __name__ == "__main__":  
    unittest.main()  