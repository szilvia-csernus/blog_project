from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import ListView
from django.views import View
from django.core.mail import send_mail, EmailMessage

from .models import Post
from .forms import CommentForm, ContactMeForm


class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


# def starting_page(request):
#      # [:3] means first 3, [-3:] is not supported!!
#     posts = Post.objects.all().order_by('-date')[:3]
#     return render(request, "blog/index.html", {
#         "posts": posts
#     })

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

# def posts(request):
#     posts = Post.objects.all().order_by('-date')
#     return render(request, "blog/all-posts.html", {
#         "posts": posts
#     })


class PostDetailView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            saved_for_later = False
        else:
            saved_for_later = post_id in stored_posts
        return saved_for_later
    
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        
         
        context = {
          "post": post,
          "post_tags": post.tags.all(),
          "comment_form": CommentForm(),
          "comments": post.comments.all().order_by("-id"),
          "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        print(comment_form)
        post = get_object_or_404(Post, slug=slug)

        if comment_form.is_valid():
          comment = comment_form.save(commit=False)
          comment.post = post
          comment.save()

          return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
          "post": post,
          "post_tags": post.tags.all(),
          "comment_form": comment_form,
          "comments": post.comments.all().order_by("-id"),
          "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)              
                      

# class PostDetailView(DetailView):
#     template_name = "blog/post-detail.html"
#     model = Post
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tags.all()
#         context["comment_form"] = CommentForm()
#         return context


# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tags.all()
#     })

class SendEmailView(View):
    def get(self, request):
        form = ContactMeForm()
        return render(request, "blog/contact-me.html", {
            "form": form
        })
    
    def post(self, request):
        form = ContactMeForm(request.POST, request.FILES)  # Include request.FILES to handle attachments

        if form.is_valid():
            subject = "Contact Me Email from " + form.cleaned_data['user_name']
            from_email = form.cleaned_data['user_email']
            message = form.cleaned_data['user_name'] + form.cleaned_data['text']
            recipient_list = ['csernus.szilvi@gmail.com']

            email = EmailMessage(subject, message, from_email, recipient_list)

            # Attach the file/image
            if 'attachment' in request.FILES:
                attachment = request.FILES['attachment']
                email.attach('my-image', attachment.read(), attachment.content_type)

            email.send()

            return HttpResponse("Email sent successfully.")
        else:
            # Handle the case when the form is not valid
            return render(request, "blog/contact-me.html", {
                "form": form
            })

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        
        context = {}
        
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
            
        return render(request, "blog/stored-posts.html", context)
    
    
    def post(self, request):
        stored_posts = request.session.get("stored_posts")
        
        if stored_posts is None:
            stored_posts = []
            
        post_id = int(request.POST["post_id"])
            
        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        else:
            stored_posts.remove(post_id)
            request.session["stored_posts"] = stored_posts
            
        return HttpResponseRedirect("/")
    
        
