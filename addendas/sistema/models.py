from django.db import models

# Create your models here.

class Add_xml(models.Model):
    file_xml = models.FileField(upload_to='xml_stored/')