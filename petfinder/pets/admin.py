from django.contrib import admin
from .models import *


class DetailAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_added_by', 'email', 'country', 'forbidden_countries', 'peepalfarm_approved',
                    'is_adopted', 'enabled']
    list_display_links = ['name']
    search_fields = ['name', 'email']

    def get_added_by(self, obj):
        return obj.added_by.username

    get_added_by.short_description = 'Added by'
    get_added_by.admin_order_field = 'added_by'


# Register your models here.
admin.site.register(Detail, DetailAdmin)
admin.site.register(Media)
admin.site.register(Query)
