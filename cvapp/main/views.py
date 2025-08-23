from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from .models import CV
import pdfkit
import tempfile
import os


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


def download_cv_pdf(request, pk):
    cv_item = get_object_or_404(CV, id=pk)

    try:
        # Create a temporary file for the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = tmp_file.name

        context = {'cv_item': cv_item}
        html_string = render_to_string('cv_page_pdf.html', context, request)

        pdfkit.from_string(html_string, pdf_path)

        with open(pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        # Clean up the temporary file
        os.unlink(pdf_path)

        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{cv_item.full_name}_CV.pdf"'

        return response

    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)
