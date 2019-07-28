import logging
import threading

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm, CustomUserCreationForm
from .service import serv_customer

logger = logging.getLogger(__name__)

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('deal_findr:login')
    template_name = 'registration/signup.html'

@login_required
def HomeView(request):
    return render(request, 'deal_findr/home.html')
    
@login_required
def FormView(request):
    if request.method == 'POST':
        logger.info("Post method")
        form = CustomerForm(request.POST)
        logger.info("Form created")
        if form.is_valid():
            first_name = request.user.first_name 
            phone = request.user.phone.as_e164[3:]
            email = request.user.email
            website = form.cleaned_data['website']
            budget = form.cleaned_data['budget']
            productURL = form.cleaned_data['productURL']
            logger.info("Creating thread")
            thread1 = threading.Thread(target=serv_customer, args=(first_name, phone, email, website, budget, productURL,))
            thread1.start()
            #thread1.join()
            # redirect to a new URL:
            logger.info('Redirecting...')
            return HttpResponseRedirect(reverse('deal_findr:home'))
        else:
            logger.info("form invalid")

    # if a GET (or any other method) we'll create a blank form
    else:
        logger.info("Get method")
        form = CustomerForm()

    return render(request, 'deal_findr/form.html', {'form': form})
