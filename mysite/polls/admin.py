from django.contrib import admin

# Register your models here.
from .models import Question,Choice
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        export_order = ('id', 'question_text', 'status', 'language', 'headImg', 'is_disabled', 'pub_date')


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(ImportExportModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        (None,               {'fields': ['status']}),
        (None,               {'fields': ['language']}),
        (None,               {'fields': ['headImg']}),
        (None,               {'fields': ['is_disabled']}),
        (None,               {'fields': ['content']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # inlines = [ChoiceInline]

    list_display = ('question_text', 'pub_date', 'was_published_recently', 'status', 'language', 'head_img_thumb','is_disabled')
    search_fields = ('question_text',)
    list_filter = ['pub_date', 'status', 'language','is_disabled']
    date_hierarchy = 'pub_date'
    resource_class = QuestionResource


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
