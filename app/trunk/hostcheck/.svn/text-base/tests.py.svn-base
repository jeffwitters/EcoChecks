
from django import test

from hostcheck.views import *



class DomainNameParserTest(test.TestCase):
    def testParseFunnyTLD(self):
        funny_tld = "www.something.co.uk"
        elements = parse_domain_name(funny_tld)

        correct_parse = [ "www.something.co.uk", "something.co.uk", "co.uk" ]        

        self.assertEquals(correct_parse, elements)

    def testParseSingleDomain(self):
        domain = "something.com"
        
        elements = parse_domain_name(domain)
        
        self.assertEquals([domain], elements)

    def testParseDegenerateDomain(self):
        domain = "com"
        
        elements = parse_domain_name(domain)

        self.assertEquals([domain], elements)


    def testMultipleSubdomains(self):
        domain = "one.www-two.something.com"

        elements = parse_domain_name(domain)

        self.assertEquals([domain, "www-two.something.com", "something.com"],
            elements)

