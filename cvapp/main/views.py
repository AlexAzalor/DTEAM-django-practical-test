from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import CV
# Create your views here.


def main(request):
    cv_items = CV.objects.all()
    return render(request, 'index.html', {'cv_items': cv_items})


def cv_details(request, pk=None):
    if pk is None:
        raise Http404("CV ID is required")

    cv_item = get_object_or_404(CV, id=pk)

    context = {
        'cv_item': cv_item,
    }

    return render(request, 'cv_page.html', context)
