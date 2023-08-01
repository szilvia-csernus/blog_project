from datetime import date

from django.shortcuts import render

all_posts = [
    {
        "slug": "hike-in-the-mountains1",
        "image": "mountains.jpg",
        "author": "Maximilian Schwarzmüller",
        "date": date(2023, 5, 1),
        "title": "Mountain Hiking",
        "excerpt": """There's nothing like the views you get when hiking in
            the mountains! And I wasn't even prepared for what happened 
            halfway through the hike...""",
        "content": """
            Lorem ipsum dolor sit amet consectetur adipisicing elit. 
            Ducimus accusantium eligendi illo quam autem laborum
            cumque error debitis quis, aliquam ex eius modi rem aut 
            ratione nulla tempora dolorem blanditiis?
            """
    },
    {
        "slug": "nature-at-its-best",
        "image": "woods.jpg",
        "author": "Maximilian Schwarzmüller",
        "date": date(2023, 8, 1),
        "title": "Nature at its best",
        "excerpt": """There's nothing like the views you get when hiking in
            the forest! And I wasn't even prepared for what happened 
            halfway through the hike...""",
        "content": """
            Lorem ipsum dolor sit amet consectetur adipisicing elit. 
            Ducimus accusantium eligendi illo quam autem laborum
            cumque error debitis quis, aliquam ex eius modi rem aut 
            ratione nulla tempora dolorem blanditiis?
            """
    },
    {
        "slug": "progreamming-is-fun",
        "image": "coding.jpg",
        "author": "Maximilian Schwarzmüller",
        "date": date(2023, 7, 1),
        "title": "Latest on AI",
        "excerpt": """This week brought yet another set of exciting news
        on the AI front...""",
        "content": """
            Lorem ipsum dolor sit amet consectetur adipisicing elit. 
            Ducimus accusantium eligendi illo quam autem laborum
            cumque error debitis quis, aliquam ex eius modi rem aut 
            ratione nulla tempora dolorem blanditiis?
            """
    },
    {
        "slug": "beach",
        "image": "beach.jpg",
        "author": "Maximilian Schwarzmüller",
        "date": date(2023, 6, 1),
        "title": "Beach Adventure",
        "excerpt": """There's nothing like the views you get when strolling on
        the beach! And I wasn't even prepared for what happened 
            halfway through the hike...""",
        "content": """
            Lorem ipsum dolor sit amet consectetur adipisicing elit. 
            Ducimus accusantium eligendi illo quam autem laborum
            cumque error debitis quis, aliquam ex eius modi rem aut 
            ratione nulla tempora dolorem blanditiis?
            """
    }
]

def get_date(post):
    return post['date']

# Create your views here.


def starting_page(request):
    sorted_posts = sorted(all_posts, key=get_date)
    latest_posts = sorted_posts[-3:]
    return render(request, "blog/index.html", {
        "posts": latest_posts
    })


def posts(request):
    posts = sorted(all_posts, key=get_date)
    return render(request, "blog/all-posts.html", {
        "posts": posts
    }
    )


def post_detail(request, slug):
    identified_post = next(post for post in all_posts if post['slug'] == slug)
    return render(request, "blog/post-detail.html", {
        "post": identified_post
    })
