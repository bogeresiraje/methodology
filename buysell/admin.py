from django.contrib import admin
from .models import Account, Buypost, Sellpost, Sent, Received

admin.site.register(Account)
admin.site.register(Buypost)
admin.site.register(Sellpost)
admin.site.register(Sent)
admin.site.register(Received)