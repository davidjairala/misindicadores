from django.db import models
# Para usar users
from django.contrib.auth.models import User

class Cuenta(models.Model):
	user = models.ForeignKey(User)
	avatar = models.CharField(max_length = 200)
	
	# Vista de unicode
	def __unicode__(self):
		return self.avatar