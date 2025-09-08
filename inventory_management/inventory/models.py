from django.db import models
from django.contrib.auth.models import User


class InventoryItem(models.Model):
	name = models.CharField(max_length=200)
	quantity = models.IntegerField()
	date_created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	expiration_date = models.DateField(null=True, blank=True)
	serial_number = models.CharField(max_length=100, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	tags = models.ManyToManyField('Tag', blank=True)

	def __str__(self):
		return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name




class InventoryProveedor(models.Model):
	name_p = models.CharField(max_length=200)
	email_p = models.EmailField(max_length=254, null=True, blank=True)
	number_p = models.CharField(max_length=100, null=True, blank=True)
	description_p = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name_p