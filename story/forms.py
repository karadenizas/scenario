from django import forms
from django.contrib.auth.models import User
from .models import Profile, Comment, Post


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length = 16, widget= \
            forms.PasswordInput(attrs=\
            {'class': 'form-control', 'placeholder': 'password'}))

    password2 = forms.CharField(max_length = 16, widget= \
            forms.PasswordInput(attrs=\
            {'class': 'form-control', 'placeholder': 'repeat password'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username',
                                               'class': 'form-control', 
                                               'required': 'required'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email',
                                             'class': 'form-control', 
                                             'required': 'required'})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is exist! Please enter an another email address.')
        return self.cleaned_data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is exist! Please enter an another email address.')
        return self.cleaned_data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'enter a post', 'class': 'form-control', 'rows': '4'})
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status')
        widgets = {
            'title': forms.Textarea(attrs={'placeholder': 'enter a title', 'class': 'form-control', 'rows': '1'}),
            'body': forms.Textarea(attrs={'placeholder': 'enter a story', 'class': 'form-control', 'rows': '8'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }

    def clean(self):
        title = self.cleaned_data.get('title')
        if Post.objects.filter(title__iexact=title).exists():
            raise forms.ValidationError(f'This title is already exist! Please enter an another title or add a number at the end of the title. Etc.: {title} 1')
        return self.cleaned_data


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)