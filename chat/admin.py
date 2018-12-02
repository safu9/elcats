from django.contrib import admin

from .models import ChatUserInfo, Channel, ChannelMembership, Message


admin.site.register(ChatUserInfo)
admin.site.register(Channel)
admin.site.register(ChannelMembership)
admin.site.register(Message)
