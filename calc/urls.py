from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('logi',views.logi,name='logi'),
    path('sign',views.sign,name='sign'),
    path('home',views.home,name='home1'),
    path('main1',views.main1,name='main1'),
    path('logout',views.logout,name='logout'),
    path('upload',views.uploadfeedback,name='fb'),
    path('feedbackpage',views.viewfb,name='viewfb')
]