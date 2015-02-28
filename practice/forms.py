from django import forms
from django.shortcuts import get_object_or_404
from practice.models import Wordlist

class QuizQuestionForm(forms.Form):
    input_choice = forms.ChoiceField(choices=(), widget=forms.RadioSelect)

    def __init__(self, wordlist_id, q_id, *args, **kwargs):
        # create quiz question choices on initialization
        super().__init__(*args, **kwargs)
        self.create_quiz_choices(wordlist_id, q_id)
        self.fields['input_choice'].choices = self.choices

    def clean_input_choice(self):
        if self.cleaned_data['input_choice'] != self.answer:
            raise forms.ValidationError("incorrect")
        return self.cleaned_data['input_choice']

    def create_quiz_choices(self, wordlist_id, q_id):
        '''Instantiates self.choices and self.answer'''
        wordlist = get_object_or_404(Wordlist, pk=wordlist_id)
        self.choices = (
            ('a', 'a'),
            ('b', 'b'),
            ('c', 'c'),
            ('d', 'd'),
        )
        self.answer = 'b'
