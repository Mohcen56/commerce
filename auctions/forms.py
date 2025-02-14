# auctions/forms.py
from django import forms
from .models import AuctionListing

class ListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the title of your listing'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter a description for your listing'
            }),
            'starting_bid': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your starting bid'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional image URL'
            }),
            'category': forms.Select(attrs={
                'style': 'width: 91%;',
                'class': 'form-select',
            }),
        }

