from django.contrib import admin

from brms_app.models import Book
admin.site.register(Book)

from brms_app.models import BRMSuser
admin.site.register(BRMSuser)
