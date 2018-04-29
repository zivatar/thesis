import os
from django.db import models


def get_image_path_site1(instance, filename):
    return os.path.join('uploads', 'site', str(instance.id))


class Site(models.Model):
    NARROW_AREA = (
        (1, 'kert'),
        (2, 'parkoló'),
        (3, 'tető'),
        (4, 'udvar'),
        (5, 'füves terület'),
        (6, 'fás terület'),
        (7, 'vízpart'),
        (8, 'utca')
    )

    WIDE_AREA = (
        (1, 'belváros'),
        (2, 'kertváros'),
        (3, 'lakótelep'),
        (4, 'ipari terület'),
        (5, 'hegyvidék'),
        (6, 'vízpart'),
        (7, 'külterület')
    )

    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.user')
    title = models.CharField(max_length=100, unique=True)
    comment = models.TextField(blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)
    isPublic = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)
    lat = models.DecimalField(max_digits=20, decimal_places=15)
    lon = models.DecimalField(max_digits=20, decimal_places=15)
    narrowArea = models.IntegerField(choices=NARROW_AREA, default=1)
    wideArea = models.IntegerField(choices=WIDE_AREA,
                                   default=1)
    primaryImage = models.ImageField(upload_to=get_image_path_site1, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_wide_area(self):
        find = [x[1] for x in Site.WIDE_AREA if x[0] == self.wideArea]
        if len(find) > 0:
            return find[0]

    def get_narrow_area(self):
        find = [x[1] for x in Site.NARROW_AREA if x[0] == self.narrowArea]
        if len(find) > 0:
            return find[0]
