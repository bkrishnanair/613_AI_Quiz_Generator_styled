
from django.contrib import admin
from .models import UploadedPDF

class UploadedPDFAdmin(admin.ModelAdmin):
    list_display = ('pdf', 'uploaded_at')  # Ensure these fields exist in UploadedPDF

admin.site.register(UploadedPDF, UploadedPDFAdmin)
