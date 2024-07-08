from django.contrib import admin

from .models import *
from .models import Plant, Hybrid, ContactMessage, PlantTransaction, HybridTransaction

admin.site.register(Plant)
admin.site.register(Hybrid)
admin.site.register(ContactMessage)
admin.site.register(PlantTransaction)
admin.site.register(HybridTransaction)