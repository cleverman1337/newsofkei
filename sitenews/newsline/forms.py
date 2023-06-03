from .models import Articles, Category
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, ModelChoiceField, Select


class ArticlesForm(ModelForm):
    category = ModelChoiceField(queryset=Category.objects.all(), empty_label=None)

    class Meta:
        model = Articles
        fields = ['title','anons','text_in_box','date','category']

        widgets = {
            "title": TextInput(attrs={'class': 'form-control', 'placeholder':'название статьи'}),
            "anons": TextInput(attrs={'class': 'form-control', 'placeholder': 'анонс статьи'}),
            "date": DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'дата публикации'}),
            "text_in_box": Textarea(attrs={'class': 'form-control', 'placeholder': 'текст статьи'}),
            "category": Select(attrs={'class': 'form-conrol'})
        }