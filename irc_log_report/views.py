from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings
import string,os,sys,glob,time,logging,re
# imports relative to irc_log_reports proper
from cugos_logging.irc_log_report.models import *
from cugos_logging.base_classes.classes import *


def index_page(request, xarg=None):
    if request.method == 'POST':
        logging.info("POST request against index_page()")
        #return HttpResponseRedirect(settings.ROOT_RELATIVE_URL+'find/?search='+search)
    else:
        order = request.GET.get('order','desc')
    
    # get a distinct list of dates and channels
    indexAll = BaseIndex.getLogView()   

    # sort it by default as ascending order
    indexSorted = BaseIndex.sortBy(indexAll, "logname")                      
    
    # depending on arguments, sort opposite
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

    # get a distinct list of dates and channels
    indexAll = BaseIndex.getLogView()   
    
    # sort ascending by default
    indexSorted = BaseIndex.sortBy(indexAll, "numThreads")                      
    
    # sort in reverse if args ask
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
        logging.info("POST request against sort_tellers()")
        #return HttpResponseRedirect(settings.ROOT_RELATIVE_URL+'find/?search='+search)
    else:
        order = request.GET.get('order','asc')
                           
    # get a distinct list of dates and channels
    indexAll = BaseIndex.getLogView()   

    # sort asc by default
    indexsorted = BaseIndex.sortBy(indexAll, "numTellers")                      
    
    # sort in reverse if args say so
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

        # strip out bad characters and setup for italicized rendering 
        regex = re.compile(r'^\x01\*(?P<message>.*)\x01$')
        if regex.match(string.strip(str(mes.message))) != None:
            irc_message = "**"+str(mes.teller)+"**" + " " + (regex.match(string.strip(str(mes.message))).group('message'))
        else:
            irc_message = str(mes.message)

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


