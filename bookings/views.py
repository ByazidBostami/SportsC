from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')
from .models import Event
from django.shortcuts import get_object_or_404

def create_event(request):
    if request.method == "POST":
        # Handle event creation logic
        pass
    return render(request, 'create_event.html')

from django.contrib.auth.decorators import login_required

@login_required
def booked_events(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booked_events.html', {'bookings': bookings})


from django.shortcuts import render
from django.db.models import Sum
from .models import Booking

def dashboard(request):
    total_paid = Booking.objects.filter(is_paid=True).aggregate(Sum('payment'))['payment__sum'] or 0
    total_due = Booking.objects.filter(is_paid=False).aggregate(Sum('payment'))['payment__sum'] or 0
    total_booked = Booking.objects.count()

    context = {
        'total_paid': total_paid,
        'total_due': total_due,
        'total_booked': total_booked,
    }
    return render(request, 'dashboard.html', context)


from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Render a template named `home.html`
from django.contrib.auth.views import LoginView



class CustomLoginView(LoginView):
    template_name = 'login.html'  # Replace with the path to your login template

from django.http import JsonResponse
from .models import Booking
from django.utils.dateparse import parse_datetime

class BookingListAPI:
    def get(self, request):
        # Parse `start` and `end` parameters from the request
        start = parse_datetime(request.GET.get('start'))
        end = parse_datetime(request.GET.get('end'))

        # Filter bookings by the given date range
        bookings = Booking.objects.filter(slot_start__gte=start, slot_end__lte=end)

        # Serialize data into a list of dictionaries
        data = [
            {
                "id": booking.id,
                "title": booking.name,
                "start": booking.slot_start.isoformat(),
                "end": booking.slot_end.isoformat(),
            }
            for booking in bookings
        ]
        return JsonResponse(data, safe=False)
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking

class BookingListAPI(APIView):
    def get(self, request):
        start = request.GET.get('start')
        end = request.GET.get('end')
        bookings = Booking.objects.filter(slot_start__gte=start, slot_end__lte=end)
        data = [
            {
                "id": booking.id,
                "title": booking.name,
                "start": booking.slot_start.isoformat(),
                "end": booking.slot_end.isoformat(),
            }
            for booking in bookings
        ]
        return Response(data)
