from django.conf import settings
from django.core.checks import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Mailing, Message, Client, Attempt


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'

class MailingCreateView(CreateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'status', 'message', 'clients']
    template_name = 'mailings/form.html'
    success_url = reverse_lazy('mailing_list')

class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'status', 'message', 'clients']
    template_name = 'mailings/form.html'
    success_url = reverse_lazy('mailing_list')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mailings/message_list.html'

class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'

class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailings/form.html'
    success_url = reverse_lazy('message_list')

class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailings/form.html'
    success_url = reverse_lazy('message_list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')


class ClientListView(ListView):
    model = Client
    template_name = 'mailings/client_list.html'

class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailings/client_detail.html'

class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailings/form.html'
    success_url = reverse_lazy('client_list')

class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailings/form.html'
    success_url = reverse_lazy('client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailings/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')


def send_mailing_now(request, pk):
    """Ручная отправка рассылки"""
    mailing = get_object_or_404(Mailing, pk=pk)

    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.title,
                message=mailing.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            status = 'Успешно'
            server_response = 'Письмо успешно отправлено'
        except Exception as e:
            status = 'Не успешно'
            server_response = str(e)

        Attempt.objects.create(
            mailing=mailing,
            attempt_time=timezone.now(),
            status=status,
            server_response=server_response,
        )

    messages.success(request, f'Рассылка «{mailing.title}» отправлена.')
    return redirect('mailing_list')



