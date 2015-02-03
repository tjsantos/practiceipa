from django.shortcuts import render
from ipa.models import Entry

# Create your views here.
def index(request):
    num_entries = Entry.objects.count()
    context = {'num_entries': num_entries}
    return render(request, 'ipa/index.html', context)
