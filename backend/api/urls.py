from django.urls import path
from . import views
urlpatterns=[
    path("setUserBlog/",views.setUserBlog),
    path("getUserBlog/",views.getUserBlog),
    path("publishUserBlog/",views.publishUserBlog),
    path("getForReviewBlogs/",views.getForReviewBlog),
    path("editUserBlog/",views.editUserBlog),
    path("getBlog/",views.getBlog),
    path("getAllBlogs/",views.getAllBlogs),
    path("users/google/",views.addGoogle),
    path("updateLikes/",views.updateLikes),
    path("addComment/",views.addComment),
    path("removeComment/",views.removeComment),
    path("getUserDraft/",views.getUserDraft),
    path("users/register/", views.register),
    path("users/login/", views.login),
]