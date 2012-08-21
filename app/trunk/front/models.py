
from django.conf import settings
from django.utils.hashcompat import sha_constructor
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator

class NewsItem(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=250)
    link = models.CharField(max_length=500)
    
    published = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    published_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('text', 'published', 'created_on', 'published_on')
    
    def __unicode__(self):
        return self.text

class Signup(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    created_on = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField()

    class Meta:
        ordering = ('email', 'name', 'ip_address', 'created_on')
    
    def __unicode__(self):
        return "%s <%s>" % (self.name, self.email)


from datetime import date

class RegistrationTokenGenerator(object):
    def make_code(self, user):
        """Hash should be unique since it uses the user id and password"""
        hash = sha_constructor(settings.SECRET_KEY + unicode(user.id) +
            user.password + unicode(date.today())).hexdigest()[::2]
        
        return hash


class RegistrationTokenManager(models.Manager):
    def create_token(self, user):
        registration_token = RegistrationToken(user=user,
            code=RegistrationTokenGenerator().make_code(user))
        registration_token.save()

        return registration_token 

class RegistrationToken(models.Model):
    user = models.ForeignKey(User, unique=True)
    code = models.CharField(max_length=50, unique=True)

    claimed = models.BooleanField(default=False)    

    created_on = models.DateTimeField(auto_now_add=True)
    claimed_on = models.DateTimeField(null=True, blank=True)

    objects = RegistrationTokenManager()

    class Meta:
        ordering = ('user', 'code', 'created_on', 'claimed_on')

    def __unicode__(self):  
        return "%s <%s>" % (self.code, self.user)


class Feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    
    created_on = models.DateTimeField(auto_now_add=True)
    sender_ip = models.IPAddressField()

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    activated = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    activated_on = models.DateTimeField(null=True, blank=True)


class SubscriptionTokenGenerator(object):
    def make_code(self, subscription):
        """Hash should be unique since it uses the user id and password"""
        hash = sha_constructor(settings.SECRET_KEY + unicode(subscription.id) +
            subscription.email + unicode(date.today())).hexdigest()[::2]

        return hash

class NewsletterSignupRequestManager(models.Manager):
    def create_request(self, newsletter_subscription, request_ip):
        request = NewsletterSignupRequest(newsletter_subscription=newsletter_subscription,
            request_ip=request_ip, code=SubscriptionTokenGenerator().make_code(newsletter_subscription))
        
        request.save()
        
        return request

class NewsletterSignupRequest(models.Model):
    newsletter_subscription = models.ForeignKey(NewsletterSubscription)
    request_ip = models.IPAddressField()
    code = models.CharField(max_length=50, unique=True)
    
    sent_on = models.DateTimeField(null=True, blank=True)
    
    objects = NewsletterSignupRequestManager()


