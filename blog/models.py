from django.db import models

class Entry(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    pub_date = models.DateTimeField("date_published")
    author = models.CharField(max_length=50)
    content = models.TextField()
    def __str__(self):
        return self.title

# Create your models here.
