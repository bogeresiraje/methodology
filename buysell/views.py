from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Account, Sellpost, Buypost
from django.utils import timezone
import datetime
from operator import itemgetter

def index(request):
	return render(request, 'buysell/index.html')

def signup(request):
	return render(request, 'buysell/signup.html')

def confirm(request):
	empty_field = "This field can't be empty"
	errors = dict()

	first_name = request.POST['inputFirstName']
	if not first_name:
		errors['error_first_name'] = empty_field
		
	last_name = request.POST['inputLastName']
	if not last_name:
		errors['error_last_name'] = empty_field
		
	user_name = request.POST['inputUserName']
	if not user_name:
		errors['error_user_name'] = empty_field
		
	e_mail = request.POST['inputEmail']
	if not e_mail:
		errors['error_email'] = empty_field
		
	first_password = request.POST['inputPass']
	if not first_password:
		errors['error_first_password'] = empty_field
		
	second_password = request.POST['inputPassword']
	if not second_password:
		errors['error_second_password'] = empty_field

	if (first_name and last_name and user_name and e_mail and first_password and second_password):
		if first_password == second_password:
			account = Account(firstName=first_name, lastName=last_name, username=user_name, email=e_mail, 
				password=first_password, datecreated=timezone.now())
			account.save()
			user_name = account.username
			return HttpResponseRedirect(reverse('buysell:contin', args=(user_name,)))
		else:
			error_password = "Passwords don't match"
			return render(request, 'buysell/signup.html', {'error_password': error_password})
	else:
		return render(request, 'buysell/signup.html', {'errors': errors})

def contin(request, user_name):
	account = Account.objects.get(pk=user_name)
	return render(request, 'buysell/contin.html', {'account': account})

def login(request):
	empty_field = "This field cannot be empty"
	errors = dict()

	user_name = request.POST['inputUserName']
	if not user_name:
		errors['empty_user_name'] = empty_field

	pass_word = request.POST['passWord']
	if not pass_word:
		errors['empty_password'] = empty_field

	if user_name and pass_word:
		try:
			account = Account.objects.get(pk=user_name)
		except Account.DoesNotExist:
			error_message = "Incorrect User Name"
			return render(request, 'buysell/index.html', {'error_message': error_message})
		else:
			if pass_word == account.password:
				return HttpResponseRedirect(reverse('buysell:postfeed', args=(account.username,)))
			else:
				error_password = "Incorrect Password"
				return render(request, 'buysell/index.html', {'error_password': error_password})
	else:
		return render(request, 'buysell/index.html', {'errors': errors})

def postfeed(request, user_name):
	account = get_object_or_404(Account, pk=user_name)
	try:
		accounts = Account.objects.all()
	except Account.DoesNotExist:
		raise Http404("Account does not exist")

	all_posts = list()
	for acc in accounts:
		buy_posts = list(acc.buypost_set.all())
		sell_posts = list(acc.sellpost_set.all())
		all_posts.extend(buy_posts + sell_posts)

	date_post = [(all_post.date_posted, all_post) for all_post in all_posts]
	sorted_date_post = sorted(date_post, key=itemgetter(0), reverse=True)
	posts = [post[1] for post in sorted_date_post]
	return render(request, 'buysell/postfeed.html', {'account': account, 'posts': posts})

def sell(request, user_name):
	account = get_object_or_404(Account, pk=user_name)
	return render(request, 'buysell/sell.html', {'account': account})

def verify_post(request, user_name):
	account = get_object_or_404(Account, pk=user_name)
	empty_field = 'This field can\'t be empty'
	errors = dict()

	item_name = request.POST['itemName']
	if not item_name:
		errors['empty_name'] = empty_field
	item_description = request.POST['description']
	if not item_description:
		errors['empty_description'] = empty_field
	item_price = request.POST['price']
	if not item_price:
		errors['empty_price'] = empty_field
	current_location = request.POST['location']
	if not current_location:
		errors['empty_location'] = empty_field
	picture = request.FILES['photo']
	if not picture:
		errors['empty_pic'] = empty_field

	if (item_name and item_description and item_price and current_location and picture):
		account.sellpost_set.create(item=item_name, description=item_description, amount=item_price,
			location=current_location, photo=picture, date_posted=timezone.now(),
			)
		return HttpResponseRedirect(reverse('buysell:my_activity', args=(account.username,)))
	else:
		return render(request, 'buysell/sell.html', {'account': account, 'errors': errors})

def display_success(request):
	return HttpResponse("Keep moving on bro, you are on track")

def buy(request, user_name):
	account = get_object_or_404(Account, pk=user_name)
	try:
		accounts = Account.objects.all()
	except Account.DoesNotExist:
		raise Http404("Account does not exist")

	all_posts = list()
	for acc in accounts:
		buy_posts = list(acc.buypost_set.all())
		sell_posts = list(acc.sellpost_set.all())
		all_posts.extend(buy_posts + sell_posts)

	date_post = [(all_post.date_posted, all_post) for all_post in all_posts]
	sorted_date_post = sorted(date_post, key=itemgetter(0), reverse=True)
	posts = [post[1] for post in sorted_date_post]
	return render(request, 'buysell/buy.html', {'account': account, 'posts': posts})

