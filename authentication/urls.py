from django.urls import path, re_path
from .views import (
	login, 
	confirmation,
	home, 
	visits,
)

urlpatterns = [
    path('', login, name='login'),
    re_path(r'^confirmation/(?P<token>.+)/', confirmation, name='confirmation'),
    path('home/', home, name='home'),
    path('visits/', visits, name='visits'),
]