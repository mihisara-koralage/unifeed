from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Like, Hashtag
from .forms import PostForm

@login_required
def feed_home(request):
    # Page accounts cannot post — enforce here
    form = None
    if request.user.is_student:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('feed:home')
        else:
            form = PostForm()

    posts = Post.objects.select_related('author').prefetch_related('hashtags', 'likes')

    # Attach liked status for each post so the template can style the button
    for post in posts:
        post.user_has_liked = post.is_liked_by(request.user)

    return render(request, 'feed/home.html', {
        'posts': posts,
        'form': form,
    })


@login_required
@require_POST  # only accepts POST requests — no accidental GETs
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not request.user.is_student:
        return JsonResponse({'error': 'Only students can like posts.'}, status=403)

    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # already liked → unlike
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.like_count})


@login_required
def hashtag_feed(request, tag_name):
    hashtag = get_object_or_404(Hashtag, name=tag_name.lower())
    posts = hashtag.posts.select_related('author').prefetch_related('likes')

    for post in posts:
        post.user_has_liked = post.is_liked_by(request.user)

    return render(request, 'feed/hashtag.html', {
        'hashtag': hashtag,
        'posts': posts,
    })