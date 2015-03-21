from django.core.management.base import BaseCommand, CommandError
import json
from ipa.models import Word
from practice.models import Wordlist, WordlistWord

class Command(BaseCommand):
    help = 'help text'

    def handle(self, *args, **options):
        if len(args) != 2:
            print('supply filename and wordlist name')
            return

        filename, wordlist_name = args
        with open(filename, 'r', encoding='utf-8') as f:
            wordlist = json.load(f)

        wordlist_obj = Wordlist.objects.create(name=wordlist_name)
        for word in wordlist:
            word_obj = Word.objects.get(word=word)
            WordlistWord.objects.create(wordlist=wordlist_obj, word=word_obj)

        print('Created {} with {} words'.format(wordlist_obj, wordlist_obj.wordlist_words.count()))
