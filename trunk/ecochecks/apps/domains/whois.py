import sys 
import socket 
import re
 
PORT = 43 
DomainSearch = {
    'com':'whois.internic.net', 
    'net':'whois.internic.net', 
    'org':'whois.pir.org', 
    'nfo':'whois.afilias.info', 
    'biz':'whois.biz', 
    '.cc':'whois.nic.cc', 
    'edu':'rs.internic.net', 
    'mil':'whois.nic.mil', 
    'gov':'whois.nic.gov', 
    '.uk':'whois.nic.uk', 
    '.us':'whois.nic.us', 
    'ame':'whois.nic.name', 
    'eum':'whois.museum', 
    '.su':'whois.ripn.net', 
    '.ru':'whois.nic.ru', 
    'int':'whois.iana.org', 
    '.ws':'whois.worldsite.ws', 
    '.kr':'whois.krnic.net', 
    '.jp':'whois.nic.ad.jp', 
    '.it':'whois.nic.it', 
    '.de':'whois.denic.de', 
    '.fr':'whois.nic.fr', 
    '.ca':'whois.cira.ca', 
    '.cn':'whois.cnnic.net.cn', 
    '.tw':'whois.twnic.net.tw', 
    '.hk':'whois.hkdnr.net.hk', 
    '.au':'whois.aunic.net', 
    '.ac':'whois.nic.ac', 
    'DEF':'whois.verisign-grs.com'
    } 
 
fulldomain = sys.argv[1] 
if fulldomain.startswith('www.'): 
    fulldomain = fulldomain[4:] 
domain = fulldomain[-3:] 
print 'Domain: ', fulldomain   
if not DomainSearch.get(domain): 
    whoisserver = DomainSearch['DEF'] 
else: 
    whoisserver = DomainSearch[domain] 
print whoisserver 
try:             
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((whoisserver, PORT)) 
    s.send(fulldomain+"\r\n") 
    response = '' 
    while True: 
        data = s.recv(4096) 
        response += data 
        if data == '': 
            break 
    s.close()   
    infomation = response.lower() 
    try: 
        print infomation     
        domain_name = re.findall('domain name:\s?(.+)', infomation)
        print domain_name
        registrar = re.findall('registrar:\s?(.+)', infomation)
        print registrar
        whois_server = re.findall('whois server:\s?(.+)', infomation)
        print whois_server
        referral_url = re.findall('referral url:\s?(.+)', infomation)
        print referral_url
        name_server = re.findall('name server:\s?(.+)', infomation)
        print name_server  
        status = re.findall('status:\s?(.+)', infomation)
        print status
        updated_date = re.findall('updated date:\s?(.+)', infomation)
        print updated_date
        creation_date = re.findall('creation date:\s?(.+)', infomation)
        print creation_date
        expiration_date = re.findall('expiration date:\s?(.+)', infomation)
        print expiration_date
        email = re.findall('[\w.-]+@[\w.-]+\.[\w]{2,4}', infomation)
        print email
    except: 
        print  'unknown'  
except: 
    print 'time out'
