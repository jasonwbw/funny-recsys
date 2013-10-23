#! /usr/bin/env python
#-*- coding: utf-8 -*-

from recsys.utils.sparse_matrix import DictMatrix
from recsys.algorithm.usercf import UserCF
import bsddb
import sys
import os

def load_data(basepath):
    filename_user_movie = basepath+'/data/movielens/u.data'
    db = bsddb.btopen(None, cachesize = 268435456)
    matrix = DictMatrix(10, 10, db)        
    with open(filename_user_movie) as fp:
        for line in fp:  
            userId, itemId, rating, timestamp = map(float, line.strip().split('\t'))  
            matrix[userId, itemId] = float(rating)    
    return matrix 

if __name__ == "__main__":
    path = os.path.dirname(sys.argv[0])    
    matrix  = load_data(path)
    usercf = UserCF(matrix)