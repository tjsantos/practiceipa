from django.contrib import admin
from ipa.models import Entry, Ipa, Audio

# Register your models here.

class IpaInline(admin.TabularInline):
    model = Ipa

class AudioInline(admin.TabularInline):
    model = Audio

class EntryAdmin(admin.ModelAdmin):
    inlines = [IpaInline, AudioInline]

admin.site.register(Entry, EntryAdmin)
