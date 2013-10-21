import struct
import numpy as np
import bsddb
from cStringIO import StringIO
 
class DictMatrix():
    '''
    Sparse Matrix
    
    this class is a sparse way to contain a matrix, so you should make sure sparse is suiteable for you situation first.
    The follow reason explain why we don't use scipy.sparse package:
        1. we can't use the data[i, ...] and data[..., j] at the same time.
        2. as the data save in memory, so the data can't be too large.
    But if you face with the follow problem, scipy is prefer 
        1. you use the matrix to compute together rather than store
        2. you just have the require to get data[i, ...] or data[..., j] and the memory is sufficient, scipy may be prefer
    
    We use a dictory like storage to build dict['i123'], dict['j123'] (123 is an example of index number)
    
    Attributes:
        _data: the dictionary container, can be normal dictionary or some key-value database like berkeley db
        _dft: default value
        _nums: total nums in the matrix
    
    Reference:
        http://www.fuchaoqun.com/2010/03/python-sparse-matrix/
    '''
    
    def __init__(self, row_num, column_num, container = {}, dft = 0.0):
        self._data  = container
        self._dft   = dft
        self._nums  = 0
        self._row_num= row_num
        self._column_num = column_num
 
    def __setitem__(self, index, value):
        try:
            i, j = index
        except:
            raise IndexError('invalid index')
 
        ik = ('i%d' % i)
        # build j and value to a binary string for saving memory
        ib = struct.pack('if', j, value)
        jk = ('j%d' % j)
        jb = struct.pack('if', i, value)
 
        try:
            self._data[ik] += ib
        except:
            self._data[ik] = ib
        try:
            self._data[jk] += jb
        except:
            self._data[jk] = jb
        self._nums += 1
 
    def __getitem__(self, index):
        try:
            i, j = index
        except:
            raise IndexError('invalid index')
 
        if (isinstance(i, int)):
            ik = ('i%d' % i)
            if not self._data.has_key(ik): return self._dft
            ret = dict(np.fromstring(self._data[ik], dtype = 'i4,f4'))
            if (isinstance(j, int)): return ret.get(j, self._dft)
 
        if (isinstance(j, int)):
            jk = ('j%d' % j)
            if not self._data.has_key(jk): return self._dft
            ret = dict(np.fromstring(self._data[jk], dtype = 'i4,f4'))
 
        return ret
 
    def __len__(self):
        return self._nums
 
    def __iter__(self):
        pass

    def column_count(self):
        """
        the matrix's column count
        
        Returns:
            the matrix's column count
        """    
        return self._column_num
    
    def row_count(self):
        """
        the matrix's row count
        
        Returns:
            the matrix's row count
        """    
        return self._row_num 
 
    def from_file(self, fp, sep = '\t'):
        '''
        Build matrix from file
        
        one line in file is "i sep j sep value"
        as dbm is slower than memory, we build a cache to write back per 1000W line
        as the combine of string is too slow, we use StringIO to combine
        
        Args:
            fp: input file instance
            sep: separator in one line
        '''        
        cnt = 0
        cache = {}
        for l in fp:
            if 10000000 == cnt:
                self._flush(cache)
                cnt = 0
                cache = {}
            i, j, v = [float(i) for i in l.split(sep)]
 
            ik = ('i%d' % i)
            ib = struct.pack('if', j, v)
            jk = ('j%d' % j)
            jb = struct.pack('if', i, v)
 
            try:
                cache[ik].write(ib)
            except:
                cache[ik] = StringIO()
                cache[ik].write(ib)
 
            try:
                cache[jk].write(jb)
            except:
                cache[jk] = StringIO()
                cache[jk].write(jb)
 
            cnt += 1
            self._nums += 1
 
        self._flush(cache)
        return self._nums
 
    def _flush(self, cache):
        '''
        write cache back to data.
        
        Args:
            cache: memory cache, an instance of dictionary
        '''
        for k,v in cache.items():
            v.seek(0)
            s = v.read()
            try:
                self._data[k] += s
            except:
                self._data[k] = s
 
if __name__ == '__main__':
    db = bsddb.btopen(None, cachesize = 268435456)
    data = DictMatrix(2, 2, db)
    #data.from_file(open('/path/to/log.txt', 'r'), ',')
    data[0,1] = 1
    data[0,1] = 2
    data[1,1] = 1
    print data[..., 1]
    print data[0, 1]
    print data[2, ...]
    print data[0, 0]