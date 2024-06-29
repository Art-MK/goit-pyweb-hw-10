from django import forms
from .models import Author, Quote

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']

class QuoteForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.Textarea, help_text="Введите теги, разделенные запятыми или новой строкой.")

    class Meta:
        model = Quote
        fields = ['tags', 'author', 'text']

    def clean_tags(self):
        data = self.cleaned_data['tags']
        tags_list = [tag.strip() for tag in data.replace('\n', ',').split(',')]
        return tags_list
