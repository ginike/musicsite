from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
#from django.http import HttpResponse
from .models import Post, Requesting
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
import operator
from .forms import PostForm, CommentForm, RequestingForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


from django.views.generic import (ListView,
 DetailView,
 UpdateView,
 DeleteView, 
  CreateView
  )


#Creating a function base home view
def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context)

#Creating a Class Based View
class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'#override
	context_object_name = 'posts'#overide
	ordering = ['-date_posted']#sorting accordint to the latest date
	paginate_by = 10

	


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'#override
	context_object_name = 'posts'#overide
	#ordering = ['-date_posted']#sorting accordint to the latest date
	paginate_by = 10

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


#using the default generic view 
class PostDetailView(DetailView):
	model = Post

@method_decorator(staff_member_required, name='dispatch')
class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'composer', 'genre', 'doc_file', 'new_price', 'sample_view', 'lyrics']
	#checking if the one creating is logged in/or is a user
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	
@method_decorator(staff_member_required, name='dispatch')
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'composer', 'doc_file','sample_view', 'lyrics']
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

#checking if the author is the one updating
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

#checking if the author is the one updating
@method_decorator(staff_member_required, name='dispatch')
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



def about(request):
	return render(request, 'blog/about.html', {'title':'About'})

def first_page(request):
	return render(request, 'blog/main.html')


def search(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(title__icontains=query) | Q(composer__icontains=query)

            results= Post.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'blog/home.html', context)

        else:
            return render(request, 'blog/home.html')

    else:
        return render(request, 'blog/home.html')




def search_by_anthem(request):	
	
	context={
		'posts':Post.objects.filter(genre='Anthem')
	}
	print (context)
	return render(request, 'blog/anthems.html', context) 


def search_by_classical(request):	

	context={
		'posts':Post.objects.filter(genre='Classical')
	}
	print (context)
	return render(request, 'blog/classicals.html', context) 



def search_by_highlife(request):	

	context={
		'posts':Post.objects.filter(genre='Highlife')
}
	print (context)
	return render(request, 'blog/highlife.html', context) 


def search_by_hymn(request):	

	context={
		'posts':Post.objects.filter(genre='Hymn')
}
	print (context)
	return render(request, 'blog/hymns.html', context) 
#else:
#	return render(request, 'blog/home.html') 

class PostUpView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = []
	
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def plans(request):
	return render(request, 'blog/plans.html')

#from django.contrib.admin.views.decorators import staff_member_required
#from django.utils.decorators import method_decorator


#@method_decorator(staff_member_required, name='dispatch')
#class ExampleTemplateView(TemplateView):
 #   ...
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})



@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post-detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)



@method_decorator(staff_member_required, name='dispatch')
class PostCreateView2(LoginRequiredMixin, CreateView):
	model = Requesting
	fields = ['author', 'song_title', 'song_composer', 'author_mail', 'author_contact']
	template_name = 'blog/song_request.html'#override
	

	#checking if the one creating is logged in/or is a user
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


def homer(request):
	context = {
		'poets': Requesting.objects.all()
	}
	return render(request, 'blog/request_display.html', context)

#Creating a Class Based View
@method_decorator(staff_member_required, name='dispatch')
class PostListView2(LoginRequiredMixin, ListView):
	model = Requesting
	template_name = 'blog/request_display.html'#override
	context_object_name = 'poets'#overide
	ordering = ['-date_posted']#sorting accordint to the latest date
	paginate_by = 5



