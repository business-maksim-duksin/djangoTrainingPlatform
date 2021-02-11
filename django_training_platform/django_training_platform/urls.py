"""django_training_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from .yasg import urlpatterns as doc_urls
import debug_toolbar

#
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# # urlpatterns += doc_urls
sub_urlpatterns_api_v1 = [
    # path('admin/', admin.site.urls),
    # path('apiauth/', include('rest_framework.urls')),
    # re_path(r'^api/v1/', include('training_platform.urls', namespace='v1')),
    # re_path(r'^api/v1/', include('users.urls', namespace='v1')),

    re_path('', include('training_platform.urls', )),
    re_path('', include('users.urls', )),

]

# sub_urlpatterns += [
#     # YOUR PATTERNS
#     path('api/v1/schema/', SpectacularAPIView.as_view(api_version='v1',), name='schema'),
#     # Optional UI:
#     path('api/v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
#
#     path('__debug__/', include(debug_toolbar.urls)),
# ]

sub_urlpatterns_api_v1 += [
    # YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(api_version='v1',), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # path('__debug__/', include(debug_toolbar.urls)),
]
foo = []
urlpatterns = [
    re_path(r'^api/v1/', include((sub_urlpatterns_api_v1, 'v1'), namespace='v1')),
    re_path(r'^api/v2/', include((sub_urlpatterns_api_v1, 'v2'), namespace='v2')),
    path('__debug__/', include(debug_toolbar.urls)),
]
