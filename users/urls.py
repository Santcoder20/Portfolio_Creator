from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.public_index, name='public_index'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/edit', views.edit_profile, name='edit_profile'),
    #add_details
    path('dashboard/add_education', views.add_education, name='add_education'),
    path('dashboard/add-project', views.add_project, name='add_project'),
    path('dashboard/add-skill', views.add_skill, name='add_skill'),
    path('dashboard/add-experience', views.add_experience, name='add_experience'),
    path('dashboard/add_certificate', views.add_certificate, name='add_certificate'),
    path('dashboard/resume', views.edit_resume, name='edit_resume'),
    path('background/edit', views.edit_background, name='edit_background'),
    #view_details
    path('education/<int:pk>', views.education_detail, name='education_detail'),
    path('project/<int:pk>', views.project_detail, name='project_detail'),
    path('skill/<int:pk>', views.skill_detail, name='skill_detail'),
    path('certificate/<int:pk>', views.certificate_detail, name='certificate_detail'),
    path('experience/<int:pk>', views.experience_detail, name='experience_detail'),
    path('resume', views.resume_detail, name='resume_detail'),
    path('background', views.background_detail, name='background_detail'),
    #edit_details
    path('education/<int:pk>/edit', views.edit_education, name='edit_education'),
    path('project/<int:pk>/edit', views.edit_project, name='edit_project'),
    path('skill/<int:pk>/edit', views.edit_skill, name='edit_skill'),
    path('certificate/<int:pk>/edit', views.edit_certificate, name='edit_certificate'),
    path('experience/<int:pk>/edit', views.edit_experience, name='edit_experience'),
    #delete_details
    path('project/<int:pk>/delete', views.delete_project, name='delete_project'),
    path('skill/<int:pk>/delete', views.delete_skill, name='delete_skill'),
    path('education/<int:pk>/delete', views.delete_education, name='delete_education'),
    path('experience/<int:pk>/delete', views.delete_experience, name='delete_experience'),
    path('certificate/<int:pk>/delete', views.delete_certificate, name='delete_certificate'),
    path('resume/delete', views.delete_resume, name='delete_resume'),

]