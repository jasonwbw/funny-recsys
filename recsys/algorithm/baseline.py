#! /usr/bin/env python
#-*- coding: utf-8 -*-

from usercf import UserCF

class Baseline(UserCF):
  """
  Use user-cf algorithm to recommend
  
  Attributes:
  _matrix: the user-item matrix contain the score by user, an instance of recsys.utils.sparse_matrix.DictMatrix.
  _user_similar: instance of UserSimilar
  """ 
  
  def prediction(self, user, item):
    """
    get prediction of user-item pair by user-cf
    prediciton(a, p) = avg_a + sum( sim(a,b) * (r(b,p) - avg_b) / sum(sim(a,b))
        
    Args:
        user: user index
        item: item index
    """          
    return self._userAverage(user)