from django.urls import re_path, path
from . import views

# urlpatterns = [
#     path('csrf/', views.get_csrf, name='api-csrf'),
#     path('login/', views.login_view, name='api-login'),
#     path('logout/', views.logout_view, name='api-logout'),
#     path('session/', views.SessionView.as_view(), name='api-session'),
#     path('whoami/', views.WhoAmIView.as_view(), name='api-whoami'),
# ]


urlpatterns = [
    # path('login/', views.LoginView.as_view(), name="login"),
    # path('login/', views.login, name="api-login"),
    re_path('login', views.login),
    re_path('logout', views.logout),
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),
]