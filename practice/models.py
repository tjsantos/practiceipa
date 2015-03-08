from django.db import models
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.text import slugify
from ipa.models import Word
from ordered_model.models import OrderedModel
import random

class Wordlist(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(db_index=False)
    words = models.ManyToManyField(Word, through='WordlistWord')

    def get_absolute_url(self):
        return reverse(
            'practice:wordlists', kwargs={'wordlist_id': self.id, 'wordlist_slug': self.slug}
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # could self.fields['slug'] work?
        self.slug = slugify(self.name)[:self._meta.get_field('slug').max_length]
        super().save(*args, **kwargs)

    @property
    def ipa_list(self):
        # TODO: how to manage multiple choice quiz?
        words = self.words.all().prefetch_related('ipa_set')
        result  = [ipa for word in words for ipa in word.ipa_set.all()]
        return result

class WordlistWord(OrderedModel):
    wordlist = models.ForeignKey(Wordlist, related_name='wordlist_words')
    word = models.ForeignKey(Word)
    order_with_respect_to = 'wordlist'
    # get order id from model field `order` as a 0-indexed positive integer

    class Meta(OrderedModel.Meta):
        unique_together = ('wordlist', 'word')

    def get_absolute_url(self):
        return reverse('practice:quiz', kwargs={
            'wordlist_id': self.wordlist.id,
            'wordlist_slug': self.wordlist.slug,
            'q_id': self.order + 1,
        })

class WordProgress(models.Model):
    '''track the progress of wordlist words for each user'''
    wordlist_word = models.ForeignKey(WordlistWord)
    user = models.ForeignKey('SessionUser')
    correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('wordlist_word', 'user')

    # through associations?
    @property
    def word(self):
        return self.wordlist_word.word

    @property
    def wordlist(self):
        return self.wordlist_word.wordlist

    @property
    def order(self):
        return self.wordlist_word.order

    def check_answer(self, ipa_input):
        if self.word.matches_ipa(ipa_input):
            self.correct = True
            self.save()
        return self.correct

    @classmethod
    def prepare(cls, user, wordlist):
        '''initialize word progress for the given user and wordlist'''
        # TODO: only execute if necessary
        wordlist_words = wordlist.wordlist_words.all().prefetch_related('word__ipa_set')
        for wordlist_word in wordlist_words:
            cls.objects.get_or_create(wordlist_word=wordlist_word, user=user)

    def mc_choices(self):
        # obtain multiple choice options
        # grab n random words in the wordlist to populate choices
        n = 4 # total number of mc_choices
        words = Word.objects.filter(wordlist=self.wordlist).order_by('?').exclude(word=self.word)
        mc_choices = []
        for word in words[:n]:
            ipa = word.ipa_set.first()
            mc_choices.append(self.ipa_choice_tuple(ipa))
        # place the correct answer in the choices
        ipa_answer = self.word.ipa_set.first()
        answer_choice_tuple = self.ipa_choice_tuple(ipa_answer)
        if len(mc_choices) < n:
            mc_choices.append(answer_choice_tuple)
        else:
            idx_replace = random.randrange(len(mc_choices))
            mc_choices[idx_replace] = answer_choice_tuple
        return mc_choices

    @classmethod
    def ipa_choice_tuple(cls, ipa):
        return (ipa.ipa, str(ipa))

    @classmethod
    def get_next_word(cls, user, wordlist):
        wp_qset = cls.objects.filter(user=user, wordlist_word__wordlist=wordlist)
        wp_qset = wp_qset.filter(correct=False).order_by('wordlist_word')
        try:
            return wp_qset[0]
        except IndexError:
            raise cls.DoesNotExist

    def get_absolute_url(self):
        return reverse('practice:quiz_question', kwargs={
            'wordlist_id': self.wordlist.id,
            'wordlist_slug': self.wordlist.slug,
            'q_id': self.order + 1,
        })

    @classmethod
    def reset_progress(cls, user, wordlist):
        cls.objects.filter(user=user, wordlist_word__wordlist=wordlist).update(correct=False)

    @classmethod
    def progress(cls, user, wordlist):
        words = list(cls.objects.filter(user=user, wordlist_word__wordlist=wordlist))
        total = len(words)
        correct = sum(1 for word in words if word.correct == True)
        percentage = int(100 * correct / total)
        return {'total': total, 'correct': correct, 'percentage': percentage}

class SessionUser(models.Model):
    # automatic ids for each session

    @classmethod
    def from_session(cls, session):
        if 'id' not in session:
            user = cls.objects.create()
            session['id'] = user.id
        else:
            user = cls.objects.get(id=session['id'])
        return user

#class IpaChoice(models.Model):
#    '''multiple choice answer for each word quiz'''
#    word_progress = models.ForeignKey(WordProgress, related_name='ipa_choices')
#    ipa = models.CharField(max_length=200)
#
#    class Meta:
#        unique_together = ('word_progress', 'ipa')
#
