import logging
import threading

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required

from .forms import CustomerForm, CustomUserCreationForm
from .service import serviceStart

logger = logging.getLogger("testlogger")

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
            customer = request.user
            deal = form.save(commit=False)
            deal.customer_id = customer.id
            deal.save()
            form.save_m2m()
            logger.info("Creating service thread")
            service_thread = threading.Thread(target=serviceStart, args=(customer, deal,))
            service_thread.start()

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
