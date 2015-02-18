from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from ipa.models import Word

def index(request):
    num_entries = Word.objects.count()
    context = {'num_entries': num_entries}
    return render(request, 'ipa/index.html', context)

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
