from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.contrib import messages

from django.forms import formset_factory
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, ListView, DetailView, FormView
import googlemaps


from .forms import AddressForm, OrderEntryForm
from .models import Restaurant, Course, Order, OrderEntry


class MainPage(TemplateView):
    template_name='restaurants/main_page.html'
    extra_context = {
        'title': 'Najlepsze jedzenie',
        'form': AddressForm(),
    }


class AllRestaurants(ListView):
    context_object_name = 'restaurants'


    template_name = 'restaurants/all.html'

    def get_coordinates(self):
        client = googlemaps.Client(key = settings.GMAPS_KEY)
        geocode_results = client.geocode(self.address)

        if geocode_results:
            return (

                geocode_results[0]['geometry']['location']['lat'],
                geocode_results[0]['geometry']['location']['lng'],
            )
        return None, None

    def get_context_data(self, **kwargs):
        context = {
            'title': 'Restauracja w Twojej okolicy',
            'address': self.address,
        }

        context.update(kwargs)
        return super().get_context_data(**context)


    def get_queryset(self):

        qs = Restaurant.objects.prefetch_related('cuisines')
        if self.address:
            lat, lng = self.get_coordinates()
            if lat and lng:
                complex_F = ((

                    (F('latitude') - lat) ** 2
                    +
                    (F('longitude') - lng) ** 2
                ) **0.5)*73*2


                return qs.annotate(distance=complex_F, delivery_cost=F('distance')*1.5).order_by('distance')
        return qs

    def get_ordering(self):
        return self.request.GET.get('o', 'name')

    def get(self, request, *args, **kwargs):

        self.address = request.GET.get('address', '')
        return super().get(request, *args, **kwargs)


class RestaurantDetails(DetailView):

    context_object_name = 'restaurant'

    pk_url_kwarg = 'restaurant_id'
    queryset = Restaurant.objects.all()
    template_name = 'restaurants/details.html'


    def get_context_data(self, **kwargs):
        self.address = self.request.GET.get('address', '')
        context = {

            'title': self.object.name,
            'address': self.address,
        }

        context.update(kwargs)
        return super().get_context_data(**context)


def add_to_cart(request, course_id):


    course = get_object_or_404(Course, pk=course_id)

    if 'cart' not in request.session:
        request.session['cart'] = list()

    request.session['cart'].append(course.pk)
    request.session.modified = True

    messages.success(request, f'Dodano "{ course }" do koszuka')

    if 'next' in request.GET:
        return redirect(request.GET['next'])

    return redirect('restaurants:all')


def cart(request):
    cart = []
    order_amount = 0
    address = request.GET.get('address', '')
    if 'cart' in request.session:
        course_set = set(request.session['cart'])

        qs = Course.objects.filter(pk__in=course_set).select_related('restaurant')


        for course in qs:
            x = request.session['cart'].count(course.pk)
            cart.append(
                {
                    'restaurant': course.restaurant,
                    'course': course,
                    'quantity': x,
                    'amount': x * course.price,
                }
            )
            order_amount += x*course.price

    context = {
        'title': 'Koszyk',
        'cart': cart,
        'order_amount': order_amount,
        'address': address,
    }
    return render(request, 'restaurants/cart.html', context)


class CreateOrder(LoginRequiredMixin, FormView):
    form_class = formset_factory(OrderEntryForm, extra=0)
    success_url = '/'
    template_name = 'restaurants/create_order.html'


    def dispatch(self, request, *args, **kwargs):
        self.address = self.request.GET.get('address', '')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context={
            'title': 'Złóż zamówienie',
            'address': self.address
        }
        context.update(kwargs)
        return super().get_context_data(**context)


    def get_initial(self):
        cart = []
        if 'cart' in self.request.session:
            course_set = set(self.request.session['cart'])

            qs = Course.objects.filter(pk__in=course_set)

            for course in qs:
                x = self.request.session['cart'].count(course.pk)
                cart.append(
                    {
                        'course': course,
                        'quantity': x,

                    }
                )
        return cart

    def form_valid(self, form):
        order = Order(
            user=self.request.user,
            amount=sum([x['course'].price * x['quantity'] for x in form.cleaned_data]),
            delivery_cost=0,
            delivery=self.address,
        )

        order.save()

        order_entries = [
            OrderEntry(order=order, course=entry['course'], quantity=entry['quantity'])
            for entry in form.cleaned_data
        ]


        OrderEntry.objects.bulk_create(order_entries)

        messages.success(self.request, 'Złożono zamówienie ')

        del self.request.session['cart']
        return super().form_valid(form)




