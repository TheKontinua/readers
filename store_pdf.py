import os
from django.core.wsgi import get_wsgi_application
from django.db import models
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentoris.settings')
application = get_wsgi_application()

from mentapp.models import Blob  

def add_pdf_to_db(pdf_path):
    # Read the PDF file content
    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()

    # Create an instance of Blob and save it to the database
    blob_instance = Blob(
        binary_data=pdf_content,
        content_type='application/pdf',
        filename=os.path.basename(pdf_path)
    )
    blob_instance.save()

if __name__ == "__main__":
    pdf_path = 'mentoris/dummy.pdf'
    
    add_pdf_to_db(pdf_path)
