from django.contrib import admin
from ipa.models import Entry, Pronunciation

# Register your models here.

class PronunciationInline(admin.StackedInline):
    model = Pronunciation

class EntryAdmin(admin.ModelAdmin):
    inlines = [PronunciationInline]

admin.site.register(Entry, EntryAdmin)
