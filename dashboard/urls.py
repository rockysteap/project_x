from django.urls import path

from dashboard import views

urlpatterns = [
    path('', views.RedirectToNews.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('news/', views.ShowNews.as_view(), name='news'),
    path('courses/', views.ShowCourses.as_view(), name='courses'),
    path('courses/<slug:course_slug>/', views.ShowCourseTeachers.as_view(), name='course'),
    path('news/add_article', views.AddArticle.as_view(), name='add_article'),
    path('news/<slug:article_slug>/', views.ShowArticle.as_view(), name='article'),
    path('schedule/', views.GenericSchedule.as_view(), name='schedule'),
    path('student/', views.StudentSchedule.as_view(), name='student'),
]
