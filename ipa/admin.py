from django.contrib import admin
from ipa.models import Word, Ipa, Audio

# Register your models here.

class IpaInline(admin.TabularInline):
    model = Ipa

class AudioInline(admin.TabularInline):
    model = Audio

class WordAdmin(admin.ModelAdmin):
    inlines = [IpaInline, AudioInline]

admin.site.register(Word, WordAdmin)
