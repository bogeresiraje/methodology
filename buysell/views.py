from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Account, Sellpost, Buypost, Followed
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
	posts = list(get_posts())
	recent_post = get_recent_post(user_name)
	recommended = get_recommended_posts(user_name, posts)
	return render(request, 'buysell/postfeed.html', {'account': account, 'posts': posts, 
		'recent_post': recent_post, 'recommended': recommended})

def sell(request, user_name):
	account = get_object_or_404(Account, pk=user_name)
	posts = list(get_posts())
	recent_post = get_recent_post(user_name)
	recommended = get_recommended_posts(user_name, posts)
	return render(request, 'buysell/sell.html', {'account': account, 'posts': posts, 'recent_post': recent_post,
		'recommended': recommended})

def verify_post(request, user_name):
	account = get_object_or_404(Account, pk=user_name)
	posts = list(get_posts())
	recent_post = get_recent_post(user_name)
	recommended = get_recommended_posts(user_name, posts)
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

	if 'photo' not in request.FILES:
		errors['empty_pic'] = empty_field
	else:
		picture = request.FILES['photo']


	if (item_name and item_description and item_price and current_location and picture):
		account.sellpost_set.create(item=item_name, description=item_description, amount=item_price,
			location=current_location, photo=picture, date_posted=timezone.now(),
			)
		return HttpResponseRedirect(reverse('buysell:my_activity', args=(account.username,)))
	else:
		return render(request, 'buysell/sell.html', {'account': account, 'errors': errors, 'posts': posts,
			'recent_post': recent_post, 'recommended': recommended})

def buy(request, user_name):
	account = get_object_or_404(Account, pk=user_name)
	posts = list(get_posts())
	recent_post = get_recent_post(user_name)
	recommended = get_recommended_posts(user_name, posts)
	return render(request, 'buysell/buy.html', {'account': account, 'posts': posts,
		'recent_post': recent_post, 'recommended': recommended})

def post_item_to_buy(request, user_name):
	account = get_object_or_404(Account, pk=user_name)
	posts = list(get_posts())
	recent_post = get_recent_post(user_name)
	recommended = get_recommended_posts(user_name, posts)

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
		account.buypost_set.create(item=item_name, description=item_description, price=item_price,
			location=current_location, date_posted=timezone.now(),
			)
		return HttpResponseRedirect(reverse('buysell:my_activity', args=(account.username, posts, recent_post, recommended)))
	else:
		return render(request, 'buysell/buy.html', {'errors': errors, 'account':account, 'posts': posts,
			'recent_post': recent_post, 'recommended': recommended})

def my_activity(request, user_name):
	account = get_object_or_404(Account, pk=user_name)
	posts = list(get_posts())
	recent_post = get_recent_post(user_name)
	recommended = get_recommended_posts(user_name, posts)

	buy_posts = list(account.buypost_set.all())
	sell_posts = list(account.sellpost_set.all())
	my_posts = buy_posts + sell_posts
	date_post = [(my_post.date_posted, my_post) for my_post in my_posts]
	sorted_dates = sorted(date_post, key=itemgetter(0), reverse=True)
	my_posts = [post for (date,post) in sorted_dates]
	return render(request, 'buysell/activity.html', {'account': account, 'posts': posts, 'my_posts': my_posts,
		'recent_post': recent_post, 'recommended': recommended})

def write_message(request, user_name, messages, message_receiver):
	account = Account.objects.get(pk=user_name)
	posts  = list(get_posts())
	recent_post = get_recent_post(user_name)
	recommended = get_recommended_posts(user_name, posts)
	unsorted_messages = list(get_messages_by_name(account, message_receiver))
	messages = sort_by_time(unsorted_messages)
	
	return render(request, 'buysell/write_message.html', {'account': account, 'posts': posts,
		'recent_post': recent_post, 'recommended': recommended, 'messages': messages, 'message_receiver': message_receiver})

def send_message(request, user_name, messages, message_receiver):
	message_ = request.POST['text_message']

	account = Account.objects.get(pk=user_name)
	receiver_account = Account.objects.get(pk=message_receiver)

	account.sent_set.create(text=message_, date_posted=timezone.now(), name=receiver_account.username)
	receiver_account.received_set.create(text=message_, date_posted=timezone.now(), name=account.username,)
	receiver_account.notifications_set.create(name=user_name, identifier='message', pub_date=timezone.now())
	return HttpResponseRedirect(reverse('buysell:write_message', args=(account.username, messages, message_receiver)))

def messages(request, user_name):
	account = get_object_or_404(Account, pk=user_name)
	posts = list(get_posts())
	recent_post = get_recent_post(user_name)
	recommended = get_recommended_posts(user_name, posts)

	all_messages = get_messages(account)
	friends = filter_message_by_name(all_messages)
	messages = [get_last_message(all_messages, friend) for friend in friends]
	messages = sort_by_time(messages)

	return render(request, 'buysell/messages.html', {'account': account, 'messages': messages, 'posts': posts,
		'recent_post': recent_post, 'recommended': recommended})

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
	account = Account.objects.get(pk=user_name)
	posts = list(get_posts())
	recent_post = get_recent_post(user_name)
	recommended = get_recommended_posts(user_name, posts)
	following = account.followed_set.all()
	return render(request, 'buysell/following.html', {'account': account, 'posts': posts, 'following': following,
		'recent_post': recent_post, 'recommended': recommended})

