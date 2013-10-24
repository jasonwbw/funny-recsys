#! /usr/bin/env python
#-*- coding: utf-8 -*-

from recsys.similarity.herlocker_user_similar import HerlockerUserSimilar
from recsys.utils.sparse_matrix import DictMatrix
import bsddb
import unittest

class HerlockerUserSimilarTestCase(unittest.TestCase):  
    def setUp(self):  
        db = bsddb.btopen(None, cachesize = 268435456)
        matrix = DictMatrix(10, 10, db)        
        m1, m2 = ([1, 1, 2, 3], [1, 1, 2, 3])
        for i in range(1,3):
            for j in range(1,5):
                if i == 1:
                    matrix[i, j] = m1[j-1]
                else:
                    matrix[i, j] = m2[j-1]
        self.similar = HerlockerUserSimilar(matrix)  
          
    def tearDown(self):  
        self.similar = None  
          
    def testCompute(self):      
        self.assertEqual(True, abs(self.similar.compute(1,2) - 0.08) < 0.01)

if __name__ == "__main__":  
    unittest.main()  