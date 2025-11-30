from django.contrib import admin
from .models import (UserProfile,Category,SubCategory,Course,Lesson,Assignment,Exam,Question,
                     Option,Certificate,Review)
from modeltranslation.admin import TranslationAdmin

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

@admin.register( Course,Lesson,Assignment,Exam,Question,Option)
class ProductAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    inlines = [SubCategoryInline]


admin.site.register(UserProfile)
admin.site.register(Certificate)
admin.site.register(Review)