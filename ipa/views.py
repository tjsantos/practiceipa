from django.shortcuts import render
from ipa.models import Entry

# Create your views here.
def index(request):
    num_entries = Entry.objects.count()
    context = {'num_entries': num_entries}
    return render(request, 'ipa/index.html', context)

def detail(request, lang, search):
    # (check language ?)
    try:
        entry = Entry.objects.get(entry=search)
        template = 'ipa/detail.html'
    except Entry.DoesNotExist:
        entry = Entry(entry=search)
        template = 'ipa/not_found.html'
    return render(request, template, {'entry': entry})
