from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('portfolio/', users_views.public_index, name='public_index'),
    path('<str:username>/', users_views.user_portfolio, name='user_portfolio'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
