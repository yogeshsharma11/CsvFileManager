from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.register_view,name='register'),
    path('',views.login_view,name='login'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('edit/<int:file_id>/', views.edit_data, name='edit_data'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('view-file/<int:file_id>/', views.view_file_data, name='view_file_data'),

]