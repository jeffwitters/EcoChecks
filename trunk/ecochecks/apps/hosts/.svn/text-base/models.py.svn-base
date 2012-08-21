from django.db import models

class Host(models.Model):
    logo = models.ImageField(upload_to='hostlogo', blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    signup_url = models.URLField(blank=True, verify_exists=False)

    def __unicode__(self):
        return self.name