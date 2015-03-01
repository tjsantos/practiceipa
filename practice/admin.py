from django.contrib import admin
from ipa.models import Word
from practice.models import Wordlist, WordlistWord

class WordlistWordInline(admin.TabularInline):
    model = WordlistWord

class WordlistAdmin(admin.ModelAdmin):
    inlines = (WordlistWordInline,)

admin.site.register(Wordlist, WordlistAdmin)
