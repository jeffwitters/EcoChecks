from datetime import date

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.hashcompat import sha_constructor
from django.utils.http import int_to_base36, base36_to_int

class HostingCompany(models.Model):
    name = models.CharField(max_length=250)

    url = models.CharField(max_length=250)

    # If the company has been checked to see if it's carbon neutral
    checked = models.BooleanField(default=False)
    
    # If the company is carbon neutral
    approved = models.BooleanField(default=False)
    

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    # The date the company was last checked for its carbon status
    checked_on = models.DateTimeField(blank=True, null=True)
    approved_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Hosting Companies'

    def __unicode__(self):
        return self.name


class DomainName(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, related_name='domain_names')
    hosting_company = models.ForeignKey(HostingCompany, related_name='domain_names')

    # The actual domain name of the site: 'www.rei.com', for example.
    name = models.CharField(max_length=250)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', 'created_on',)
    
    def __unicode__(self):
        return self.name

class ClaimTokenGenerator(object):
    def make_code(self, domain_name, user):
        timestamp = date.today()
        timestamp = (timestamp - date(2001, 1, 1)).days

        hash = sha_constructor(settings.SECRET_KEY + unicode(user.id) +
                domain_name.name + 
                user.password + unicode(user.last_login) + 
                unicode(timestamp)).hexdigest()[::2]
        ts_b36 = int_to_base36(timestamp)

        return "%s-%s" % (ts_b36, hash)
    
    def check_code(self, hash, domain_name, user):
        try:
            ts_b36, hash = hash.split("-")
        except ValueError:
            return False
        
        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        if self.make_code(domain_name, user) != hash:
            return False

        return True
    

class DomainClaimTokenManager(models.Manager):
    def create(self, domain_name, user):
        generator = ClaimTokenGenerator()
        code = generator.make_code(domain_name, user)
        token = DomainClaimToken(user=user, domain_name=domain_name,
            token=code)
    
        token.save()

        return token

class DomainClaimToken(models.Model):
    user = models.ForeignKey(User)
    # Domain name tokens are NOT unique 
    domain_name = models.ForeignKey(DomainName)
    token = models.CharField(max_length=50)
    
    claimed = models.BooleanField(default=False)    

    created_on = models.DateTimeField(auto_now_add=True)
    claimed_on = models.DateTimeField(blank=True, null=True)

    objects = DomainClaimTokenManager()
    
    class Meta:
        ordering = ('domain_name', 'user', 'token')

    def __unicode__(self):
        return "%s (%s)" % (self.token, self.domain_name)





