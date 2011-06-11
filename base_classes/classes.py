import string, glob, os, sys
from operator import itemgetter, attrgetter
from cugos_logging.irc_log_report.models import *

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
    def getLogView():
        distinct = Message.objects.values_list('channel', 'date').distinct().order_by('-date')
        indexAll = []    
        for chan, date in distinct: 
            logname = chan +"-"+ str(date) +".log" 
            indexAll.append(  BaseIndex(chan, str(date), logname, Message.objects.values_list('teller').filter(channel=chan).filter(date=str(date)).distinct().count(), Message.objects.filter(channel=chan).filter(date=str(date)).count())  ) 

        return indexAll
        

    @staticmethod 
    def sortBy(objects, property_sort):
        sorted_list = sorted(objects, key=attrgetter(property_sort)) 
        return sorted_list  
    
