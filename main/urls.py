from django.urls import path
from .import views
urlpatterns = [
    path('', views.index,name='main'),
    path('promenya', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('inprogress', views.inprogress, name='inprogress'),
    path('account/', views.view_account, name='view_account'),
    path('account/edit/', views.edit_account, name='edit_account'),
]
