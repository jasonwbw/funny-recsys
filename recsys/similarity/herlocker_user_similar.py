#! /usr/bin/env python
#-*- coding: utf-8 -*-

from user_similar import UserSimilar

class HerlockerUserSimilar(UserSimilar):
    '''
    Explicitly inherits from another class already.
    
    based on Herlocker's "An Algorithmic Framework for Performing Collaborative Filtering. et al.1999"
    '''
    
    def _getComputeWeight(self, u1, u2):  
        weight = 0.0
        for i in range(len(u1)): 
            if u1[i] == u2[i] and u1[i] <> 0 : weight+=1
        return weight>=50 and 1 or weight/50 