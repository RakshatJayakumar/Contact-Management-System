from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth .mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Contact

class CustomLoginView(LoginView):
    template_name='contacts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('contacts')
        
class RegisterPage(FormView):
    template_name = 'contacts/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('contacts')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('contacts')
        return super(RegisterPage, self).get(*args, **kwargs)
    
class ContactList(LoginRequiredMixin, ListView):
    model = Contact
    context_object_name = 'contacts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts']= context['contacts'].filter(user=self.request.user)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['contacts'] = context['contacts'].filter(name__startswith=search_input)
            
        context['search_input'] = search_input
        
        return context
    
class ContactDetail(LoginRequiredMixin, DetailView):
    model = Contact
    context_object_name = 'contact'
    
class ContactCreate(LoginRequiredMixin, CreateView):
    model = Contact
    fields = ['name','phone_number','address', 'email_address']
    success_url = reverse_lazy('contacts')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ContactCreate, self).form_valid(form)
    
class ContactUpdate(LoginRequiredMixin, UpdateView):
    model = Contact
    fields = ['name','phone_number','address', 'email_address']
    success_url = reverse_lazy('contacts')
    
class ContactDelete(LoginRequiredMixin, DeleteView):
    model = Contact
    context_object_name = 'contact'
    success_url = reverse_lazy('contacts')