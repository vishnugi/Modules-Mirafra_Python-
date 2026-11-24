from django.urls import path

from leave import views

urlpatterns = [
    path('apply/',views.apply_leave,name='apply_leave'),
    path('leave/',views.leave,name='leave'),
    path('status/',views.status,name='status'),
    path('personal-info',views.personal_info,name='personal_info')
]