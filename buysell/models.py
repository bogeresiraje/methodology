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
	description = models.CharField(max_length=255)
	date_posted = models.DateTimeField('date published')
	amount = models.CharField(max_length=200)
	photo = models.FileField(upload_to='documents/')
	location = models.CharField(max_length=200)
	post_identifier = 'sell'

class Buypost(models.Model):
	publisher = models.ForeignKey(Account, on_delete=models.CASCADE)
	item = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	price = models.CharField(max_length=200)
	location = models.CharField(max_length=200)
	date_posted = models.DateTimeField('Posted date')
	post_identifier = 'buy'

class Sent(models.Model):
	publisher = models.ForeignKey(Account, on_delete=models.CASCADE)
	text = models.CharField(max_length=200)
	date_posted = models.DateTimeField('time sent')
	message_identifier = "outbox"
	#user name of the person receiving the message
	name = models.CharField(max_length=200)
	msg_identifier = 'sent'

class Received(models.Model):
	publisher = models.ForeignKey(Account, on_delete=models.CASCADE)
	text = models.CharField(max_length=200)
	date_posted = models.DateTimeField('time sent')
	message_identifier = "inbox"
	#user name of the person who sent the message
	name = models.CharField(max_length=200)
	msg_identifier = 'received'

class Followed(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	pub_time = models.DateTimeField("date added")

class Notifications(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	identifier = models.CharField(max_length=100)
	date_posted = models.DateTimeField('time notified')

class Sellcomment(models.Model):
	post = models.ForeignKey(Sellpost, on_delete=models.CASCADE)
	text = models.CharField(max_length=200)
	publisher = models.CharField(max_length=100, default='')
	date_posted = models.DateTimeField('date commented')

class Buycomment(models.Model):
	post = models.ForeignKey(Buypost, on_delete=models.CASCADE)
	text = models.CharField(max_length=200)
	publisher = models.CharField(max_length=100, default='')
	date_posted = models.DateTimeField('date commented')