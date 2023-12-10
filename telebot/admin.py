from django.contrib import admin

from telebot.models import Store, User, Trek, Order, CompletedOrder

admin.site.register(Store)
admin.site.register(User)
admin.site.register(Trek)
admin.site.register(Order)
admin.site.register(CompletedOrder)
