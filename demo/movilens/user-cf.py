#! /usr/bin/env python
#-*- coding: utf-8 -*-

from recsys.utils.sparse_matrix import DictMatrix

def load_data():
    file_user_movie = 'data/movielends/u.data'
    db = bsddb.btopen(None, cachesize = 268435456)
    matrix = DictMatrix(10, 10, db)        
    with open(filename_user_movie) as fp:
        for line in fp:  
            (userId, itemId, rating, timestamp) = line.strip().split('\t')  
            matrix[userId, itemId] = float(rating)    
    
    return matrix 

if __name__ == "__main__":
    load_data()