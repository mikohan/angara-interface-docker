from product.models import Category
from django import forms


class KeyWordForm(forms.Form):
    group_name = forms.CharField(label='Название группы')
    parent = forms.ModelChoiceField(queryset=Category.objects.filter(id__gt=0, id__lt=20).order_by('name'), label='Родительская Категория', required=False)
    plus = forms.CharField(label='Плюс слова', widget=forms.Textarea(attrs={'rows': 5}))
    minus = forms.CharField(label='Минус слова', widget=forms.Textarea(attrs={'rows': 5}), required=False)