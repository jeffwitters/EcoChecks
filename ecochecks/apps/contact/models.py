from django.db import models


class ContactText(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    class Meta:
        verbose_name = "Contact Text"
        verbose_name_plural = "Contact Texts"
        
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()