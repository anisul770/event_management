from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from users.forms import LoginForm,CustomRegistrationForm,CreateGroupForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test

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
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')
    except User.DoesNotExist:
        return HttpResponse('User not found')
 
@login_required   
def create_group(request):
    form = CreateGroupForm()
    if request.method=='POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request,f"Group {group.name} has been created successfully")
            return redirect('create-group')
    return render(request,'create_group.html',{'form':form})
