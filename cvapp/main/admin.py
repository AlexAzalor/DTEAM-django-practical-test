from django.contrib import admin
from .models import CV, Skill, Project

# Register your models here.

admin.site.register(CV)
admin.site.register(Skill)
admin.site.register(Project)
