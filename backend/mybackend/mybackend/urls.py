"""mybackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from .views import landing_page, product_normal, product_recommend,product_recommend_register,product_rated_recommend,Register,Update_Rated_Recommend

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',landing_page,name='landing_page'),
    path('product_normal',product_normal,name='product_normal'),
    path('product_recommend',product_recommend,name='product_reccommend'),
    path('product_recommend_register',product_recommend_register,name='product_recommend_register'),
    path('product_rated_recommend',product_rated_recommend,name='product_rated_recommend'),
    path('Register',Register,name='Register'),
    path('Update_Rated_Recommend',Update_Rated_Recommend,name='Update_Rated_Recommend'),
    
]
