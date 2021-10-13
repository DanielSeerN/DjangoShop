from django.contrib import admin
from .models import *
from django import forms


class SmartphoneAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug='smartphone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class LawnMoverAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug='lawnmover'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ConditionerAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug='conditioner'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TVAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug='tv'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PhotoCameraAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug='photocamera'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class WashingMachineAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug='washingmachine'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class VideoGameConsoleAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug='videogameconsole'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


models_ = [Category, SmartPhone, PhotoCamera, TV, LawnMover, WashingMachine, Conditioner, VideoGameConsole, CartProduct,
           Cart, Customer, Order]
for model in models_:
    if model == SmartPhone:
        admin.site.register(model, SmartphoneAdmin)
    elif model == TV:
        admin.site.register(model, TVAdmin)
    elif model == PhotoCamera:
        admin.site.register(model, PhotoCameraAdmin)
    elif model == LawnMover:
        admin.site.register(model, LawnMoverAdmin)
    elif model == WashingMachine:
        admin.site.register(model, WashingMachineAdmin)
    elif model == Conditioner:
        admin.site.register(model, ConditionerAdmin)
    elif model == VideoGameConsole:
        admin.site.register(model, VideoGameConsoleAdmin)
    else:
        admin.site.register(model)