#! /usr/bin/env python
#-*- coding: utf-8 -*-

from recsys.similarity.distance.pearson_distance import PearsonDistance
from recsys.exception.error_wrongvec import WrongVecError
import numpy as np
import unittest

class PearsonDistanceTestCase(unittest.TestCase):  
    def setUp(self):  
        self.distance = PearsonDistance()  
      
    def tearDown(self):  
        self.distance = None  
      
    def testDistance(self):  
        self.assertEqual(True, self.distance.distance(np.array([[1, 2, 4]]), np.array([[1, 2, 3]]))-0.948<0.01)
        with self.assertRaises(WrongVecError):
            self.distance.distance(np.array([[]]), np.array([[1, 2, 3]]))          
        with self.assertRaises(TypeError):
            self.distance.distance([], np.array([[1, 2, 3]]))   
  
if __name__ == "__main__":  
    unittest.main()  