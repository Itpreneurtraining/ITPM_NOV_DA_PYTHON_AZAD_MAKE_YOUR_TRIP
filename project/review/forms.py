from django import forms
from .models import Review,ReviewComment

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, '★' * i) for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label="Rating"
    )

    class Meta:
        model = Review
         
        exclude = ['user']
        fields = ['rating', 'comment', 'profile_picture']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
   
        }

class ReviewCommentForm(forms.ModelForm):
    name = forms.CharField(
        required=False,
        max_length=100,
        label="Your name (if not logged in)"
    )

    class Meta:
        model = ReviewComment
        fields = ['name', 'comment']