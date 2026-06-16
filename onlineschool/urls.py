"""
URL configuration for onlineschool project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from courses import views as courses_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Global aliases for exam submit/results to support non-namespaced template resolutions
    path('<int:course_id>/submit/', courses_views.submit, name='submit'),
    path('<int:course_id>/submit/', courses_views.submit, name='submit_exam'),
    path('course/<int:course_id>/submission/<int:submission_id>/result/', courses_views.show_exam_result, name='show_exam_result'),
    
    path('', include('courses.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

