from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from practice.models import Wordlist, SessionUser, WordProgress, WordlistWord
from practice.forms import QuizQuestionForm
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
    user = get_object_or_404(SessionUser, id=request.session['id'])
    if not q_id:
        # redirect to first unsolved q
        try:
            word_progress = WordProgress.get_next_word(user, wordlist)
        except WordProgress.DoesNotExist:
            messages.info(request, 'You have already completed this quiz.')
            return redirect(wordlist)
        else:
            return redirect(word_progress.wordlist_word)
    else:
        # show word info and link to quiz question
        try:
            # word_progress = wordlist.word_progress.filter(user).get(wordlist_word__order)
            word_progress = WordProgress.objects.get(
                user=user, wordlist_word__wordlist=wordlist, wordlist_word__order=(int(q_id) - 1)
            )
        except WordProgress.DoesNotExist:
            raise Http404('Error retreiving quiz data.')
        else:
            return render(request, 'practice/quiz_intro.html', {'word_progress': word_progress})

def quiz_question(request, wordlist_id, wordlist_slug, q_id):
    correct = False
    if request.method == 'POST':
        if request.POST['action'] == 'next_question':
            return redirect(reverse('practice:quiz',
                kwargs={'wordlist_id': wordlist_id, 'wordlist_slug': wordlist_slug}
            ))
        else:
            question_form = QuizQuestionForm(wordlist_id, q_id, request.POST)
            if question_form.is_valid():
                correct = True
    else:
        question_form = QuizQuestionForm(wordlist_id, q_id)
    return render(request, 'practice/quiz_question.html',
        {'question_form': question_form, 'correct': correct}
    )

def prepare_quiz_session(request, wordlist):
    '''If necessary, create user and associated word progress for the given wordlist, and set
    session id'''
    if 'id' not in request.session:
        user = SessionUser.objects.create()
        request.session['id'] = user.id
    else:
        user = SessionUser.objects.get(id=request.session['id'])
    WordProgress.prepare(user, wordlist)
