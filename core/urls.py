from django.urls import path
from core import views

urlpatterns = [
    # Index
    path('', views.Home.as_view(), name='home'),
    # Certificates
    path('cert/', views.CertList.as_view(), name='cert_list'),
    path('cert/create', views.CertCreate.as_view(), name='cert_create'),
    path('cert/<str:id>/edit', views.CertEdit.as_view(), name='cert_edit'),
    path('cert/<str:id>/delete', views.CertDelete.as_view(), name='cert_delete'),

    # Skills
    path('skill/', views.SkillList.as_view(), name='skill_list'),
    path('skill/create', views.SkillCreate.as_view(), name='skill_create'),
    path('skill/<str:id>/edit', views.SkillEdit.as_view(), name='skill_edit'),
    path('skill/<str:id>/delete', views.SkillDelete.as_view(), name='skill_delete'),

    # Authentication
    path('login', views.Login.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
]