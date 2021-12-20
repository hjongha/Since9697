from django.apps import AppConfig
from deep.model import DeepModel

class PostConfig(AppConfig):
    name = 'post'
    model=DeepModel()