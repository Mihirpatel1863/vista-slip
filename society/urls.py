from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_with_pin, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('block/<int:block_id>/', views.block_detail, name='block_detail'),
    path('create-slip/', views.create_slip, name='create_slip'),
    path('create-slip/<int:block_id>/', views.create_slip, name='create_slip_block'),
    path('create-slip/<int:block_id>/available-residents/', views.get_available_residents_ajax, name='available_residents'),
    path('slip/<int:pk>/', views.slip_detail, name='slip_detail'),
]
