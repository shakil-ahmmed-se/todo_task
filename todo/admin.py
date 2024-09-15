from django.contrib import admin
from .models import Todo,Profile,PriorityChoices
# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed')

class PriorityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display=['name','slug']

admin.site.register(Todo, TodoAdmin)
admin.site.register(Profile)
admin.site.register(PriorityChoices)