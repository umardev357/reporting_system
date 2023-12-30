from django.contrib import admin

# Register your models here.

from .models import Job, Personnel, JobCategory, Equipment, Substation, MonthContainer

admin.site.register(Job)
admin.site.register(Personnel)
admin.site.register(JobCategory)
admin.site.register(Equipment)
admin.site.register(Substation)
admin.site.register(MonthContainer)