from django.urls import path
from . import views


urlpatterns = [
    # Web views
    path('', views.main),
    path('cv_page/<int:pk>/', views.cv_details, name="cv_page"),
    path('cv_page/<int:pk>/download/', views.download_cv_pdf, name="download_cv_pdf"),
    path('api/cvs/', views.CVListCreateView.as_view(), name='cv-list-create'),
    path('api/cvs/<int:pk>/', views.CVDetailView.as_view(), name='cv-detail'),
]
