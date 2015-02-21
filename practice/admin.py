from django.contrib import admin
from ipa.models import Word
from practice.models import Wordlist

#class WordInline(admin.TabularInline):
#    model = Word

class WordlistAdmin(admin.ModelAdmin):
    filter_horizontal = ('words',)
#    inlines = [WordInline]

admin.site.register(Wordlist, WordlistAdmin)
