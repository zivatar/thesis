from datetime import datetime

from django.db import models


class UnprocessedData(models.Model):

    EXPIRATION_TIME_IN_SEC = 60

    site_id = models.ForeignKey('climate.Site')
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    uploaded_at = models.DateTimeField()

    @property
    def is_expired(self):
        return (self.uploaded_at - datetime.now()).seconds >= UnprocessedData.EXPIRATION_TIME_IN_SEC


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
