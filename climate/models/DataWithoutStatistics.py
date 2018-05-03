from datetime import datetime

from django.db import models


class DataWithoutStatistics(models.Model):

    EXPIRATION_TIME_IN_SEC = 60

    siteId = models.ForeignKey('climate.Site')
    fromYear = models.IntegerField()
    fromMonth = models.IntegerField()
    toYear = models.IntegerField()
    toMonth = models.IntegerField()
    uploadedAt = models.DateTimeField()

    @property
    def is_expired(self):
        return (self.uploadedAt - datetime.now()).seconds >= DataWithoutStatistics.EXPIRATION_TIME_IN_SEC


"""
DataWithoutStatistics
siteId | fromYear | fromMonth | toYear | toMonth | uploadedAt

amikor az adatatfeltöltős REST API endpointra érkezik adat:
- elindítjuk az adatok bevitelét
- bevisszük ebbe az ideiglenes táblába az adatokat
- ellenőrzés 1 perces timeout múlva:
    - ha van olyan siteId, amelyikre a legfrissebb adat régebbi mint 1 perc:
    - kiszámoljuk a lefedett időszak kezdetét, végét
        - statisztikát számoltatunk rá
        - kiszedjük a táblából az elemeit
    - ha maradt még elem a táblában:
        - újabb ellenőrzés 1 perces timeout múlva
"""
