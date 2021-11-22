from django import forms
from django.contrib import admin
from .models import Cloth


       
@admin.register(Cloth)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'nickname']
    list_display_links = ['author', 'nickname']

    
    def nickname(request, cloth):
        return cloth.author.profile.nickname



    
    
    
    
    
    
    
    
    
    
    
    








    
    
    
    
    
    
    