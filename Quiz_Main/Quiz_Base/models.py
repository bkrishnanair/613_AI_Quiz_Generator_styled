from django.db import models

class UploadedPDF(models.Model):
    pdf = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)