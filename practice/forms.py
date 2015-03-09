from django import forms

class QuizQuestionForm(forms.Form):
    input_choice = forms.ChoiceField(choices=(), widget=forms.RadioSelect)

    def __init__(self, mc_choices, *args, **kwargs):
        # create quiz question choices on initialization
        super().__init__(*args, **kwargs)
        self.fields['input_choice'].choices = mc_choices

class ResetProgressForm(forms.Form):
    pass
