#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="anish"
__date__ ="$25 Oct, 2010 11:33:56 AM$"

import urllib
from lxml import etree
from django.conf import settings
WIHT_API_KEY = settings.WIHT_API_KEY

def __request(domain):
    url = 'http://api.whoishostingthis.com/?key=%s&domain=%s' % (WIHT_API_KEY, domain)
    return urllib.urlopen(url).read().strip()

def who_hosted_this(domain):
    xml_response =  __request(domain)
    hosted_by = None
    try:
	doc = etree.XML(xml_response.strip())
	hosted_by = doc.findtext('HostingCompany')
    except etree.XMLSyntaxError:
	print 'XML parsing error.'
    return hosted_by