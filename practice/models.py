from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from ipa.models import Word
from ordered_model.models import OrderedModel

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

class WordlistWord(OrderedModel):
    wordlist = models.ForeignKey(Wordlist, related_name='wordlist_words')
    word = models.ForeignKey(Word)
    order_with_respect_to = 'wordlist'
    # get order id from model field `order` as a 0-indexed positive integer

    class Meta(OrderedModel.Meta):
        pass # placeholder to remember to inherit from ordered model

    def get_absolute_url(self):
        #return redirect(reverse(
        #    'practice:quiz',
        #    kwargs={'wordlist_id': wordlist.id, 'wordlist_slug': wordlist.slug, 'q_id': next_q_id}
        #))

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
        return self.word.matches_ipa(ipa_input)

    @classmethod
    def prepare(cls, user, wordlist):
        '''if necessary, initialize word progress for the given user and wordlist'''
        for wordlist_word in wordlist.wordlist_words.all():
            cls.create(wordlist_word=wordlist_word, user=user)

    def get_mc_form(self):
        pass

    @classmethod
    def get_next_word(cls):
        raise cls.DoesNotExist

    def get_absolute_url(self):
        return reverse(
            'practice:quiz_question',
            kwargs={'wordlist_id': wordlist.id, 'wordlist_slug': wordlist.slug, 'q_id': next_q_id}
        )

class IpaChoice(models.Model):
    '''multiple choice answer for each word quiz'''
    word_progress = models.ForeignKey(WordProgress, related_name='ipa_choices')
    ipa = models.CharField(max_length=200)

class SessionUser(models.Model):
    # automatic ids for each session
    pass
