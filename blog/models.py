from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image
from django.conf import settings


CHOICES=(
	('Anthem','ANTHEM'),
	('Classical','CLASSICAL'),
	('Highlife','HIGHLIFE'),
	('Hymn','HYMN'),

)
class Post(models.Model):	
	title = models.CharField(max_length=100)
	composer = models.CharField(max_length=100)
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)	
	doc_file = models.FileField(upload_to='media/site_docs/')
	genre = models.CharField(choices=CHOICES, default='Anthem', max_length=30, null=True)
	new_price = models.IntegerField(default='0.00', null=True)
	sample_view= models.ImageField(default='/media/sample_score.jpg', upload_to='sample_sheet', null=False)
	lyrics = models.TextField(max_length=1000, null=True)
	

	def approved_comments(self):
	    return self.comments.filter(approved_comment=True)


	


	

	def __str__(self):
		return self.title

	def get_absolute_url(self):
			return reverse('post-detail', kwargs={'pk': self.pk})
	def save(self):
			super().save()

			img = Image.open(self.sample_view.path)

			if img.height > 300 or img.width > 300:
				output_size = (100, 100)
				img.thumbnail(output_size)
				img.save(self.sample_view.path)








class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text



class Requesting(models.Model):
	author = models.CharField(max_length=50)
	song_title = models.CharField(max_length=50)
	song_composer = models.CharField(max_length=50, null=True)
	author_mail = models.CharField(null=True, max_length=50)
	author_contact=models.CharField(max_length=15)
	date_posted = models.DateTimeField(default=timezone.now)
	

	def __str__(self):
		return self.author

	def get_absolute_url(self):
			return reverse('blog-home')
	





