from django.contrib import admin
from .models import *
from trackers.models import *
from django.forms import TextInput, Textarea
# Register your models here.

class GoalAdmin(admin.ModelAdmin):
    list_display = ('date', 'tracker','name')
    list_editable = ('date', 'tracker', 'name')
    list_display_links = None

    # formfield_overrides = {
    #     models.CharField: {'widget': TextInput(attrs={'size':'150'})},
    # }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tracker":
            kwargs["queryset"] = Tracker.objects.all().order_by('product_feature')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Goal, GoalAdmin)