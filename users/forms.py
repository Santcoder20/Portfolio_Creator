from django import forms
from portfolio.models import Project, Skill, Certificate, Education, Resume, Experience, BackGround
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

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