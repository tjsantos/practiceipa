from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from practice.models import Wordlist
from ipa.models import Word
from django.http import Http404

def index(request):
    wordlists = Wordlist.objects.all()
    return render(request, 'practice/index.html', {'wordlists': wordlists})

def wordlists(request, wordlist_id, wordlist_slug=None):
    wordlist = get_object_or_404(Wordlist, pk=wordlist_id)
    if request.path != wordlist.get_absolute_url():
        return redirect(wordlist)
    else:
        return render(request, 'practice/wordlists.html', {'wordlist': wordlist})

def quiz(request, wordlist_id, wordlist_slug=None, q_id=None):
    '''q_id is 1-based index of words in the wordlist's order'''
    wordlist = get_object_or_404(Wordlist, pk=wordlist_id)
    prepare_quiz_session(request, wordlist)
    if not q_id:
        # redirect to first unsolved q
        next_q_id = request.session['score'][wordlist_id] + 1
        if next_q_id > wordlist.words.count():
            messages.info(request, 'You have already completed this quiz.')
            return redirect(wordlist)
        else:
            return redirect(reverse(
                'practice:quiz',
                kwargs={'wordlist_id': wordlist.id, 'wordlist_slug': wordlist.slug, 'q_id': next_q_id}
            ))
    else:
        # show word info and link to quiz question
        try:
            word = wordlist.words.all()[int(q_id) - 1] # given q_id is 1-based
            return render(request, 'practice/quiz_intro.html', {'word': word})
        except IndexError:
            raise Http404('Error retreiving quiz data.')

def quiz_question(request, q_id):
    # render quiz form with answer choices
    # check quiz answers
    pass

def prepare_quiz_session(request, wordlist):
    '''helper method to initialize quiz data'''
    # store score for a given quiz/wordlist
    if 'score' not in request.session:
        request.session['score'] = {}
    if str(wordlist.id) not in request.session['score']:
        request.session['score'][str(wordlist.id)] = 0