def not_followed(request, user_name):
	account = Account.objects.get(pk=user_name)
	posts = list(get_posts())
	recent_post = get_recent_post(user_name)
	recommended = get_recommended_posts(user_name, posts)
	all_accounts = Account.objects.all()
	followed = account.followed_set.all()
	followed_users = [user.name for user in followed]
	not_followed_users = [user.username for user in all_accounts if user.username not in followed_users]
	#filter out empty users that is to say users who do not exist, simply with no IDs
	not_followed_users = [user for user in not_followed_users if user]
	return render(request, 'buysell/not_followed.html', {'account': account, 'posts': posts,
	'not_followed_users': not_followed_users, 'recent_post': recent_post, 'recommended': recommended})

def follow(request, user_name):
	account = Account.objects.get(pk=user_name)
	name_ = request.POST['follow']
	account.followed_set.create(name=name_, pub_time=timezone.now())
	followed_account = Account.objects.get(pk=name_)
	followed_account.notifications_set.create(name=user_name, identifier='follow', pub_date=timezone.now())
	return HttpResponseRedirect(reverse('buysell:not_followed', args=(user_name,)))

def notifications(request, user_name):
	account = Account.objects.get(pk=user_name)
	posts = list(get_posts())
	recent_post = get_recent_post(user_name)
	recommended = get_recommended_posts(user_name, posts)
	my_notifications = account.notifications_set.all()
	my_notifications = sort_by_time(my_notifications)
	return render(request, 'buysell/notifications.html', {'account': account, 'posts': posts, 'my_notifications': my_notifications,
		'recent_post': recent_post, 'recommended': recommended})

def forgot_password(request):
	return render(request, 'buysell/forgot_password.html')

def comments(request, user_name, post_identifier, post_id):
	account = Account.objects.get(pk=user_name)
	posts = list(get_posts())
	recent_post = get_recent_post(user_name)
	recommended = get_recommended_posts(user_name, posts)

	post = get_post_by_id(post_identifier, post_id)
	comments = get_comments(post)

	return render(request, 'buysell/comments.html', {'account': account, 'posts': posts, 'recent_post': recent_post,
		'recommended': recommended, 'post': post, 'comments': comments})

def write_comment(request, user_name, post_identifier, post_id):
	account = Account.objects.get(pk=user_name)
	text_message = request.POST['text']
	post = get_post_by_id(post_identifier, post_id)
	if post_identifier == 'sell':
		post.sellcomment_set.create(text=text_message,publisher=user_name, date_posted=timezone.now())
	else:
		post.buycomment_set.create(text=text_message, publisher=user_name, date_posted=timezone.now())
	return HttpResponseRedirect(reverse('buysell:comments', args=(user_name, post_identifier, post_id)))

def go_to_recent_post(request, user_name, post_identifier, post_id):
	account = Account.objects.get(pk=user_name)
	posts = list(get_posts())
	post = get_post_by_id(post_identifier, post_id)
	return render(request, 'buysell/recent_post.html')

""" 
	Post accessor methods
"""
def get_posts():
	buy_posts = list(Buypost.objects.all())
	sell_posts = list(Sellpost.objects.all())
	all_posts = buy_posts + sell_posts
	posts = sort_by_time(all_posts)
	return posts

def filter_by_item_name(data):
	done = list()
	for obj in data:
		field = obj.item
		if field not in done:
			done.append(field)
			yield obj
		else:
			continue

def sort_by_time(data):
	obj_time = [ (obj, obj.date_posted) for obj in data]
	sorted_obj_time = sorted(obj_time, key=itemgetter(1), reverse=True)
	for obj, time in sorted_obj_time:
		yield obj

def get_recent_post(user_name):
	for post in get_posts():
		if post.post_identifier == 'sell' and post.publisher.username != user_name:
			no_post = None
			return post

def get_recommended_posts(user_name, posts):
	filtered_posts = list(filter_by_item_name(posts))
	sorted_posts = list(sort_by_time(filtered_posts))
	return filtered_posts[:6]

"""
	Message accessor methods
"""

def get_messages(account):
	sent_messages = list(account.sent_set.all())
	received_messages = list(account.received_set.all())
	return (sent_messages + received_messages)

def filter_message_by_name(messages):
	done = list()
	for message in messages:
		name = message.name
		if name not in done:
			done.append(name)
			yield name
		else:
			continue

def get_last_message(messages, friend):
	messages = sort_by_time(messages)
	for message in messages:
		if message.name == friend:
			return message
		else:
			continue

def get_messages_by_name(account, name):
	messages = get_messages(account)
	for message in messages:
		if message.name == name:
			yield message

def get_post_by_id(post_identifier, post_id):
	if post_identifier == 'sell':
		return Sellpost.objects.get(pk=post_id)
	else:
		return Buypost.objects.get(pk=post_id)

def get_comments(post):
	if post.post_identifier == 'sell':
		comments = list(post.sellcomment_set.all())
	else:
		comments = list(post.buycomment_set.all())
	return sort_by_time(comments)