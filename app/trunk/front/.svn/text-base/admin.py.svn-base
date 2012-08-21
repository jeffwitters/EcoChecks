from django.contrib import admin
from front.models import *


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ['text', 'published', 'published_on']

admin.site.register(NewsItem, NewsItemAdmin)

class SignupAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'ip_address', 'created_on']

admin.site.register(Signup, SignupAdmin) 

class RegistrationTokenAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'claimed', 'created_on', 'claimed_on']

admin.site.register(RegistrationToken, RegistrationTokenAdmin)

class FeedbackAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(Feedback, FeedbackAdmin)

class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    pass

admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)

class NewsletterSignupRequestAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(NewsletterSignupRequest, NewsletterSignupRequestAdmin)
