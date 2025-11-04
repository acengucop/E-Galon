from django.contrib import admin
from .models import Depot

@admin.register(Depot)
class DepotAdmin(admin.ModelAdmin):
    list_display = ('nama', 'alamat', 'latitude', 'longitude', 'stok_galon')
    search_fields = ('nama', 'alamat')
    list_filter = ('stok_galon',)
