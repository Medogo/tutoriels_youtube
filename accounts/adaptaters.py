from lib2to3.fixes.fix_input import context
import sib_api_v3_sdk
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.providers.mediawiki.provider import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from sib_api_v3_sdk.rest import ApiException

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        #obtenir le nom du site

        current_site = get_current_site(request)

        context = {
            'user': emailconfirmation.email_address.user,
            'activate_url': activate_url,
            'current_site': current_site,
            'key': emailconfirmation.key,
            'signup':signup
        }
        # rendre les templates

        subject = render_to_string('account/email/email_confirmation_subject.txt', context).strip()
        message = render_to_string('account/email_confirmation_message.html', context)

        # configuration de l'API Brevo

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api_key'] = settings.SEDINBLUE_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        #creer l'email
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            sender={
                "email": settings.BREVO_SENDER['EMAIL'],
                "name": settings.BREVO_SENDER['NAME']
            },
            to=[
                {
                    "email": emailconfirmation.email_address.email,
                    "name":emailconfirmation.email_address.email
                }
            ],
            subject=subject,
            html_content=message
        )
        # Envoyer l'email
        try:
            api_instance.send_transac_email(send_smtp_email)
        except ApiException as e:
            print(f"Erreur lors de l'envoi de l'email de confirmation : {e}")