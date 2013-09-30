#! /usr/bin/env python
#-*- coding: utf-8 -*-

from distance.pearson_distance import PearsonDistance
import numpy as np

class UserSimilar():
  """
  Handle user's similar
      
  use-item matrix to compute user's similar for user-cf algorithm, the distance used to compute user's distance is pearson distance.
  (this is "An Algorithmic Framework for Performing Collaborative Filtering. et al.1999" by Herlocker, pearson distance perform better than cosin distance in user-cf, 
  more detail is described in "Empirical analysis of predictive algorithms for collaborative filtering. et al.1998", by Breese)
  
  Attributes:
  _matrix: the user-item matrix contain the score by user, an instance of recsys.utils.sparse_matrix.DictMatrix.
  """ 
  
  def __init__(self, matrix):
    """
    init method
        
    Args:
        matrix: the user-item matrix contain the score by user. 
                        matrix is an instance of recsys.utils.sparse_matrix.DictMatrix.
                        if you make sure matrix's index i and j is continuous from 0, the compute speed while be fast. 
    """        
    self._matrix = matrix
  
  def edit_score(self, user, item, value):
    """
    init method
        
    Args:
        user: the user index
        item: the item index
        value: the value
    """   
    self._matrix[user][item] = value
  
  def compute(self, u1, u2):
    """
    compute user's distance
        
    Args:
        u1: user index 1
        u2: user index 2
    
    Returns:
        the similarity of two user
    """         
    d1, d2, v1, v2 = (self._matrix[u1, ...], self._matrix[u2, ...], [], [])
    for i in range(max(max(d1.keys()), max(d2.keys()))+1):
      try:
        v1.append(d1[i])
      except:
        v1.append(0)
      try:
        v2.append(d2[i])
      except:
        v2.append(0)
    return PearsonDistance().distance(np.array([v1]), np.array([v2]))
  