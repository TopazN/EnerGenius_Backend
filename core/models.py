from django.db import models

class UserFile(models.Model):
    user = models.CharField(max_length=100)  # שם משתמש
    uploaded_file = models.FileField(upload_to='uploads/')  # קובץ Excel
    uploaded_at = models.DateTimeField(auto_now_add=True)  # תאריך העלאה