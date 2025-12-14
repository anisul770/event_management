from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from users.forms import LoginForm,CustomRegistrationForm,CreateGroupForm,AssignRoleForm,EditProfileForm,CustomPasswordChangeForm,CustomPasswordResetConfirmForm,CustomPasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from core.templatetags.role_filters import is_admin,is_organizer,is_participant
from event.models import Event
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,TemplateView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

User = get_user_model()


class EditProfileView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'
    context_object_name = 'form'
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save()
        return redirect('profile')
    
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


class CustomSignUp(CreateView):
    form_class = CustomRegistrationForm
    context_object_name = 'form'
    template_name = 'sign_up.html'
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.is_active = False
        user.save()
        messages.success(self.request,"A Confirmation mail sent. Please check the email")
        return redirect('sign-in')     
        

def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
        
    return render(request,'sign_in.html',{'form':form})

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'sign_in.html'

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
            if not user.password or not user.has_usable_password():
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

create_group_decorator = [login_required,user_passes_test(is_admin,login_url='no-permission')]
@method_decorator(create_group_decorator,name='dispatch')
class CreateGroupView(CreateView):
    form_class = CreateGroupForm
    context_object_name = 'form'
    template_name = 'create_group.html'
    
    def form_valid(self, form):
        group = form.save()
        messages.success(self.request,f"Group {group.name} has been created successfully")
        return redirect('create-group')
    

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
@user_passes_test(is_participant,login_url='no-permission')
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


@method_decorator(create_group_decorator,name='dispatch')
class GroupView(ListView):
    model = Group
    template_name = 'group_list.html'
    context_object_name = 'groups'
    
    def post(self,request,*args, **kwargs):
        if "delete_group" in request.POST:
            group_id = request.POST.get("group_id")
            group = Group.objects.filter(id=group_id).first()
            if group:
                group.delete()
                messages.success(request, f"Group '{group.name}' deleted successfully!")
            return redirect('group-list')
    


def profile(request):
    return render(request,'profile.html')

class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['group'] = user.groups.first().name
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        context['phone'] = user.phone

        return context
    
class ChangePassword(LoginRequiredMixin,PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = CustomPasswordChangeForm
    
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "reset_password.html"
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'reset_email.html'
    
    def form_valid(self, form):
        messages.success(self.request,"A reset email has been sent. Please check your email")
        return super().form_valid(form)
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = "reset_password.html"
    success_url = reverse_lazy('sign-in')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocol"] = "https" if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context
    
    def form_valid(self, form):
        messages.success(self.request,"Password reset successfully")
        return super().form_valid(form)
    