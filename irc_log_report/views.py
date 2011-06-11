from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings
import string,os,sys,glob,time,logging
# imports relative to irc_log_reports proper
from cugos_logging.irc_log_report.models import *
from cugos_logging.base_classes.classes import *


def index_page(request, xarg=None):
    if request.method == 'POST':
        logging.info("POST request against sort_threads()")
        #return HttpResponseRedirect(settings.ROOT_RELATIVE_URL+'find/?search='+search)
    else:
        order = request.GET.get('order','desc')
    
    # get a distinct list of dates and channels
    distinct = Message.objects.values_list('channel', 'date').distinct().order_by('-date')
    indexAll = []    
    for chan, date in distinct: 
        logname = chan +"-"+ str(date) +".log" 
        indexAll.append(  BaseIndex(chan, str(date), logname, Message.objects.values_list('teller').filter(channel=chan).filter(date=str(date)).distinct().count(), Message.objects.filter(channel=chan).filter(date=str(date)).count())  ) 
           
    indexSorted = BaseIndex.sortBy(indexAll, "logname")                      
    if order != 'asc': indexSorted.reverse()

    return render_to_response('index_content.html',
                              {
                                'records' : indexSorted,
                                'root': settings.ROOT_URL,
                                'order': order,
                              },
                              context_instance=RequestContext(request))


def sort_threads(request, xarg=None):
    if request.method == 'POST':
        logging.info("POST request against sort_threads()")
        #return HttpResponseRedirect(settings.ROOT_RELATIVE_URL+'find/?search='+search)
    else:
        order = request.GET.get('order','asc')
        logging.info("GET request against take_dump")

    # get a distinct list of dates and channels
    distinct = Message.objects.values_list('channel', 'date').distinct().order_by('-date')
    indexAll = []    
    for chan, date in distinct: 
        logname = chan +"-"+ str(date) +".log" 
        indexAll.append(  BaseIndex(chan, str(date), logname, Message.objects.values_list('teller').filter(channel=chan).filter(date=str(date)).distinct().count(), Message.objects.filter(channel=chan).filter(date=str(date)).count())  ) 

    indexSorted = BaseIndex.sortBy(indexAll, "numThreads")                      
    if order != 'asc': indexSorted.reverse()

    return render_to_response('index_content.html',
                              {
                                'records' : indexSorted,
                                'root': settings.ROOT_URL,
                                'order': order,
                              },
                              context_instance=RequestContext(request))


def sort_tellers(request, xarg=None):
    if request.method == 'POST':
        logging.info("POST request against sort_threads()")
        #return HttpResponseRedirect(settings.ROOT_RELATIVE_URL+'find/?search='+search)
    else:
        order = request.GET.get('order','asc')

    # get a distinct list of dates and channels
    distinct = Message.objects.values_list('channel', 'date').distinct().order_by('-date')
    indexall = []    
    for chan, date in distinct: 
        logname = chan +"-"+ str(date) +".log" 
        indexall.append(  BaseIndex(chan, str(date), logname, Message.objects.values_list('teller').filter(channel=chan).filter(date=str(date)).distinct().count(), Message.objects.filter(channel=chan).filter(date=str(date)).count())  ) 
                           
    indexsorted = BaseIndex.sortBy(indexall, "numTellers")                      
    if order != 'asc': indexsorted.reverse()

    return render_to_response('index_content.html',
                              {
                                'records' : indexsorted,
                                'root': settings.ROOT_URL,
                                'order': order,
                              },
                              context_instance=RequestContext(request))


def take_dump(request, chan=None, YEAR=None, MONTH=None, DAY=None):

    if request.method == 'POST':
        logging.info("POST request against take_dump")
        #return HttpResponseRedirect(settings.ROOT_RELATIVE_URL+'find/?search='+search)
    else:
        #searchdate = request.GET.get('date','')
        logging.info("GET request against take_dump")
        
    # get the messages we need 
    messages = Message.objects.filter(date=YEAR+"-"+MONTH+"-"+DAY).filter(channel=chan).order_by('time')
    recordsList = []
    key = None
    for mes in messages:
        # strip out some bad characters
        irc_message = str(mes.message).replace('\x01','')
        recordsList.append ({ 'time': str(mes.time),
                             'chan' : str(mes.channel),
                             'teller' : str(mes.teller),
                             'message' : irc_message})

        key = mes.channel + "-" + str(mes.date) + ".log"
    
    return render_to_response('log_view.html',
                              {
                                'messages' : recordsList,
                                'key' : key,
                              },
                              context_instance=RequestContext(request))


