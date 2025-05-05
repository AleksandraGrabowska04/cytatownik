from django.contrib import admin
from .models import Quote, Comment, Vote

admin.site.register(Quote)
admin.site.register(Comment)
admin.site.register(Vote)
