from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.account.signals import email_confirmed
from django.http import HttpResponse
from django.views import View
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import CustomUser
from .serializers import UserRegistrationSerializers


# Create your views here.
from rest_framework.permissions import IsAuthenticated

class UserRegistratioView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializers
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            "request": self.request
        })
        return context

class ConfirmationEmail(View):
    def get(self, request, key, *args, **kwargs):
        # tenter de confirmer l'email

        email_confirmation = None
        try:
            email_confirmation = EmailConfirmationHMAC.from_key(key)
            if email_confirmation:
                email_confirmation.confirm(request)
                email_confirmed.send(sender=self.__class__, request=request, email_address=email_confirmation.email_address)
            else:
                return HttpResponse('Clé de confirmation invalide ou expiré', status=400)
        except Exception as e:
            return HttpResponse('Erreur lors de la confirmation de lemail,', status=400)