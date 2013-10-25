#! /usr/bin/env python
#-*- coding: utf-8 -*-

from distance.pearson_distance import PearsonDistance
import numpy as np
import bsddb
from recsys.utils.sparse_matrix import DictMatrix

class UserSimilar():
  """
  Handle user's similar
      
  use-item matrix to compute user's similar for user-cf algorithm, the distance used to compute user's distance is pearson distance.
  (this is "An Algorithmic Framework for Performing Collaborative Filtering. et al.1999" by Herlocker, pearson distance perform better than cosin distance in user-cf, 
  more detail for different preformance between pearson and cosine is described in "Empirical analysis of predictive algorithms for collaborative filtering. et al.1998", by Breese)
  
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
    db = bsddb.btopen(None, cachesize = 268435456)     
    self._similar = DictMatrix(matrix.row_count(), matrix.row_count(), db, -1)     
  
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
    if self._similar[u1, u2] <> -1:
      return self._similar[u1, u2]
    
    d1, d2, v1, v2 = (self._matrix[u1, ...], self._matrix[u2, ...], [], [])
    if d1 == 0 or d2 == 0:
      return 0
    for i in range(1, max(max(d1.keys()), max(d2.keys()))+1):
      try:
        v1.append(d1[i])
      except:
        v1.append(0)
      try:
        v2.append(d2[i])
      except:
        v2.append(0)
    self._similar[u1, u2] = self._getComputeWeight(v1, v2) * PearsonDistance().distance(np.array([v1]), np.array([v2]))
    return self._similar[u1, u2]
  
  def _getComputeWeight(self, u1, u2):  
    """
    get weight while compute distance of u1 and u2
        
    Args:
        u1: user vector
        u2: user vector
    
    Returns:
        the weight
    """      
    return 1
  
  def topN(self, user, item, n=35):
    """
    compute the topN user rated item
        
    Args:
        user: user index
        item: item index
        n: n default 35 based on 
            "An empirical analysis of design choices in neighborhood-based collaborative filtering algorithms. et al.2002"
            20-50 perfrom better on movielen
    
    Returns:
        topN similar user list
    """
    top = []    # use list of size n to sort the suitable user
    for u in range(1, self._matrix.row_count()+1):
      if u == user or self._matrix[u, item] == 0:
        continue
      dis = self.compute(u, user)
      if dis <= 0:
        continue
      top_len = len(top)
      for i in range(top_len):
        if top[i][1] < dis or (i == top_len - 1 and top_len<n):
          top.insert(i, (u, dis))
          if len(top) > n:
            top.pop()
          break
      if top_len == 0:
        top.append((u, dis))
    return top
  
  def testTopNNoWeight(self, user, item, n=35):
    return [i[0] for i in self.topN(user, item, n)]   