from django.contrib import admin
from .models import UserWrapper, EmailCode, Banner


class UserWrapperAdmin(admin.ModelAdmin):
    pass


class EmailCodeAdmin(admin.ModelAdmin):
    pass


class BannerAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserWrapper, UserWrapperAdmin)
admin.site.register(EmailCode, EmailCodeAdmin)
admin.site.register(Banner, BannerAdmin)