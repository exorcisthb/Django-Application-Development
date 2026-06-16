from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('courses/<int:lesson_id>/submit/', views.submit, name='submit_exam'),
    path('submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
]
