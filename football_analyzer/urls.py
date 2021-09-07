"""football_analyzer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from home import views as homeViews
from my_user import views as myUserViews
from price import views as myPriceViews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homeViews.viewHomepage,name='Homepage'),
    path('user/',myUserViews.viewUserdata,name='Userpage'),
    path('login/',myUserViews.viewUserlogin,name='Userlogin'),
    path('about/',homeViews.viewAboutpage,name='Aboutpage'),
    path('logout/',myUserViews.logout,name='Logout'),
    path('price/',myPriceViews.viewPrice,name='Price'),
]
