from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


class ChoiceInline(admin.TabularInline):
    """Inline admin for Choice model within Question admin."""
    model = Choice
    extra = 3
    fields = ('choice_text', 'is_correct')


class QuestionInline(admin.StackedInline):
    """Inline admin for Question model within Lesson admin."""
    model = Question
    extra = 1
    fields = ('question_text', 'points')
    show_change_link = True


class LessonInline(admin.StackedInline):
    """Inline admin for Lesson model within Course admin."""
    model = Lesson
    extra = 1
    fields = ('title', 'content', 'order')


class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for Question model."""
    list_display = ('question_text', 'lesson', 'points')
    list_filter = ('lesson', 'points')
    search_fields = ('question_text', 'lesson__title')
    inlines = [ChoiceInline]
    fieldsets = (
        (None, {
            'fields': ('lesson', 'question_text', 'points')
        }),
    )


class ChoiceAdmin(admin.ModelAdmin):
    """Admin configuration for Choice model."""
    list_display = ('choice_text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__lesson')
    search_fields = ('choice_text', 'question__question_text')


class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for Lesson model."""
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('course', 'order')
    inlines = [QuestionInline]
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'content', 'order')
        }),
    )


class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for Course model."""
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')
    inlines = [LessonInline]


class SubmissionAdmin(admin.ModelAdmin):
    """Admin configuration for Submission model."""
    list_display = ('user', 'lesson', 'submitted_at', 'score', 'total_points')
    list_filter = ('submitted_at', 'lesson')
    search_fields = ('user__username', 'lesson__title')


class InstructorAdmin(admin.ModelAdmin):
    """Admin configuration for Instructor model."""
    list_display = ('user', 'expertise')
    search_fields = ('user__username', 'expertise')


class LearnerAdmin(admin.ModelAdmin):
    """Admin configuration for Learner model."""
    list_display = ('user', 'date_of_birth')
    search_fields = ('user__username',)


# Register exactly the seven models with the admin site
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)

# Customize admin site header and title
admin.site.site_header = 'Online School Administration'
admin.site.site_title = 'Online School Admin'
admin.site.index_title = 'Welcome to Online School Admin Portal'

