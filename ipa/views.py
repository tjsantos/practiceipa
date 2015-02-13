from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from ipa.models import Word

# Create your views here.
def index(request):
    num_entries = Word.objects.count()
    context = {'num_entries': num_entries}
    return render(request, 'ipa/index.html', context)

def detail(request, lang, search):
    # (check language ?)
    try:
        word = Word.objects.get(word=search)
        template = 'ipa/detail.html'
    except Word.DoesNotExist:
        word = Word(word=search)
        template = 'ipa/not_found.html'
    return render(request, template, {'word': word})

def search(request):
    try:
        redirect_url = reverse('detail', args=(request.GET['lang'],
                                               request.GET['search']))
        return HttpResponseRedirect(redirect_url)
    except KeyError:
        return HttpResponseRedirect(reverse('index'))
