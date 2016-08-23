from django.db import models
from django.core.urlresolvers import reverse



class List(models.Model):
  
    def get_absolute_url(self):
        '''
        instance.get_abuslute_url() and redurect(instance) will return url named vew_list
        '''
        return reverse('view_list', args=[self.id])

    
class Item(models.Model):
    text = models.TextField(default="",)
    list = models.ForeignKey(List, default=None)
    
    class Meta:
        ordering = ("id",)
        unique_together = ('list', 'text') 
        
    def __str__(self):
        return self.text
    
