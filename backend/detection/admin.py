from django.contrib import admin
from .models import Hazard, Detection

# Register your models here.
admin.site.register(Hazard)
admin.site.register(Detection)