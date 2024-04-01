from django.test import TestCase,Client

# Create your tests here.
from .models import Airport,Flights,Passenger

class FlightTestCase(TestCase):

    def setUp(self):

        a1 = Airport.objects.create(code="AAA",city="city_A")
        a2 = Airport.objects.create(code="BBB",city="city_B")

        Flights.objects.create(origin=a1,destination=a2,duration=100)
        Flights.objects.create(origin=a1,destination=a1,duration=200)
        Flights.objects.create(origin=a1,destination=a2,duration=-200)
    
    def test_departures_count(self):
        
        a = Airport.objects.get(code="AAA")
        
        self.assertEqual(a.departures.count(),3)
    def test_arrivals_count(self):

        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(),1)

    def test_valid_flight(self):
        a1=Airport.objects.get(code="AAA")
        a2=Airport.objects.get(code="BBB")
        f=Flights.objects.get(origin=a1,destination=a2,duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_valid_flight_destination(self):
        a=Airport.objects.get(code="AAA")
        f=Flights.objects.get(origin=a,destination=a)
        self.assertFalse(f.is_valid_flight())
    def test_valid_flight_duration(self):
        a1=Airport.objects.get(code="AAA")
        a2=Airport.objects.get(code="BBB")
        f=Flights.objects.get(origin=a1,destination=a2,duration=-200)
        self.assertFalse(f.is_valid_flight())
    def test_index(self):
        c = Client()
        response = c.get("/flights/")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["flights"].count(),3)
    def test_valid_flight_page(self):
        p=Passenger.objects.create(first="harry",last="potter")
        f=Flights.objects.get(pk=1)
        f.passengers.add(p)
        c=Client()
        response=c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["passengers"].count(),1)


        
    
