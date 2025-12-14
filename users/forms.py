import re
import string
from django.contrib.auth.models import Group,Permission,AbstractUser
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django import forms
from django.contrib.auth import get_user_model
from users.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style_widget()
        
    default_class = " py-2 w-full rounded-lg border-1 border-gray-400 shadow focus:bg-rose-100"
    def apply_style_widget(self):
        for field_name, field in self.fields.items():
            self.fields[field_name].help_text = None
            field.widget.attrs.update({
                'class' : self.default_class,
                
            })
            if field.label:
                field.widget.attrs.update({
                    'placeholder': f"Enter {field.label.lower()}"
                })
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : "space-y-2",
                })
                
                
class CustomRegistrationForm(StyleFormMixin,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password','confirm_password','email']
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []
         
        if len(password)<8:
            errors.append('Password mush be at least 8 characters long')
        if not re.search('[A-Z]', password):
            errors.append("Your password must contain at least one uppercase letter.")
        if not re.findall('[a-z]', password):
            errors.append("Your password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in password):
            errors.append("Your password must contain at least one number.")
        if not re.findall("[!@#$%^&*()-_+={}[]|\\;:'\"<>,./?]", password):
            errors.append("Your password must contain at least one special character.")
        if errors:
            raise forms.ValidationError(errors)
        
        return password
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exist = User.objects.filter(email=email).exists()
        
        if email_exist:
            raise forms.ValidationError("Email already exists")

        return email
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password do not match")
        
        return cleaned_data
        
        
class LoginForm(StyleFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class CreateGroupForm(StyleFormMixin,forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = 'Assign Permission'
    )
    
    class Meta:
        model = Group
        fields = ['name','permissions']

class AssignRoleForm(StyleFormMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label='Select a Role'
    )
    
class EditProfileForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','bio','profile_image','phone']
        
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not phone.isdigit():
                raise forms.ValidationError("Input Only digits")
        return phone
    
class CustomPasswordChangeForm(StyleFormMixin,PasswordChangeForm):
    pass

class CustomPasswordResetForm(StyleFormMixin,PasswordResetForm):
    pass

class CustomPasswordResetConfirmForm(StyleFormMixin,SetPasswordForm):
    pass