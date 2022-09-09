"""Django url views."""
from django.http import HttpResponse


def home(request):
    """Main page."""
    return HttpResponse("Pls, go to admin section.")
