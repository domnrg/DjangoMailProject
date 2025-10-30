from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Mailing, Message, Client


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'

class MailingCreateView(CreateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'frequency', 'status', 'message', 'clients']
    template_name = 'mailings/form.html'
    success_url = reverse_lazy('mailing_list')

class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'frequency', 'status', 'message', 'clients']
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


