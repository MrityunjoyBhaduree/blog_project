from django import forms
from .models import Comment

class CommentFrom(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ["name", "email", "body"]
    widgets = {
      "name": forms.TextInput(attrs={"placeholder": "Your name"}),
      "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
      "body": forms.Textarea(attrs={"placeholder": "Share your thoughts..."})
    }


class SearchFrom(forms.Form):
  q = forms.CharField(max_length=100, required=False)

