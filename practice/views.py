from django.shortcuts import render, get_object_or_404, redirect
from practice.models import Wordlist

def index(request):
    wordlists = Wordlist.objects.all()
    return render(request, 'practice/index.html', {'wordlists': wordlists})

def wordlists(request, wordlist_id, wordlist_name=None):
    wordlist = get_object_or_404(Wordlist, pk=wordlist_id)
    if request.path != wordlist.get_absolute_url():
        return redirect(wordlist)
    else:
        return render(request, 'practice/wordlists.html', {'wordlist': wordlist})
