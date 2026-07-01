from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model

from users.decorators import admin_required
from users.models import CustomUser
from feed.models import Post
from messaging.models import Message
from resources.models import Resource
from events.models import Event, RSVP
from marketplace.models import Listing, Report

User = get_user_model()


@admin_required
def overview(request):
    now = timezone.now()

    stats = {
        'total_users':      User.objects.count(),
        'student_count':    User.objects.filter(role='student').count(),
        'page_count':       User.objects.filter(role='page').count(),
        'pending_pages':    User.objects.filter(role='page', is_verified=False).count(),
        'total_posts':      Post.objects.count(),
        'total_messages':   Message.objects.count(),
        'total_resources':  Resource.objects.filter(is_approved=True).count(),
        'total_events':     Event.objects.count(),
        'upcoming_events':  Event.objects.filter(start_date__gte=now).count(),
        'total_listings':   Listing.objects.filter(is_active=True, is_approved=True).count(),
        'open_reports':     Report.objects.count(),
    }

    return render(request, 'dashboard/overview.html', {'stats': stats})


@admin_required
def user_list(request):
    role   = request.GET.get('role', '')
    search = request.GET.get('search', '').strip()

    users = User.objects.all().order_by('-date_joined')

    if role in ('student', 'page', 'admin'):
        users = users.filter(role=role)
    if search:
        users = users.filter(email__icontains=search)

    return render(request, 'dashboard/users.html', {
        'users':       users,
        'active_role': role,
        'search':      search,
    })


@admin_required
def change_role(request, user_id):
    target = get_object_or_404(User, id=user_id)

    if target == request.user:
        messages.error(request, 'You cannot change your own role.')
        return redirect('dashboard:users')

    new_role = request.POST.get('role')
    if new_role in ('student', 'page', 'admin'):
        target.role = new_role
        target.save()
        messages.success(request, f'{target.email} role changed to {new_role}.')

    return redirect('dashboard:users')


@admin_required
def verify_page(request, user_id):
    target = get_object_or_404(User, id=user_id, role='page')
    target.is_verified = not target.is_verified
    target.save()
    status = 'verified' if target.is_verified else 'unverified'
    messages.success(request, f'{target.email} is now {status}.')
    return redirect('dashboard:users')


@admin_required
def moderation_queue(request):
    flagged_posts    = Post.objects.select_related('author').order_by('-created_at')[:50]
    open_reports     = Report.objects.select_related(
        'reporter', 'listing'
    ).order_by('-created_at')
    flagged_resources = Resource.objects.filter(
        is_approved=True
    ).select_related('contributor').order_by('-created_at')[:30]

    return render(request, 'dashboard/moderation.html', {
        'flagged_posts':      flagged_posts,
        'open_reports':       open_reports,
        'flagged_resources':  flagged_resources,
    })


@admin_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect('dashboard:moderation')


@admin_required
def remove_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    listing.is_approved = False
    listing.save()
    messages.success(request, f'Listing "{listing.title}" removed.')
    return redirect('dashboard:moderation')


@admin_required
def remove_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    resource.is_approved = False
    resource.save()
    messages.success(request, f'Resource "{resource.title}" removed.')
    return redirect('dashboard:moderation')