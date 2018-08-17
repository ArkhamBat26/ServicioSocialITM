# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class FaceRecognizer(models.Model):
	sample1 = models.FileField(upload_to='samples')
	sample2 = models.FileField(upload_to='samples')
	sample3 = models.FileField(upload_to='samples')
	sample4 = models.FileField(upload_to='samples')
	sample5 = models.FileField(upload_to='samples')