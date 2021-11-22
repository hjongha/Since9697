from django.urls import path
from .views import *

app_name = 'cloth'

urlpatterns = [
    
    path('<username>/list/detail', my_cloth_list, name='my_cloth_list'),
    
    path('new', cloth_new, name='cloth_new'),
    path('cloth_recommend/<int:pk>/<username>/', cloth_recommend, name='cloth_recommend'),
    path('cloth_recommend_tot/<int:pk>/<username>/', cloth_recommend_tot, name='cloth_recommend_tot'),
    path('cloth_recommend_tit/<int:pk>/<username>/', cloth_recommend_tit, name='cloth_recommend_tit'),
    
    path('cloth_edit/<int:pk>/<username>/',cloth_edit, name='cloth_edit'),
    path('cloth_delete/<int:pk>/<username>/', cloth_delete, name='cloth_delete'),
    # path('delete_cloth/<int:pk>/<username>/', cloth_delete, name='cloth_delete'),
]

