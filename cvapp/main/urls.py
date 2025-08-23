from django.urls import path
from . import views


urlpatterns = [
    path('', views.main),
    path('cv_page/<int:pk>/', views.cv_details, name="cv_page"),
    path('cv_page/<int:pk>/download/', views.download_cv_pdf, name="download_cv_pdf"),
]
