from django.shortcuts import render, redirect, get_object_or_404
from event.models import Category, Event, Participant
from event.forms import CategoryForm,EventForm,ParticipantForm
from django.db.models import Q,Count
from django.utils import timezone
from django.contrib import messages

# ----- CATEGORY -----
def category_page(request):
    selected, delete_item = None, None

    # DELETE
    if 'delete_confirm' in request.POST:
        Category.objects.filter(id=request.POST['delete_confirm']).delete()
        return redirect('category_page')

    # EDIT / DELETE
    if 'edit' in request.GET:
        selected = get_object_or_404(Category, id=request.GET['edit'])
    elif 'delete' in request.GET:
        delete_item = get_object_or_404(Category, id=request.GET['delete'])

    # CREATE / UPDATE
    elif request.method == 'POST' and 'delete_confirm' not in request.POST:
        cid = request.POST.get('id', '').strip()
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if cid:
            category = get_object_or_404(Category, id=cid)
            category.name = name
            category.description = description
            category.save()
        else:
            Category.objects.create(name=name, description=description)
        return redirect('category_page')

    categories = Category.objects.all().order_by('name')

    return render(request, 'category.html', {
        'categories': categories,
        'selected': selected,
        'delete_item': delete_item,
    })



# ----- EVENT -----

def event_page(request):
    selected, delete_item = None, None

    # DELETE
    if 'delete_confirm' in request.POST:
        Event.objects.filter(id=request.POST['delete_confirm']).delete()
        return redirect('event_page')

    # EDIT / DELETE
    if 'edit' in request.GET:
        selected = get_object_or_404(Event, id=request.GET['edit'])
    elif 'delete' in request.GET:
        delete_item = get_object_or_404(Event, id=request.GET['delete'])

    # CREATE / UPDATE
    elif request.method == 'POST' and 'delete_confirm' not in request.POST:
        eid = request.POST.get('id')
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location', '').strip()
        category_id = request.POST.get('category')

        if eid:  # ✅ Updating existing
            event = get_object_or_404(Event, id=eid)
            event.name = name
            event.description = description
            event.date = date
            event.time = time
            event.location = location
            event.category_id = category_id
            event.save()
        else:  # ✅ Creating new
            Event.objects.create(
                name=name,
                description=description,
                date=date,
                time=time,
                location=location,
                category_id=category_id
            )

        return redirect('event_page')

    # LIST + SEARCH
    search = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category_filter', '').strip()

    events = Event.objects.select_related('category').prefetch_related('participants').all()

    if search:
        events = events.filter(Q(name__icontains=search) | Q(location__icontains=search))
    if category_filter:
        events = events.filter(category_id=category_filter)

    # No property conflict — rename annotation
    events = events.annotate(total_participants=Count('participants'))
    categories = Category.objects.all()
    total_participants = Participant.objects.count()

    return render(request, 'event.html', {
        'events': events,
        'categories': categories,
        'selected': selected,
        'delete_item': delete_item,
        'search': search,
        'category_filter': category_filter,
        'total_participants': total_participants,
    })

# Participant 

def participant_page(request):
    selected, delete_item = None, None

    # DELETE
    if 'delete_confirm' in request.POST:
        Participant.objects.filter(id=request.POST['delete_confirm']).delete()
        return redirect('participant_page')

    # GET edit/delete actions
    if 'edit' in request.GET:
        selected = get_object_or_404(Participant, id=request.GET['edit'])
    elif 'delete' in request.GET:
        delete_item = get_object_or_404(Participant, id=request.GET['delete'])

    # CREATE / UPDATE
    elif request.method == 'POST' and 'delete_confirm' not in request.POST:
        pid = request.POST.get('id', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        event_ids = request.POST.getlist('events')  # IMPORTANT: checkboxes => getlist

        if pid:
            p = get_object_or_404(Participant, id=pid)
            p.name = name
            p.email = email
            p.save()
            p.events.set(event_ids)
        else:
            p = Participant.objects.create(name=name, email=email)
            p.events.set(event_ids)
        return redirect('participant_page')

    # LIST
    participants = Participant.objects.prefetch_related('events').all()
    events = Event.objects.select_related('category').all()

    return render(request, 'participant.html', {
        'participants': participants,
        'events': events,
        'selected': selected,
        'delete_item': delete_item,
    })