from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/add/', views.product_add, name='product_add'),
    path('admin-panel/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('admin-panel/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('admin-panel/toggle/<int:pk>/', views.product_toggle, name='product_toggle'),
]
