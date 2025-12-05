from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from users.forms import LoginForm,CustomRegistrationForm,CreateGroupForm,AssignRoleForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from core.templatetags.role_filters import is_admin,is_organizer,is_participant
from event.models import Event

# Create your views here.

def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST': 
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            messages.success(request,"A Confirmation mail sent. Please check the email")
            return redirect('sign-in')      
        else:
            print("Form is not valid")
    return render(request,'sign_up.html',{'form':form})


def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        print(form)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
        
    return render(request,'sign_in.html',{'form':form})

@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign-in')
    

def activate_user(request,user_id,token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            if not user.has_usable_password():
                user.set_password('12345')  
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')
    except User.DoesNotExist:
        return HttpResponse('User not found')
 
@login_required   
@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method=='POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request,f"Group {group.name} has been created successfully")
            return redirect('create-group')
    return render(request,'create_group.html',{'form':form})

@login_required
@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request,user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if  request.method=='POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,f"User {user.username} has been assigned to the {role.name} role")
            return redirect('participant_page')
    return render(request,'admin/assign_role.html',{'form': form})

@login_required
def respond(request, e_id):
    event = get_object_or_404(Event, id=e_id)
    user = request.user
    if event.participants.filter(id=user.id).exists():
        messages.error(request, "You have already responded to this event!")
        return redirect('event-list')
    event.participants.add(user)
    messages.success(request, f"You are now going to '{event.name}'.")
    return redirect('event-list')

@login_required
def cancel_response(request, e_id):
    event = get_object_or_404(Event, id=e_id)
    user = request.user

    if not event.participants.filter(id=user.id).exists():
        messages.error(request, "You are not participating in this event!")
        return redirect('event-list')

    event.participants.remove(user)
    messages.success(request, f"You have cancelled your participation for '{event.name}'.")
    return redirect('event-list')

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.all()

    if request.method == "POST" and "delete_group" in request.POST:
        group_id = request.POST.get("group_id")
        group = Group.objects.filter(id=group_id).first()
        if group:
            group.delete()
            messages.success(request, f"Group '{group.name}' deleted successfully!")
        return redirect('group-list')

    return render(request, 'group_list.html', {'groups': groups})
