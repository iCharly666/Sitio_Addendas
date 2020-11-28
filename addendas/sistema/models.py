from django.db import models
import os


# Create your models here.

class Add_xml(models.Model):
    file_xml = models.FileField(upload_to='xml_stored/')
    #def delete(self, *args, **kwargs):
    #    self.file_xml.delete()
    #    return super(Add_xml, self).delete(*args, **kwargs)
    
class Xml_Addenda(models.Model):
    file_addenda = models.FileField(upload_to='xml_addenda/')

