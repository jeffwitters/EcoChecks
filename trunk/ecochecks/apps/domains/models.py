from django.db import models
from django.contrib.auth.models import User
from hosts.models import Host

class Domain(models.Model):
    user = models.ForeignKey(User, null=True, related_name="domains")
    url = models.URLField()
    host = models.ForeignKey(Host)
    awarded_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField()
    badge_file_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.url

class Log(models.Model):
    url = models.URLField()
    host = models.CharField(max_length=50)
    whois = models.TextField(max_length=5000)
    ip = models.CharField(max_length=20)
    server = models.CharField(max_length=60)
    
    def __unicode__(self):
        return "%s - %s" % (self.url, self.host)
