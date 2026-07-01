from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Event, RSVP
from .forms import EventForm

@login_required
def event_list(request):
    now      = timezone.now()
    upcoming = Event.objects.filter(start_date__gte=now).select_related('organizer')
    past     = Event.objects.filter(start_date__lt=now).select_related('organizer')

    return render(request, 'events/list.html', {
        'upcoming': upcoming,
        'past':     past,
    })


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Get this user's RSVP if it exists
    user_rsvp = None
    if request.user.is_student:
        user_rsvp = RSVP.objects.filter(user=request.user, event=event).first()

    return render(request, 'events/detail.html', {
        'event':     event,
        'user_rsvp': user_rsvp,
    })


@login_required
def create_event(request):
    # Only Page accounts can create events
    if not request.user.is_page:
        messages.error(request, 'Only organisation accounts can create events.')
        return redirect('events:list')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:detail', event_id=event.id)
    else:
        form = EventForm()

    return render(request, 'events/create.html', {'form': form})


@login_required
def rsvp_toggle(request, event_id, status):
    # Only students can RSVP
    if not request.user.is_student:
        messages.error(request, 'Only students can RSVP to events.')
        return redirect('events:detail', event_id=event_id)

    if status not in ('going', 'interested'):
        return redirect('events:detail', event_id=event_id)

    event = get_object_or_404(Event, id=event_id)
    rsvp  = RSVP.objects.filter(user=request.user, event=event).first()

    if rsvp:
        if rsvp.status == status:
            # Same button clicked again — cancel the RSVP
            rsvp.delete()
            messages.info(request, 'RSVP cancelled.')
        else:
            # Switch between Going and Interested
            rsvp.status = status
            rsvp.save()
            messages.success(request, f'RSVP updated to {status}.')
    else:
        RSVP.objects.create(user=request.user, event=event, status=status)
        messages.success(request, f'You are marked as {status}!')

    return redirect('events:detail', event_id=event_id)


@login_required
def rsvp_dashboard(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Only the organizer or admin can see this
    if request.user != event.organizer and not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('events:detail', event_id=event_id)

    going      = event.rsvps.filter(status=RSVP.Status.GOING).select_related('user')
    interested = event.rsvps.filter(status=RSVP.Status.INTERESTED).select_related('user')

    return render(request, 'events/dashboard.html', {
        'event':      event,
        'going':      going,
        'interested': interested,
    })