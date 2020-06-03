from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.Home,name="Home"),
    re_path(r'Question$', views.Questions,name="Question"),
    re_path(r'Register$', views.Register,name="Register"),
    re_path(r'Register_user$', views.Register_user,name="Register_user"),
    re_path(r'Login$', views.Login,name="login"),
    re_path(r'Login_user$', views.Login_user,name="Login_user"),
    re_path(r'Logout$', views.Logout,name="Logout"),
    re_path(r'Contribute$', views.Contribution,name="contribute"),
    re_path(r'ReviewContribution$', views.Review_Contribution,name="ReviewContribution"),
    path('Problems/<str:problem>/', views.Editor,name="Editor"),
     re_path(r'Request$', views.User_Request,name="user_Request"),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT) 
    