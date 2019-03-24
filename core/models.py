from djongo import models


class AppsAppleStore(models.Model):
    """
    'id', 'track_name', 'n_citacoes', 'size_bytes', 'price', 'prime_genre'

    """
    track_name = models.CharField(max_length=150)
    n_citacoes = models.IntegerField()
    size_bytes = models.IntegerField()
    price = models.FloatField()
    prime_genre = models.CharField(max_length=50)

    def __str__(self):
        return self.track_name


class CsvFile(models.Model):
    name = models.CharField(max_length=150)
    file_csv = models.FileField()