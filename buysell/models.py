from django.db import models

class Account(models.Model):
	firstName = models.CharField(max_length=200)
	lastName = models.CharField(max_length=200)
	username = models.CharField(max_length=200, primary_key=True)
	email = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	datecreated = models.DateTimeField('Date Created')

	def __str__(self):
		return self.username

class Sellpost(models.Model):
	publisher = models.ForeignKey(Account, on_delete=models.CASCADE)
	item = models.CharField(max_length=200)
	date_posted = models.DateTimeField('date published')
	description = models.CharField(max_length=255)
	amount = models.CharField(max_length=200)
	photo = models.FileField(upload_to='documents/')
	location = models.CharField(max_length=200)
	post_identifier = 'sell'

class Buypost(models.Model):
	publisher = models.ForeignKey(Account, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	price = models.CharField(max_length=200)
	location = models.CharField(max_length=200)
	date_posted = models.DateTimeField('Posted date')
	time_diff = models.IntegerField(default=0)
	post_identifier = 'buy'

class Sent(models.Model):
	publisher = models.ForeignKey(Account, on_delete=models.CASCADE)
	text = models.CharField(max_length=200)
	time = models.DateTimeField('time sent')
	message_identifier = "outbox"
	#user name of the person receiving the message
	name = models.CharField(max_length=200)
	post_identifier = models.IntegerField(blank=True)

class Received(models.Model):
	publisher = models.ForeignKey(Account, on_delete=models.CASCADE)
	text = models.CharField(max_length=200)
	time = models.DateTimeField('time sent')
	message_identifier = "inbox"
	#user name of the person who sent the message
	name = models.CharField(max_length=200)
	post_identifier = models.IntegerField(blank=True)