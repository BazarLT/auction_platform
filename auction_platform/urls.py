from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from bidding import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('bidding/', include('bidding.urls')),  # Include the bidding app's URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/', include('allauth.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
