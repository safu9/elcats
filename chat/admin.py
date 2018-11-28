from django.contrib import admin

from .models import ChatUserInfo, Channel, ChannelUserInfo, Message


admin.site.register(ChatUserInfo)
admin.site.register(Channel)
admin.site.register(ChannelUserInfo)
admin.site.register(Message)
