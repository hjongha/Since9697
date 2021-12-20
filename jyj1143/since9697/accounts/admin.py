from django.contrib import admin
from .models import Profile, Follow


# Register your models here.

class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = 'from_user'


@admin.register(Profile)  #  @admin.register() 장식자(decorator)를 사용하여 등록한다
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'user']   #    list_display는 노출시키고자 하는 필드를 선택
    list_display_links = ['nickname', 'user']   #    list_display_links는 등록한 필드의 데이터에 링크를 걸어 세부내역을 확인할 수 있다
    search_fields = ['nickname']                #    search_fields는 해당 필드의 데이터를 검색할 수 있게 해준다
    inlines = [FollowInline,]
    
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'created_at']
    list_display_links = ['from_user', 'to_user', 'created_at']