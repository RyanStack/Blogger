from django.db import models
from django.core.urlresolvers import reverse

class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    created_date = models.DateTimeField('created date')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
            return reverse('blog:list')


