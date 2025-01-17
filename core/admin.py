from django.contrib import admin
from .models import User

# אם המודל כבר רשום, אין צורך לרשום אותו שוב
try:
    admin.site.register(User)
except admin.sites.AlreadyRegistered:
    pass
