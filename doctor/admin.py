from django.contrib import admin

from .models import Doctor, Entry, Comment, Favorite, Rating, Like, ServiceListing, Category, Chat

admin.site.register(Doctor)
admin.site.register(Entry)
admin.site.register(ServiceListing)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(Chat)
admin.site.register(Favorite)