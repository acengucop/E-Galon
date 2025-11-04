from django.db import models

class Depot(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    stok_galon = models.IntegerField(default=0)

    def __str__(self):
        return self.nama
