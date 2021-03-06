from datetime import datetime

from django.db import models


class UnprocessedData(models.Model):
    """
    | Temporary storage of arrived raw data
    | We wait a minute before process data
    | To make sure calculate statistics only when everything is inserted and to avoid race conditions
    """

    EXPIRATION_TIME_IN_SEC = 60

    site_id = models.ForeignKey('climate.Site', help_text='foreign key for Site table')
    from_date = models.DateTimeField(help_text='starting date of data pack')
    to_date = models.DateTimeField(help_text='finishing date of data pack')
    uploaded_at = models.DateTimeField(help_text='datetime of upload')

    @property
    def is_expired(self):
        """
        | Is this line old enough to calculate statistics

        :return: boolean
        """
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
