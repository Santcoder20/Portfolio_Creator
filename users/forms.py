from django import forms
from portfolio.models import Project, Skill, Certificate, Education, Resume, Experience, BackGround
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django.contrib.auth import authenticate


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            # Try to find user by email first
            try:
                user_obj = User.objects.get(email__iexact=username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                username = username_or_email  # fallback to username

            self.user_cache = authenticate(
                self.request, username=username, password=password
            )

            if self.user_cache is None:
                raise ValidationError(
                    "Please enter a correct username/email and password."
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        if  User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user





class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('full_name', 'bio', 'about', 'profile_pic', 'phone_number', 'linkedin', 'github', 'instagram','whatsapp' ,'location')

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'link', 'image', 'video']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']

class CertificateForm(forms.ModelForm):
    issue_date = forms.DateField(
        input_formats=['%d/%m/%Y'],  # Accepts DD/MM/YYYY format
        widget=forms.DateInput(format='%d/%m/%Y')
    )
    class Meta:
        model = Certificate
        fields = ['title', 'organization', 'issue_date', 'certificate_file']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'score_type', 'score', 'start_year', 'end_year']

    score_type = forms.ChoiceField(
        choices=Education.SCORE_TYPE_CHOICES,
        initial=Education.CGPA,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    score = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01})
    )
    start_year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    end_year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    institution = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    degree = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class ExperienceForm(forms.ModelForm):
    start_date = forms.DateField(
        input_formats=['%d/%m/%Y'],  # Accepts DD/MM/YYYY format
        widget=forms.DateInput(format='%d/%m/%Y')
    )
    end_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y'),
        required=False
    )
    class Meta:
        model = Experience
        fields = ['company','position', 'start_date', 'end_date','description']

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume_file', 'resume_link']

class BackGroundForm(forms.ModelForm):
    class Meta:
        model = BackGround
        fields = ['main_file', 'sidebar_file']