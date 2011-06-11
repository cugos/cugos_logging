import string, glob, os, sys
from operator import itemgetter, attrgetter


class BaseIndex(object):

    def __init__(self, channel, date, logname, numTellers, numThreads):
        self.chan = channel
        self.date = date
        self.logname = logname
        self.numTellers = numTellers
        self.numThreads = numThreads
    
    #Override object.__rep__
    def __rep__(self):
        return [self.logname, self.numThreads, self.numTellers ]

    @staticmethod 
    def sortBy(objects, property_sort):
        sorted_list = sorted(objects, key=attrgetter(property_sort)) 
        return sorted_list  
    
