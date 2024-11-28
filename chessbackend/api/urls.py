# from django.contrib import admin
# from django.urls import path, include
# from rest_framework import routers
# from .views import *
 
# router = routers.DefaultRouter()

# router.register(r'game', GameViewSet)
 
# urlpatterns = [
#     path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls'))
# ]


from django.urls import path
from .views import GameMatch,GameList

urlpatterns = [
    path('game/<int:game_id>/', GameMatch.as_view(), name='game_match'),
    path('game/', GameList.as_view(), name='game_list')
]