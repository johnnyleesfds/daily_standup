from django.contrib import admin
from .models import *
from django.urls import resolve
import datetime

# Register your models here.
current_week = datetime.date.today().isocalendar()[1]


# current_week = self.model.standup.week

class AccomplishmentInline(admin.TabularInline):
    model = Accomplishment
    fields = ("description", "goal")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(AccomplishmentInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "goal":
            # current_week = self.model.standup.week
            if request._obj_ is not None:
                week = request._obj_.week
                field.queryset = Goal.objects.filter(date__week=week).order_by("tracker__product_feature",
                                                                               'name')
            else:
                field.queryset = Goal.objects.filter(date__week=current_week).order_by("tracker__product_feature",
                                                                                       'name')
        return field


class WorkingOnAdmin(admin.TabularInline):
    model = WorkingOn
    fields = ("description", "goal")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(WorkingOnAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "goal":
            # current_week = self.model.standup.week
            if request._obj_ is not None:
                week = request._obj_.week
                field.queryset = Goal.objects.filter(date__week=week).order_by("tracker__product_feature",
                                                                               'name')
            else:
                field.queryset = Goal.objects.filter(date__week=current_week).order_by("tracker__product_feature",
                                                                                       'name')
        return field


class BlockerAdmin(admin.TabularInline):
    model = Blocker
    fields = ("description", "goal")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(BlockerAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "goal":
            # current_week = self.model.standup.week
            if request._obj_ is not None:
                week = request._obj_.week
                field.queryset = Goal.objects.filter(date__week=week).order_by("tracker__product_feature",
                                                                               'name')
            else:
                field.queryset = Goal.objects.filter(date__week=current_week).order_by("tracker__product_feature",
                                                                                       'name')
        return field


class StandupAdmin(admin.ModelAdmin):
    model = Standup
    inlines = [AccomplishmentInline, WorkingOnAdmin, BlockerAdmin]
    list_display = ["person", "date"]

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(StandupAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(StandupAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(person__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "person":
            kwargs["queryset"] = Person.objects.all() if request.user.is_superuser else Person.objects.filter(
                user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Standup, StandupAdmin)
