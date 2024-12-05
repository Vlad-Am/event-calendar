from django.urls import path, include
from rest_framework.routers import DefaultRouter

from sport import views
from sport.apps import SportConfig
from sport.views import TrainerViewSet, DirectionViewSet
app_name = SportConfig.name

router = DefaultRouter()
router.register(r'trainers', TrainerViewSet)
router.register(r'directions', DirectionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('trainers/', views.TrainerListView.as_view(), name='trainer_list'),
    path('trainers/create/', views.TrainerCreateView.as_view(), name='trainer_add'),
    path('trainers/update/<int:pk>/', views.TrainerUpdateView.as_view(), name='trainer_edit'),
    path('trainers/delete/<int:pk>/', views.TrainerDeleteView.as_view(), name='trainer_delete'),

    path('directions/', views.DirectionListView.as_view(), name='direction_list'),
    path('directions/create/', views.DirectionCreateView.as_view(), name='direction_add'),
    path('directions/update/<int:pk>/', views.DirectionUpdateView.as_view(), name='direction_edit'),
    path('directions/delete/<int:pk>/', views.DirectionDeleteView.as_view(), name='direction_delete'),

]

