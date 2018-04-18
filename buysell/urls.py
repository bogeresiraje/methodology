from django.urls import path
from . import views

app_name = 'buysell'

urlpatterns = [
	path('', views.index, name='index'),
	path('signup/', views.signup, name='signup'),
	path('confirm/', views.confirm, name='confirm'),
	path('contin/<str:user_name>/', views.contin, name='contin'),
	path('login/', views.login, name='login'),
	path('<user_name>/postfeed/', views.postfeed, name='postfeed'),
	path('<user_name>/sell/', views.sell, name='sell'),
	path('<user_name>/verify_post/', views.verify_post, name='verify_post'),
	path('<user_name>/post_item_to_buy/', views.post_item_to_buy, name='post_item_to_buy'),
	path('<user_name>/buy/', views.buy, name='buy'),
	path('<user_name>/my_activity/', views.my_activity, name='my_activity'),
	path('<user_name>/<messages>/<message_receiver>/write_message/', views.write_message, name='write_message'),
	path('<user_name>/<messages>/<message_receiver>/send_message/', views.send_message, name='send_message'),
	path('<user_name>/messages/', views.messages, name='messages'),
	path('<user_name>/search/', views.search, name='search'),
	path('<user_name>/most_followed/', views.most_followed, name='most_followed'),
	path('<user_name>/categories/', views.categories, name='categories'),
	path('<user_name>/my_account/', views.my_account, name='my_account'),
	path('<user_name>/terms/', views.terms, name='terms'),
	path('<user_name>/feedback/', views.feedback, name='feedback'),
	path('<user_name>/settings/', views.settings, name='settings'),
	path('<user_name>/following/', views.following, name='following'),
	path('<user_name>/not_followed/', views.not_followed, name='not_followed'),
	path('<user_name>/follow/', views.follow, name='follow'),
	path('<user_name>/notifications/', views.notifications, name='notifications'),
	path('forgot_password/', views.forgot_password, name='forgot_password'),
	path('<user_name>/<post_identifier>/<int:post_id>/comments/', views.comments, name='comments'),
	path('<user_name>/<post_identifier>/<int:post_id>/write_comment', views.write_comment, name='write_comment'),
	]