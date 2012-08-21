#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="ssnair"
__date__ ="$04 Nov, 2010 11:33:56 AM$"

import urllib
import libxml2
from django.conf import settings
WIHT_API_KEY = settings.WIHT_API_KEY

def __request(domain):
    url = 'http://api.whoishostingthis.com/?key=%s&domain=%s' % (WIHT_API_KEY, domain)
    return urllib.urlopen(url).read().strip()

def who_hosted_this(domain):
    xml_response =  __request(domain)
    hosted_by = None
    try:
        doc = libxml2.parseDoc(xml_response)
        ctxt = doc.xpathNewContext()
        result = ctxt.xpathEval("//HostingCompany")
        for node in result:
         hosted_by = node.content
    except:
        print 'XML parsing error.'
    return hosted_by