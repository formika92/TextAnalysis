import os

from django.urls import re_path, path

from text_load.views import Index, ShowFiles

app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('file/<int:pk>', ShowFiles.as_view(), name='file'),
]
