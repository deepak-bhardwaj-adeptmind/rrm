# rrm_app/views.py
from datetime import timedelta

from django.db.models import Min
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from rrm_app.forms import OverriddenRoomRateForm, DiscountForm, RoomRateFilterForm, DiscountRoomRateForm
from rrm_app.forms import RoomRateForm
from rrm_app.models import OverriddenRoomRate, Discount, DiscountRoomRate
from rrm_app.models import RoomRate


class RoomRateListView(ListView):
    model = RoomRate
    template_name = 'room_rate_list.html'
    context_object_name = 'room_rates'


class RoomRateCreateView(CreateView):
    model = RoomRate
    form_class = RoomRateForm
    template_name = 'room_rate_form.html'
    success_url = reverse_lazy('room_rate_list')


class RoomRateUpdateView(UpdateView):
    model = RoomRate
    form_class = RoomRateForm
    template_name = 'room_rate_form.html'
    success_url = reverse_lazy('room_rate_list')


class RoomRateDeleteView(DeleteView):
    model = RoomRate
    template_name = 'room_rate_confirm_delete.html'
    success_url = reverse_lazy('room_rate_list')


class OverriddenRoomRateListView(ListView):
    model = OverriddenRoomRate
    template_name = 'overridden_rate_list.html'
    context_object_name = 'overridden_rates'


class OverriddenRoomRateCreateView(CreateView):
    model = OverriddenRoomRate
    form_class = OverriddenRoomRateForm
    template_name = 'overridden_rate_form.html'
    success_url = reverse_lazy('overridden_rate_list')


class OverriddenRoomRateUpdateView(UpdateView):
    model = OverriddenRoomRate
    form_class = OverriddenRoomRateForm
    template_name = 'overridden_rate_form.html'
    success_url = reverse_lazy('overridden_rate_list')


class OverriddenRoomRateDeleteView(DeleteView):
    model = OverriddenRoomRate
    template_name = 'overridden_rate_confirm_delete.html'
    success_url = reverse_lazy('overridden_rate_list')


class DiscountListView(ListView):
    model = Discount
    template_name = 'discount_list.html'
    context_object_name = 'discounts'


class DiscountCreateView(CreateView):
    model = Discount
    form_class = DiscountForm
    template_name = 'discount_form.html'
    success_url = reverse_lazy('discount_list')


class DiscountUpdateView(UpdateView):
    model = Discount
    form_class = DiscountForm
    template_name = 'discount_form.html'
    success_url = reverse_lazy('discount_list')


class DiscountDeleteView(DeleteView):
    model = Discount
    template_name = 'discount_confirm_delete.html'
    success_url = reverse_lazy('discount_list')


class RoomDiscountListView(ListView):
    model = DiscountRoomRate
    template_name = 'room_discount_list.html'
    context_object_name = 'room_discounts'


class RoomDiscountCreateView(CreateView):
    model = DiscountRoomRate
    form_class = DiscountRoomRateForm
    template_name = 'room_discount_form.html'
    success_url = reverse_lazy('room_discount_list')


class RoomDiscountUpdateView(UpdateView):
    model = DiscountRoomRate
    form_class = DiscountRoomRateForm
    template_name = 'room_discount_form.html'
    success_url = reverse_lazy('room_discount_list')


class RoomDiscountDeleteView(DeleteView):
    model = DiscountRoomRate
    template_name = 'room_discount_confirm_delete.html'
    success_url = reverse_lazy('room_discount_list')


def get_minimum_room_rate(request):
    room_rate_object = discounted_total_rate = None

    if request.method == 'POST':
        form = RoomRateFilterForm(request.POST)
        if form.is_valid():
            room_id = form.cleaned_data['room_id']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # fetch the room_rate_object object.
            room_rate_object = get_object_or_404(RoomRate, room_id=room_id)

            # generate a map containing {stay_date: overridden_price, stay_date_2: overridden_price_2}
            overridden_room_rates_qs = OverriddenRoomRate.objects.filter(
                room_rate_id=room_rate_object.id,
                stay_date__range=[start_date, end_date]
            ).values('stay_date').annotate(
                lowest_price=Min('overridden_rate')
            )
            overridden_room_rates = dict()
            for overridden_room_rate in overridden_room_rates_qs:
                overridden_room_rates[overridden_room_rate['stay_date']] = overridden_room_rate['lowest_price']

            # calculate the rate considering room_rate_object and overridden_room_rates
            total_rate = 0
            while start_date <= end_date:
                # Move to the next date
                start_date += timedelta(days=1)
                if overridden_room_rates.get(start_date):
                    total_rate += overridden_room_rates[start_date]
                else:
                    total_rate += room_rate_object.default_rate

            # apply the maximum discount applicable.
            discounts = Discount.objects.filter(discountroomrate__room_rate_id=room_rate_object.id)
            discounted_total_rate = total_rate
            for discount in discounts:
                if discount.discount_type == 'fixed':
                    curr_total_rate = total_rate - discount.discount_value
                else:
                    curr_total_rate = total_rate * (1 - discount.discount_value / 100)
                discounted_total_rate = min(discounted_total_rate, curr_total_rate)

            # discounted_total_rate should be 0 or greater than 0
            if discounted_total_rate < 0:
                discounted_total_rate = 0

    else:
        form = RoomRateFilterForm()

    return render(
        request, 'minimum_room_rate.html',
        {'form': form, 'room_rate': room_rate_object, "min_total_rate": discounted_total_rate}
    )
