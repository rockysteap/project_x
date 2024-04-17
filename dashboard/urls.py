from django.urls import path

from dashboard import views

urlpatterns = [
    path('', views.RedirectToNews.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('news/', views.ShowNews.as_view(), name='news'),
    path('news/add_article', views.AddArticle.as_view(), name='add_article'),
    path('news/<slug:article_slug>/', views.ShowArticle.as_view(), name='article'),
]
