from django.urls import path
from . import views


app_name = 'bloger'
urlpatterns = [ 
    #post views
    path('', views.post_list, name='post_list'),
    path('bloger-list/', views.PostListView.as_view(), name='bloger_post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
]
