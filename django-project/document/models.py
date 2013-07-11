from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=300)
    content = models.TextField()
    uploaded_date = models.DateTimeField()
    #Files will be saved at media/documents/"uploaded year"/"uploaded month"/"uploaded day"/file
    file = models.FileField(upload_to="documents/%Y/%m/%d")