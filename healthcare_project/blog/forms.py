from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'featured_image', 'summary', 'content', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'summary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief summary (max 15 words)', 'maxlength': '150'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if len(summary.split()) > 15:
            raise forms.ValidationError('Summary cannot exceed 15 words.')
        if len(summary) > 500:
            raise forms.ValidationError('Summary cannot exceed 500 characters.')
        return summary
