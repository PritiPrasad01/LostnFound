
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm,UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import Post,Profile,Comment
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation

GENDER_CHOICES = (
    ('Male','Male'),
    ('Female','Female'),
    ('Prefer Not to Say','Prefer Not to Say'),
)
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    password1 = forms.CharField(label='Password')
    password2 = forms.CharField(label='Confirm Password')
    email = forms.CharField(required=True)
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    phone_num = forms.IntegerField(max_value=9999999999,min_value=1000000000)
    gender = forms.ChoiceField(choices = GENDER_CHOICES)
    profile_pic = forms.ImageField()
    class Meta:
        model = User
        fields = [
            'first_name','last_name','username',
            'email','phone_num','birth_date',
            'gender','password1','password2','profile_pic'
            ]
        labels = {'email':'Email'}
        # widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label=_('New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField( label=_("Email"), max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email'}))
    

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['user','created_at']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_num','gender','birth_date','profile_pic']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']