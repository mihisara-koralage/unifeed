from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Listing, ListingImage, Report
from .forms import ListingForm, ReportForm

@login_required
def listing_browse(request):
    category = request.GET.get('category', '')
    search   = request.GET.get('search', '').strip()

    listings = Listing.objects.filter(
        is_active=True, is_approved=True
    ).select_related('seller').prefetch_related('images')

    if category and category in Listing.Category.values:
        listings = listings.filter(category=category)

    if search:
        listings = listings.filter(title__icontains=search) | \
                   listings.filter(description__icontains=search)

    return render(request, 'marketplace/browse.html', {
        'listings':   listings,
        'categories': Listing.Category.choices,
        'active_cat': category,
        'search':     search,
    })


@login_required
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, is_approved=True)
    already_reported = Report.objects.filter(
        reporter=request.user, listing=listing
    ).exists()

    return render(request, 'marketplace/detail.html', {
        'listing':          listing,
        'already_reported': already_reported,
    })


@login_required
def create_listing(request):
    if not request.user.is_student:
        messages.error(request, 'Only students can list items.')
        return redirect('marketplace:browse')

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()

            # Save up to 3 images
            for i, field_name in enumerate(['image_1', 'image_2', 'image_3']):
                img = form.cleaned_data.get(field_name)
                if img:
                    ListingImage.objects.create(listing=listing, image=img, order=i)

            messages.success(request, 'Listing posted successfully!')
            return redirect('marketplace:detail', listing_id=listing.id)
    else:
        form = ListingForm()

    return render(request, 'marketplace/create.html', {'form': form})


@login_required
def mark_sold(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, seller=request.user)
    listing.is_active = False
    listing.save()
    messages.success(request, 'Listing marked as sold.')
    return redirect('marketplace:browse')


@login_required
def report_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if listing.seller == request.user:
        messages.error(request, 'You cannot report your own listing.')
        return redirect('marketplace:detail', listing_id=listing_id)

    if Report.objects.filter(reporter=request.user, listing=listing).exists():
        messages.info(request, 'You have already reported this listing.')
        return redirect('marketplace:detail', listing_id=listing_id)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            Report.objects.create(
                reporter=request.user,
                listing=listing,
                reason=form.cleaned_data['reason'],
                details=form.cleaned_data.get('details', ''),
            )
            messages.success(request, 'Report submitted. Our team will review it.')
            return redirect('marketplace:detail', listing_id=listing_id)
    else:
        form = ReportForm()

    return render(request, 'marketplace/report.html', {
        'form':    form,
        'listing': listing,
    })