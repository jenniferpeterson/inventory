from django import forms

from .models import User, Category, Location, Item, StorageType


class NewItemForm(forms.Form):
    item_name = forms.CharField(label="Item Name", widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    description = forms.CharField(
        label="Description", widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(
    ).order_by('category_name'), widget=forms.Select(attrs={'class': 'form-control'}))
    img = forms.URLField(label="Image", widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)
    stored_in = forms.ModelChoiceField(queryset=StorageType.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))


class NewStorage(forms.Form):
    storageType = forms.CharField(label="Storage Name", widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    location = forms.ModelChoiceField(queryset=Location.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))
    notes = forms.CharField(label="Notes", widget=forms.Textarea(
        attrs={'class': 'form-control'}), required=False)


class NewStorageLocation(forms.Form):
    location = forms.CharField(
        label="Location Name", widget=forms.TextInput(attrs={'class': 'form-control'}))


class SearchUsersForm(forms.Form):
    user = forms.CharField(label="Search Users", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
