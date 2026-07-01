from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Resource
from .forms import ResourceForm

@login_required
def resource_list(request):
    category = request.GET.get('category', '')  # from sidebar filter
    search   = request.GET.get('search', '').strip()

    resources = Resource.objects.filter(
        is_approved=True
    ).select_related('contributor')

    # Filter by category if one is selected
    if category and category in Resource.Category.values:
        resources = resources.filter(category=category)

    # Search by title or description
    if search:
        resources = resources.filter(title__icontains=search) | \
                    resources.filter(description__icontains=search)

    return render(request, 'resources/list.html', {
        'resources':  resources,
        'categories': Resource.Category.choices,
        'active_cat': category,
        'search':     search,
    })


@login_required
def submit_resource(request):
    # Only students can submit
    if not request.user.is_student:
        messages.error(request, 'Only students can submit resources.')
        return redirect('resources:list')

    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.contributor = request.user
            resource.save()
            messages.success(request, 'Resource submitted successfully!')
            return redirect('resources:list')
    else:
        form = ResourceForm()

    return render(request, 'resources/submit.html', {'form': form})


@login_required
def open_resource(request, resource_id):
    # Safe redirect — opens the external URL in a new tab via the template
    resource = get_object_or_404(Resource, id=resource_id, is_approved=True)
    return render(request, 'resources/redirect.html', {'resource': resource})