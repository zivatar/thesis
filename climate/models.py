from django.db import models
from django.utils import timezone

NARROW_AREA = (
	(1, 'kert'),
	(2, 'parkoló'),
)

WIDE_AREA = (
	(1, 'belváros'),
	(2, 'kertváros'),
	(3, 'lakótelep'),
)

class Site(models.Model):
	id = models.AutoField(primary_key = True)
	owner = models.ForeignKey('auth.user')
	title = models.CharField(max_length = 100, unique = True)
	comment = models.TextField(blank = True)
	createdDate = models.DateTimeField(default = timezone.now)
	isActive = models.BooleanField(default = True)
	isPublic = models.BooleanField(default = True)
	lat = models.DecimalField(max_digits = 20, decimal_places = 15)
	lon = models.DecimalField(max_digits = 20, decimal_places = 15)
	narrowArea = models.IntegerField(choices = NARROW_AREA, default = 1)
	wideArea = models.IntegerField(choices = WIDE_AREA, default = 1) # site.wideArea; site.get_wideArea_display() https://docs.djangoproject.com/en/1.9/topics/db/models/#field-options
	
	def __str__(self):
		return self.title

	def publish(self):
		self.save()