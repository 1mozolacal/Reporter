from django.db import models

# Create your models here.


class Test(models.Model):
    name = models.CharField(max_length=50)
    # creation_time = models.DateTimeField()
    # created_on = models.FloatField()
    data = models.CharField(max_length=250)
    def __str__(self):
        return self.name

