from django.contrib import admin
from .models import Client, Message, Mailing

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment')
    search_fields = ('full_name', 'email')
    list_filter = ('full_name',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    search_fields = ('subject', 'body')

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'start_time', 'end_time', 'message_list', 'clients_list')
    list_filter = ('status',)
    search_fields = ('message__subject',)

    def message_list(self, obj):
        return obj.message.subject
    message_list.short_description = 'Сообщение'

    def clients_list(self, obj):
        return ", ".join([client.full_name for client in obj.clients.all()])
    clients_list.short_description = 'Получатели'

