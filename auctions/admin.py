from django.contrib import admin
from .models import User, Listing, Watchlist, Category, Bid, Comments, Winner
# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(Winner)