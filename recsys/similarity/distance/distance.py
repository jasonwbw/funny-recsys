#! /usr/bin/env python
#-*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from recsys.exception.error_wrongvec import WrongVecError
import numpy 

class Distance():
  """
    abstract class, represent distance of two vector
    
    Attributes:
    """    

  __metaclass__ = ABCMeta
         
  @abstractmethod
  def distance(self, vec1, vec2):
    """
    Compute distance of two vector(one line numpy array)
    if you use scipy to store the sparse matrix, please use s.getrow(line_num).toarray() build the one dimensional array
    
    Args:
        vec1: the first line vector, an instance of array
        vec2: the second line vector, an instance of array
      
    Returns:
        the computed distance
    
    Raises:
        TypeError: if vec1 or vec2 is not numpy.ndarray and one line array
    """
    if not isinstance(vec1, numpy.ndarray) or not isinstance(vec2, numpy.ndarray):
      raise TypeError("type of vec1 or vec2 is not numpy.ndarray")
    if vec1.shape[0] is not 1 or vec2.shape[0] is not 1:
      raise WrongVecError("vec1 or vec2 is not one line array")
    if vec1.size != vec2.size:
      raise WrongVecError("vec1 or vec2 is not same size")    
    pass
  