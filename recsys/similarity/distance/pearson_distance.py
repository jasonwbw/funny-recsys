#! /usr/bin/env python
#-*- coding: utf-8 -*-

from distance import Distance
from math import sqrt
import numpy as np
import numpy.linalg as linalg

class PearsonDistance(Distance):
  """
  pearson distance
      
  a sub class of Distance
  
  Attributes:
  """  

  def distance(self, vec1, vec2):
    """
        Compute distance of two vector by pearson distance
        more information view father class recsys.similarity.distance.distance.Distance
    """
    super(PearsonDistance, self).distance(vec1, vec2)      #super method
    avg1 = self.__avg(vec1)
    avg2 = self.__avg(vec2)
    v1 = [item - avg1 for item in vec1[0]]
    v2 = [item - avg1 for item in vec2[0]]
    return reduce(lambda n,m:n+m, [i*j for i,j in zip(v1, v2)]) \
           / sqrt(sum([pow(item, 2) for item in v1])) \
           / sqrt(sum([pow(item, 2) for item in v2]))
  
  def __avg(self, vec):
    """
        Compute average of a vector
        
        Args:
            vec: a line vector, an instance of array
          
        Returns:
            the average of the vector
        
        Raises:
    """    
    if vec.size == 0:
      return 0
    return vec.sum()/vec.size