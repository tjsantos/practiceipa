from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from ipa.models import Word
from practice.models import Wordlist

def index(request):
    try:
        wordlist = Wordlist.objects.get(name__iexact='english alphabet')
    except Wordlist.DoesNotExist:
        wordlist = None
    return render(request, 'ipa/index.html', {'wordlist': wordlist})

def detail(request, lang, search):
    if lang not in Word.LANG_CODES:
        raise Http404('Language code "{}" not found'.format(lang))
    try:
        word = Word.objects.prefetch_related('ipa_set', 'audio_set').get(word=search)
    except Word.DoesNotExist:
        word = Word(word=search)
    return render(request, 'ipa/detail.html', {'word': word})

def search(request):
    try:
        redirect_url = reverse('ipa:detail', args=(request.GET['lang'], request.GET['search']))
        return HttpResponseRedirect(redirect_url)
    except KeyError:
        raise Http404('Missing GET parameter(s)')