def post_item_to_buy(request, user_name):
	account = get_object_or_404(Account, pk=user_name)

	empty_field = 'This field can\'t be empty'
	errors = dict()

	item_name = request.POST['itemName']
	if not item_name:
		errors['empty_name'] = empty_field
	item_description = request.POST['description']
	if not item_description:
		errors['empty_description'] = empty_field
	item_price = request.POST['price']
	if not item_price:
		errors['empty_price'] = empty_field
	current_location = request.POST['location']
	if not current_location:
		errors['empty_location'] = empty_field

	if (item_name and item_description and item_price and current_location):
		account.buypost_set.create(name=item_name, description=item_description, price=item_price,
			location=current_location, date_posted=timezone.now(),
			)
		return HttpResponseRedirect(reverse('buysell:my_activity', args=(account.username,)))
	else:
		return render(request, 'buysell/buy.html', {'errors': errors, 'account':account})

def my_activity(request, user_name):
	account = get_object_or_404(Account, pk=user_name)
	buy_posts = list(account.buypost_set.all())
	sell_posts = list(account.sellpost_set.all())
	my_posts = buy_posts + sell_posts
	date_post = [(my_post.date_posted, my_post) for my_post in my_posts]
	sorted_dates = sorted(date_post, key=itemgetter(0), reverse=True)
	posts = [post for (date,post) in sorted_dates]
	return render(request, 'buysell/activity.html', {'account': account, 'posts': posts})

def message_panel_from_post(request, user_name):
	account = get_object_or_404(Account, pk=user_name)

def write_message(request, user_name, post_id, post_identifier):
	my_account = Account.objects.get(pk=user_name)
	if post_identifier == 'sell':
		post = Sellpost.objects.get(pk=post_id)
	else:
		post = Buypost.objects.get(pk=post_id)
	return render(request, 'buysell/write_message.html', {'account': my_account, 'post': post})

def send_message(request, user_name, post_id, post_identifier):
	if post_identifier == 'sell':
		post_ = Sellpost.objects.get(pk=post_id)
	else:
		post_ = Buypost.objects.get(pk=post_id)
	message_ = request.POST['text_message']

	sender_account = Account.objects.get(pk=user_name)
	receiver_account = Account.objects.get(pk=post_.publisher.username)

	sender_account.sent_set.create(text=message_, time=timezone.now(), name=receiver_account.username,
		post_identifier=post_id)
	receiver_account.received_set.create(text=message_, time=timezone.now(), name=sender_account.username,
		post_identifier=post_id)

	return HttpResponseRedirect(reverse('buysell:messages', args=(sender_account.username,)))

def messages(request, user_name):
	account = get_object_or_404(Account, pk=user_name)
	try:
		accounts = Account.objects.all()
	except Account.DoesNotExist:
		raise Http404("Account does not exist")

	all_posts = list()
	for acc in accounts:
		buy_posts = list(acc.buypost_set.all())
		sell_posts = list(acc.sellpost_set.all())
		all_posts.extend(buy_posts + sell_posts)

	date_post = [(all_post.date_posted, all_post) for all_post in all_posts]
	sorted_date_post = sorted(date_post, key=itemgetter(0), reverse=True)
	posts = [post[1] for post in sorted_date_post]

	def gen_sorted_msg(input_message):
		msg_time = [ (message, message.time) for message in input_message]
		sorted_msg_time = sorted(msg_time, key=itemgetter(1), reverse=True)
		for message, time in sorted_msg_time:
			yield message

	def filter(raw_data):
		done = list()
		for message in raw_data:
			name = message.name
			if name not in done:
				done.append(name)
				yield message
			else:
				continue

	def gen_msg_list(sent, received):
		l = list()
		for message_sent in sent:
			for message_received in received:
				if message_sent.name == message_received.name:
					if message_sent.time > message_received.time:
						l.append(message_sent)
					else:
						l.append(message_received)
				else:
					l.extend((message_sent, message_received))
		return l

	sent_messages = account.sent_set.all()
	sorted_sent_msgs = gen_sorted_msg(sent_messages)
	filtered_sent_msgs = filter(sorted_sent_msgs)

	received_messages = account.received_set.all()
	sorted_received_msgs = gen_sorted_msg(received_messages)
	filtered_received_msgs = filter(sorted_received_msgs)

	unsorted_messages = gen_msg_list(filtered_sent_msgs, filtered_received_msgs)
	messages = list(filter(unsorted_messages))

	return render(request, 'buysell/messages.html', {'account': account, 'messages': messages, 'posts': posts})

def search(request, user_name):
	return render(request, 'buysell/search.html')

def most_followed(request, user_name):
	return render(request, 'buysell/most_followed.html')

def categories(request, user_name):
	return render(request, 'buysell/categories.html')

def my_account(request, user_name):
	return render(request, 'buysell/my_account.html')

def terms(request, user_name):
	return render(request, 'buysell/terms.html')

def feedback(request, user_name):
	return render(request, 'buysell/feedback.html')

def settings(request, user_name):
	return render(request, 'buysell/settings.html')

def following(request, user_name):
	return render(request, 'buysell/following.html')

def notifications(request, user_name):
	return render(request, 'buysell/notifications.html')

def forgot_password(request):
	return render(request, 'buysell/forgot_password.html')