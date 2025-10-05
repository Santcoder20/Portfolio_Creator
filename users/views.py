from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProjectForm, SkillForm, SignUpForm, LoginForm, ProfileForm, CertificateForm, ExperienceForm, ResumeForm, EducationForm, BackGroundForm
from portfolio.models import Project, Skill, Education, Experience, Certificate, Resume, BackGround
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from .models import OTPVerification
import random
from django.contrib import messages
from django.conf import settings


def verify_otp(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')
        signup_data = request.session.get('signup_data')

        if not signup_data:
            messages.error(request, "No signup data found. Please try again.")
            return redirect('users:signup')

        email = signup_data['email']
        real_otp = otp_store.get(email)

        if real_otp and str(input_otp) == str(real_otp):
            # Create user
            user = User.objects.create_user(
                username=signup_data['username'],
                email=signup_data['email'],
                password=signup_data['password1'],
                first_name=signup_data.get('first_name', ''),
                last_name=signup_data.get('last_name', ''),
            )
            # Optional: clear OTP and session data
            otp_store.pop(email, None)
            request.session.pop('signup_data', None)

            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('users:login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'users/verify_otp.html')


def public_index(request):
    users = User.objects.all()[:20]
    return render(request, 'users/public_index.html', {'users': users})


otp_store = {}


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            otp = random.randint(100000, 999999)

            # store OTP temporarily
            otp_store[email] = otp

            # Compose a welcoming email with OTP
            subject = 'Welcome to Portfolio Creator! Your OTP Inside'
            message = f"""
Hi there!

Welcome to Portfolio Creator! 🎉

Your One-Time Password (OTP) to complete the signup process is: {otp}

Please enter this OTP on the verification page to finish creating your account.

Thank you for joining us and happy portfolio building!

— The Portfolio Creator Team
"""
            # Send OTP to email
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,  # set True if you don't want server errors to show
            )

            # Save form data for OTP verification step
            request.session['signup_data'] = form.cleaned_data
            return redirect('users:verify_otp')
    else:
        form = SignUpForm()

    return render(request, 'users/signup.html', {'form': form})

class log_in(LoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'


def user_portfolio(request, username):
    user = get_object_or_404(User, username=username)
    profile = getattr(user, 'profile', None)
    projects = Project.objects.filter(user=user)
    skills = Skill.objects.filter(user=user)
    education = Education.objects.filter(user=user)
    experience = Experience.objects.filter(user=user)
    certificate = Certificate.objects.filter(user=user)
    resume = Resume.objects.filter(user=user)
    background = BackGround.objects.filter(user=user).first()
    return render(request, 'users/user_portfolio.html', {
        'owner': user, 'profile': profile, 'projects': projects,'skills': skills, 'education': education,
        'experience': experience, 'certificate': certificate, 'resume': resume, 'background': background,
    })

def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = getattr(user, 'profile', None)
    return render(request, 'users/profile_detail.html', {'user': user, 'profile': profile})

def education_detail(request, pk):
    education = get_object_or_404(Education, pk=pk)
    return render(request, 'users/education_detail.html', {'education': education})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'users/project_detail.html', {'project': project})

def skill_detail(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    return render(request, 'users/skill_detail.html', {'skill': skill})

def experience_detail(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    return render(request, 'users/experience_detail.html', {'experience': experience})

def certificate_detail(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    return render(request, 'users/certificate_detail.html', {'certificate': certificate})

def resume_detail(request):
    resume, created = Resume.objects.get_or_create(user=request.user)
    return render(request, 'users/resume_detail.html', {'resume': resume})

def background_detail(request):
    background, created = BackGround.objects.get_or_create(user=request.user)
    return render(request, 'users/background_details.html', {'background': background})

@login_required
def dashboard(request):
    profile = request.user.profile
    projects = Project.objects.filter(user=request.user)
    skills = Skill.objects.filter(user=request.user)
    education = Education.objects.filter(user=request.user)
    experience = Experience.objects.filter(user=request.user)
    certificate = Certificate.objects.filter(user=request.user)
    resume = Resume.objects.filter(user=request.user)
    background = BackGround.objects.filter(user=request.user)
    return render(request, 'users/dashboard.html', {
        'profile': profile, 'projects': projects, 'skills': skills, 'education': education, 'experience': experience ,
        'certificate': certificate, 'resume': resume, 'background': background
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('users:dashboard')
    else:
        form = EducationForm()
    return render(request, 'users/add_education.html', {'form': form})

@login_required
def edit_education(request, pk):
    education = get_object_or_404(Education, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('users:dashboard')
    else:
        form = EducationForm(instance=education)
    return render(request, 'users/edit_education.html', {'form': form})

@login_required
def delete_education(request, pk):
    education = get_object_or_404(Education, pk=pk, user=request.user)
    if request.method == 'POST':
        education.delete()
        return redirect('users:dashboard')
    return render(request, 'users/confirm_delete.html', {'object': education, 'type': 'education'})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('users:dashboard')
    else:
        form = ProjectForm()
    return render(request, 'users/add_project.html', {'form': form})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('users:dashboard')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'users/edit_project.html', {'form': form})
@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('users:dashboard')
    return render(request, 'users/confirm_delete.html', {'object': project, 'type': 'project'})

@login_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            return redirect('users:dashboard')
    else:
        form = SkillForm()
    return render(request, 'users/add_skill.html', {'form': form})

@login_required
def edit_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, request.FILES, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('users:dashboard')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'users/edit_skill.html', {'form': form})

@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        skill.delete()
        return redirect('users:dashboard')
    return render(request, 'users/confirm_delete.html', {'object': skill, 'type': 'skill'})


@login_required
def add_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.user = request.user
            certificate.save()
            return redirect('users:dashboard')
    else:
        form =  CertificateForm()
    return render(request, 'users/add_certificate.html', {'form': form})

@login_required
def edit_certificate(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES, instance=certificate)
        if form.is_valid():
            form.save()
            return redirect('users:dashboard')
    else:
        form = CertificateForm(instance=certificate)
    return render(request, 'users/edit_certificate.html', {'form': form})

@login_required
def delete_certificate(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk, user=request.user)
    if request.method == 'POST':
        certificate.delete()
        return redirect('users:dashboard')
    return render(request, 'users/confirm_delete.html', {'object': certificate, 'type': 'certificate'})


@login_required
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            return redirect('users:dashboard')
    else:
        form =  ExperienceForm()
    return render(request, 'users/add_experience.html', {'form': form})

@login_required
def edit_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, request.FILES, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('users:dashboard')
    else:
        form = ExperienceForm(instance=experience)
    return render(request, 'users/edit_experience.html', {'form': form})

@login_required
def delete_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk, user=request.user)
    if request.method == 'POST':
        experience.delete()
        return redirect('users:dashboard')
    return render(request, 'users/confirm_delete.html', {'object': experience, 'type': 'experience'})

@login_required
def edit_resume(request):
    # Get existing resume or create a new one if it doesn't exist
    resume, created = Resume.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('users:dashboard')
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'users/edit_resume.html', {'form': form})



@login_required
def delete_resume(request):
    resume = get_object_or_404(Resume, user=request.user)
    if request.method == 'POST':
        resume.delete()
        return redirect('users:dashboard')
    return render(request, 'users/confirm_delete.html', {'object': resume, 'type': 'resume'})

@login_required
def edit_background(request):
    background, created = BackGround.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = BackGroundForm(request.POST, request.FILES, instance=background)
        if form.is_valid():
            form.save()
            return redirect('users:dashboard')
    else:
        form = BackGroundForm(instance=background)
    return render(request, 'users/edit_background.html', {'form': form})

@login_required
def delete_background(request):
    background = get_object_or_404(BackGround, user=request.user)
    file_type = request.GET.get('type')

    if request.method == 'POST':
        if file_type == 'main' and background.main_file:
            background.main_file.delete(save=True)
        elif file_type == 'sidebar' and background.sidebar_file:
            background.sidebar_file.delete(save=True)
        return redirect('users:background_detail')

    object_name = background.main_file.name if file_type == 'main' else background.sidebar_file.name
    type_name = "Main File" if file_type == 'main' else "Sidebar File"
    return render(request, 'users/confirm_delete.html', {'object': object_name, 'type': type_name})
