from django.contrib import admin

# Register your models here.
from apps.models import User
from apps.models.phrases import OpenPhrase, Phrase

admin.site.register(User)
admin.site.register(Phrase)
admin.site.register(OpenPhrase)
