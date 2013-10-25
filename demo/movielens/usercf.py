#! /usr/bin/env python
#-*- coding: utf-8 -*-

#算过user的两两相似度的话就存起来，每个user存5倍的topN个数

from recsys.utils.sparse_matrix import DictMatrix
from recsys.algorithm.usercf import UserCF
import bsddb
import sys
import os

def load_data(basepath):
    filename_user_movie = basepath+'/data/movielens/ua.base'
    db = bsddb.btopen(None, cachesize = 268435456)
    matrix = DictMatrix(943, 2000, db)        
    with open(filename_user_movie) as fp:
        for line in fp:  
            userId, itemId, rating, timestamp = map(float, line.strip().split('\t'))  
            matrix[int(userId), int(itemId)] = float(rating)    
    return matrix 

if __name__ == "__main__":
    print "build the matrix..."
    path = os.path.dirname(sys.argv[0])    
    matrix  = load_data(path)
    ucf = UserCF(matrix)
    testfile = path + "/data/movielens/ua.test"
    
    print "start prediction by default usercf..."
    with open(testfile)  as fp:
        total = 0.0
        total_count = 0.0        
        for line in fp:
            userId, itemId, rating, timestamp = map(float, line.strip().split('\t'))  
            predict = ucf.prediction(int(userId), int(itemId))
            if predict > 5:
                predict = 5.0
            elif predict<1:
                predict = 1.0
            #print predict, rating
            total += (predict - rating) ** 2
            total_count += 1
        rmse = (total/total_count)**0.5
        print "rmse:", rmse    #1.2140
 
    ucf = UserCF(matrix, UserCF.HERLOCKER_USER_SIMILAR)   
    print "start prediction by herlocker usercf..."
    with open(testfile)  as fp:
        total = 0.0
        total_count = 0.0        
        for line in fp:
            userId, itemId, rating, timestamp = map(float, line.strip().split('\t'))  
            predict = ucf.prediction(int(userId), int(itemId))
            if predict > 5:
                predict = 5.0
            elif predict<1:
                predict = 1.0
            #print predict, rating
            total += (predict - rating) ** 2
            total_count += 1
        rmse = (total/total_count)**0.5
        print "rmse:", rmse     #1.2108
   