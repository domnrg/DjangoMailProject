from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Mailing

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'

class MailingCreateView(CreateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'frequency', 'status', 'message', 'clients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'frequency', 'status', 'message', 'clients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')


