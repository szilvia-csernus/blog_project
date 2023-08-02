from .models import Post, Author, Tag

from django.shortcuts import render, get_object_or_404


def starting_page(request):
     # [:3] means first 3, [-3:] is not supported!!
    posts = Post.objects.all().order_by('-date')[:3]
    return render(request, "blog/index.html", {
        "posts": posts
    })


def posts(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, "blog/all-posts.html", {
        "posts": posts
    }
    )


def post_detail(request, slug):
    identified_post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html", {
        "post": identified_post,
        "post_tags": identified_post.tags.all()
    })
