from django.shortcuts import render, redirect, get_object_or_404
from event.models import Category, Event
from event.forms import CategoryForm,EventForm
from django.db.models import Q,Count
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User

# ----- CATEGORY -----

@login_required
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
    if request.method == 'POST' and 'delete_confirm' not in request.POST:
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

@login_required
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
    if request.method == 'POST' and 'delete_confirm' not in request.POST:
        eid = request.POST.get('id')
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location', '').strip()
        participant_ids = request.POST.getlist('participants')  # IMPORTANT: checkboxes => getlist
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
            event.participants.set(participant_ids)
        else:  # ✅ Creating new
            e = Event.objects.create(
                name=name,
                description=description,
                date=date,
                time=time,
                location=location,
                category_id=category_id
            )
            e.participants.set(participant_ids)
        return redirect('event_page')

    # LIST + SEARCH
    search = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category_filter', '').strip()

    events = Event.objects.select_related('category').prefetch_related('participants').all()

    if search:
        events = events.filter(Q(name__icontains=search) | Q(location__icontains=search))
    if category_filter:
        events = events.filter(category_id=category_filter)

    # No property conflict — rename annotationszd
    events = events.annotate(total_participants=Count('participants'))
    categories = Category.objects.all()
    total_participants = User.objects.count()
    context = {
        'events': events,
        'categories': categories,
        'selected': selected,
        'delete_item': delete_item,
        'search': search,
        'category_filter': category_filter,
        'total_participants': total_participants,
    }
    return render(request, 'event.html', context)

# Participant 
@login_required
def participant_page(request):
    selected, delete_item = None, None

    # DELETE
    if 'delete_confirm' in request.POST:
        User.objects.filter(id=request.POST['delete_confirm']).delete()
        return redirect('participant_page')

    # GET edit/delete actions
    if 'edit' in request.GET:
        selected = get_object_or_404(User, id=request.GET['edit'])
    elif 'delete' in request.GET:
        delete_item = get_object_or_404(User, id=request.GET['delete'])

    # CREATE / UPDATE
    if request.method == 'POST' and 'delete_confirm' not in request.POST:
        pid = request.POST.get('id', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        event_ids = request.POST.getlist('events')  # IMPORTANT: checkboxes => getlist

        if pid:
            p = get_object_or_404(User, id=pid)
            p.first_name = first_name
            p.last_name = last_name
            p.email = email
            p.save()
            p.events.set(event_ids)
        else:
            try:
                p = User.objects.create(first_name=first_name,last_name=last_name, email=email)
                p.events.set(event_ids)
            except Exception as e:
                messages.error(request,"Email already Exist")
                return redirect('participant_page')
        return redirect('participant_page')

    # LIST
    participants = User.objects.prefetch_related('events').all()
    events = Event.objects.select_related('category').all()

    return render(request, 'participant.html', {
        'participants': participants,
        'events': events,
        'selected': selected,
        'delete_item': delete_item,
    })
    
def event_list(request):
    events = Event.objects.select_related('category').all()
    return render(request,'event_list.html',{'events':events})