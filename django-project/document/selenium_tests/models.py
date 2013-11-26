from django.db import models


class Document(models.Model):
    law_name = models.CharField(max_length=300)
    article = models.TextField()