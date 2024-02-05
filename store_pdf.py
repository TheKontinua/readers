#For manually uploading PDFs to the db (testing)

import os
from django.core.wsgi import get_wsgi_application
from django.db import models
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentoris.settings')
application = get_wsgi_application()

from mentapp.models import Blob

def add_pdf_to_db(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        # Use Django's ContentFile to create a file-like object
        content_file = ContentFile(pdf_content, name=os.path.basename(pdf_path))

        blob_instance = Blob(
            file=content_file,
            content_type='application/pdf',
            filename=os.path.basename(pdf_path)
        )
        blob_instance.save()

        print("File added to the database successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    pdf_path = 'mentoris/dummy.pdf'
    add_pdf_to_db(pdf_path)
