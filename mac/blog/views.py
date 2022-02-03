from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from .models import Blogpost

# Create your views here.


def index(request):
    params = {}
    blogpost = Blogpost.objects.all()

    params['blogpost'] = blogpost
    return render(request, "blog/index.html", params)


def blogpost(request, postid):
    print(postid)
    blogpost = Blogpost.objects.filter(post_id=postid)[0]
    print(blogpost)
    params = {'blogpost': blogpost}
    return render(request, "blog/blogPost.html", params)
