from ipa.models import Word

def word_count(request):
    return {'word_count': Word.objects.count()}
