from django import forms
from .models import auction

class uploads(forms.ModelForm):
    class Meta:
        model = auction
        fields = ('title', 'image' , 'bid' , 'describe', 'category')