from django.urls import path
from . import views

app_name = 'legislation'

urlpatterns = [
    path('', views.LegislationListView.as_view(), name='list'),
    path('<int:pk>/', views.LegislationDetailView.as_view(), name='detail'),
]