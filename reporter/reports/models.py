from django.db import models

# Create your models here.

BASIC_PROPERTY_LABELS = [
    ('', 'UnSet Property'),
    ('A', 'An example'),
    ('C', 'Commerical'),
    ('FM', 'Farmers Market'),
    ('P', 'Parking'),
    ('E', 'Random prop'),
    ('ZZ', 'Another random Prop'),
]


class Test(models.Model):
    name = models.CharField(max_length=250)
    # creation_time = models.DateTimeField()
    # created_on = models.FloatField()
    data = models.CharField(max_length=30, null=True)
    data_two = models.DecimalField(max_digits=19, decimal_places=9, null=True)
    data_three = models.DecimalField(
        max_digits=19, decimal_places=9, null=True)
    proper = models.CharField(
        max_length=2,
        choices=BASIC_PROPERTY_LABELS,
        null=True
    )

    def __str__(self):
        return self.name


class TestNumbers(models.Model):
    data_one = models.IntegerField()
    data_two = models.IntegerField()

    def __str__(self):
        return str(self.data_one) + " " + str(self.data_two)


class TestText(models.Model):
    data_one = models.CharField(max_length=30)
    data_two = models.CharField(max_length=30)

    def __str__(self):
        return self.data_one + " " + self.data_two
