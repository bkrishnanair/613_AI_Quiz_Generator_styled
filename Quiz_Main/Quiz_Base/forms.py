from django import forms

class QuizForm(forms.Form):
    def __init__(self, mcqs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for idx, mcq in enumerate(mcqs):
            choices = [(key, value) for key, value in mcq.get('options', {}).items()]
            self.fields[f'question_{idx}'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect(attrs={
                    'class': 'form-radio'
                }),
                required=True
            )