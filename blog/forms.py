from django import forms

from .models import Post, Comment, Requesting

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'author', 'composer', 'doc_file','sample_view', 'new_price','date_posted', 'genre', 'lyrics')



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text')


class RequestingForm(forms.ModelForm):
    class Meta:
        model = Requesting
        fields = ('your_name', 'song_title', 'song_composer', 'your_email', 'your_contact')
