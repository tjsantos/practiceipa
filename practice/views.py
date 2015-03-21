from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from practice.models import Wordlist, SessionUser, WordProgress, WordlistWord
from practice.forms import QuizQuestionForm, ResetProgressForm
from ipa.models import Word
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage

def index(request):
    wordlists = Wordlist.objects.all()
    return render(request, 'practice/index.html', {'wordlists': wordlists})

def wordlists(request, wordlist_id, wordlist_slug=None, page=1):
    user = SessionUser.from_session(request.session)
    wordlist = get_object_or_404(Wordlist, pk=wordlist_id)
    if wordlist.slug != wordlist_slug:
        return redirect(wordlist.get_absolute_url(page=page))
    paginator = Paginator(wordlist.wordlist_words.all(), 10) # 10 words per page
    try:
        page_words = paginator.page(page)
    except InvalidPage:
        return redirect(wordlist)

    WordProgress.prepare(user, wordlist)
    reset_url = reverse('practice:reset_progress',
        kwargs={'wordlist_id': wordlist.id, 'wordlist_slug': wordlist.slug}
    )
    reset_form = ResetProgressForm()
    wordlist_progress = WordProgress.progress(user, wordlist)
    # paginator navigation; extend by 2 pages, max of 5 visible
    first = max(1, page_words.number - 2)
    last = min(first + 5, paginator.num_pages)
    page_range = range(first, last + 1)
    return render(request, 'practice/wordlists.html', {
        'wordlist': wordlist, 'reset_url': reset_url, 'reset_form': reset_form,
        'wordlist_progress': wordlist_progress, 'page_range': page_range, 'page_words': page_words
    })

def quiz(request, wordlist_id, wordlist_slug=None):
    wordlist = get_object_or_404(Wordlist, pk=wordlist_id)
    user = SessionUser.from_session(request.session)
    return redirect_next_question(request, user, wordlist)

def quiz_question(request, wordlist_id, wordlist_slug, q_id):
    '''q_id is 1-based index of words in the wordlist's order'''
    wordlist = get_object_or_404(Wordlist, pk=wordlist_id)
    user = SessionUser.from_session(request.session)
    try:
        word_progress = WordProgress.objects.get(
            user=user, wordlist_word__wordlist=wordlist, wordlist_word__order=(int(q_id) - 1)
        )
    except WordProgress.DoesNotExist:
        raise Http404('Error retreiving quiz data.')

    if request.method == 'POST':
        if request.POST['action'] == 'Continue':
            return redirect_next_question(request, user, wordlist)
        else:
            question_form = word_progress.mc_question_form(request)
            if question_form.is_valid():
                word_progress.check_answer(question_form.cleaned_data['input_choice'])
    else:
        question_form = word_progress.mc_question_form(request)

    return render(request, 'practice/quiz_question.html',
        {'question_form': question_form, 'word_progress': word_progress}
    )

def redirect_next_question(request, user, wordlist):
    # redirect to first unsolved q
    try:
        word_progress = WordProgress.get_next_word(user, wordlist)
    except WordProgress.DoesNotExist:
        messages.info(request, 'You have already completed this quiz.')
        return redirect(wordlist)
    else:
        return redirect(word_progress)

def reset_progress(request, wordlist_id, wordlist_slug=None):
    wordlist = get_object_or_404(Wordlist, pk=wordlist_id)
    prepare_quiz_session(request, wordlist)
    user = get_object_or_404(SessionUser, id=request.session['id'])
    if request.method == 'POST':
        form = ResetProgressForm(request.POST)
        if form.is_valid():
            WordProgress.reset_progress(user, wordlist)
            messages.info(request, 'Progress reset')
            return redirect(wordlist)
    messages.error(request, 'Error reseting progress')
    return redirect(wordlist)
