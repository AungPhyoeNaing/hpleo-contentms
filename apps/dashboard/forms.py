from django import forms
from apps.videos.models import Video, Category

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'category', 'thumbnail_url', 'description', 'external_id']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500'}),
            'category': forms.Select(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500'}),
            'thumbnail_url': forms.URLInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500', 'rows': 5}),
            'external_id': forms.NumberInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'external_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500'}),
            'external_id': forms.NumberInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500'}),
        }
