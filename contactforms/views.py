from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from . import models

from .email_manager.sender import Email_manager

# Allow only post and disable csrf
@require_http_methods(["POST"])
@csrf_exempt
def index (request):
    """Send email and redirect"""

    # Get form data
    form_data = request.POST.dict()

    # Check all inputs
    all_inputs = True
    inputs_names = ["api_key", "user", "redirect"]
    for input_name in inputs_names:
        if input_name not in form_data.keys():
            all_inputs = False
            break

    # Return inputs error 
    if not all_inputs:
        return HttpResponseBadRequest ("Invalid form structure")

    # Validate api user name
    valid_login = False
    users = models.User.objects.filter (name=form_data["user"])
    if users:
        user = users[0]
        api_key = user.api_key
        if api_key == form_data["api_key"]:
            valid_login = True

    # Return login error
    if not valid_login:
        return HttpResponseBadRequest ("invalid api key or user name")    

    # Format email body
    message = ""
    subject = "New contact message!"
    for input_name, input_value in form_data.items():

        # Get body values
        if input_name not in ["api_key", "redirect", "subject", "user"]:
            message += f"{input_name}: {input_value}\n"

        # Get custom subject
        if input_name == "subject":
            subject = input_value

    # Get blacklist of emails
    is_spam = False
    blackLiist_email_found = ""
    message_clean = message.lower().strip()
    blackLiist_emails = map (lambda elem : elem.to_email, models.BlackList.objects.all())
    for blackLiist_email in blackLiist_emails:
        blackLiist_email_clean = blackLiist_email.lower().strip()
        if blackLiist_email in message_clean:
            is_spam = True
            blackLiist_email_found = blackLiist_email
            break

    if is_spam:
        # Dont send message and change subject in history
        subject = f"Spam try from {blackLiist_email_found}"
    else:
        # Send email 
        email = models.FromEmail.objects.all()[0].email
        password = models.FromEmail.objects.all()[0].password
        emailer = Email_manager (email, password)
        emailer.send_email ([user.to_email], subject, message)

    # Save in history
    register = models.History (user=user, subject=subject)
    register.save()

    return HttpResponseRedirect(form_data["redirect"]) 
