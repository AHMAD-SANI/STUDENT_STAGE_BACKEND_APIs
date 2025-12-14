from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from .views import questionview, answeerview, questioninstanceview, answerinstanceview
from .views import  newsview, newsinstanceview, e_bookview, e_bookinstanceview
from .views import register, login, profileview, profileinstanceview, request_user_profile, logout
from .views import Adding_user_to_group, remove_user_to_group, statistics, group_members, userQs, adminAns


urlpatterns = [
    #DOCUMENTATION URLS PATHS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema' ),
    path('api/docs/swagger/', SpectacularRedocView.as_view(url_name='scheme'), name='swagger-ui' ),
    path('doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='redoc' ),


    #PROJECT URLS PATHS
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('addtogroup/<str:group_name>/<int:user_id>', Adding_user_to_group),
    path('removetogroup/<str:group_name>/<int:user_id>', remove_user_to_group),
    path('group_members/<str:group_name>/', group_members),
    path('me', request_user_profile),
    path('profiles/<int:pk>', profileinstanceview.as_view()),
    path('profiles/', profileview.as_view()),
    path('statistics', statistics),
    path('userQs', userQs),
    path('adminAns', adminAns),
    path('questions', questionview.as_view()),
    path('questions/<str:pk>', questioninstanceview.as_view()),
    path('answers', answeerview.as_view()),
    path('answers/<str:pk>', answerinstanceview.as_view()),
    path('news', newsview.as_view()),
    path('news/<int:pk>', newsinstanceview.as_view()),
    path('ebook', e_bookview.as_view()),
    path('ebook/<int:pk>', e_bookinstanceview.as_view()),
    
]


