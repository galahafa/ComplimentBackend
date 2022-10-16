from django import forms
from django.contrib import admin

# Register your models here.
from apps.models import User
from apps.models.phrases import OpenPhrase, Phrase

# admin.site.register(User)
# admin.site.register(Phrase)
# admin.site.register(OpenPhrase)


@admin.register(OpenPhrase)
class OpenPhraseAdmin(admin.ModelAdmin):
    list_display = ['id', 'phrase', 'user',  'open_date', 'left_to_share']
    fields = ['user', 'phrase', 'open_date', 'is_watched', 'get_from', 'left_to_share']
    readonly_fields = ['open_date']
    list_filter = ['left_to_share']
    list_display_links = ['id', 'phrase']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'name', 'last_name']
    fields = ['username', 'name', 'last_name', 'email', 'is_superuser', 'is_staff']
    search_fields = ['name', 'last_name']
    list_filter = ['is_superuser', 'is_staff']
    list_display_links = ['id', 'username']


class PhraseAdminForm(forms.ModelForm):
    class Meta:
        model = Phrase
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
        fields = '__all__'


@admin.register(Phrase)
class PhraseAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_text', 'rarity']
    search_fields = ['text']
    list_filter = ['rarity']
    fields = ['text', 'rarity']
    list_display_links = ['id', 'get_text']
    form = PhraseAdminForm

    def get_text(self, obj):
        short_text = obj.text[:50]
        if short_text != obj.text:
            short_text = f'{short_text}...'
        return short_text

    get_text.short_description = "text"
