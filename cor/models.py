from django.db import models
from django.contrib.auth.models import User

class WordOfTheDay(models.Model):
	word = models.CharField(max_length = 30)

	def __str__(self):
		return self.word


class AllFields(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	earning = models.IntegerField(max_length = 10, default = 0)
	pulls = models.IntegerField(max_length = 6, default = 0)
	lettersfound = models.CharField(max_length = 30, default = "Null")

class Pool(models.Model):
	moneypooled = models.IntegerField(max_length = 10, default = 0)