from django.urls import path
from . import views

urlpatterns = [
    path('score/', views.UserContentScoreUpdateCreateApiview.as_view(), name='add_content_score'),
    path('', views.ContentListApiview.as_view(), name='content_list'),
]
