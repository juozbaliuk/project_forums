from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('tasks', views.TaskListView.as_view(), name='tasks'),
    # path('task/<int:pk>', views.TaskDetailView.as_view(), name='task'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('forum/<int:forum_id>', views.forum, name='forum'),
    path('topic/<int:pk>', views.PostsListView.as_view(), name='topic'),
    path('forum/<int:pk>/new-topic/', views.NewTopicView.as_view(), name='new_topic'),
    path('settings/', views.SettingsUpdateView.as_view(), name='settings'),
    path('post/<int:pk>', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('search/', views.search, name='search'),
]