from django import forms
from django.contrib import admin
from django.db.models import Count
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from apps.models import User
from apps.models.phrases import Collection, OpenPhrase, Phrase


class PhraseResource(resources.ModelResource):

    class Meta:
        model = Phrase
        fields = ['id', 'text', 'rarity', 'collection', 'status']


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


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'phrase_numbers', 'create_date']
    search_fields = ['name']
    list_filter = ['status']
    list_editable = ['status']
    list_display_links = ['id', 'name']

    def get_queryset(self, request):
        qs = super(CollectionAdmin, self).get_queryset(request)
        qs = qs.annotate(phrase_numbers=Count('phrase'))
        return qs

    def phrase_numbers(self, obj):
        return obj.phrase_numbers


@admin.register(Phrase)
class PhraseAdmin(ImportExportModelAdmin):
    list_display = ['id', 'get_text', 'rarity', 'status', 'collection']
    search_fields = ['text']
    list_filter = ['rarity']
    list_editable = ['collection', 'status']
    fields = ['text', 'rarity']
    list_display_links = ['id', 'get_text']
    resource_classes = [PhraseResource]
    list_per_page = 10
    form = PhraseAdminForm

    def get_text(self, obj):
        short_text = obj.text[:50]
        if short_text != obj.text:
            short_text = f'{short_text}...'
        return short_text

    get_text.short_description = "text"
