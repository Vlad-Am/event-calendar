from django.urls import path, include
from rest_framework.routers import DefaultRouter

from sport.apps import SportConfig
from sport.views import TrainerViewSet, DirectionViewSet, trainer_list, trainer_create, trainer_update, trainer_delete, \
    direction_list, direction_create, direction_update, direction_delete

app_name = SportConfig.name

router = DefaultRouter()
router.register(r'trainers', TrainerViewSet)
router.register(r'directions', DirectionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('trainers/', trainer_list, name='trainer_list'),
    path('trainers/add/', trainer_create, name='trainer_add'),
    path('trainers/<int:pk>/', trainer_update, name='trainer_edit'),
    path('trainers/<int:pk>/delete/', trainer_delete, name='trainer_delete'),
    path('directions/', direction_list, name='direction_list'),
    path('directions/add/', direction_create, name='direction_add'),
    path('directions/<int:pk>/', direction_update, name='direction_edit'),
    path('directions/<int:pk>/delete/', direction_delete, name='direction_delete'),

]

