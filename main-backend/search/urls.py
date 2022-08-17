from django.urls import path

from search.views import SearchPosts, SearchCategories, SearchUsers

urlpatterns = [
    path('user/<str:query>/', SearchUsers.as_view()),
    path('category/<str:query>/', SearchCategories.as_view()),
    path('posts/<str:query>/', SearchPosts.as_view()),
]