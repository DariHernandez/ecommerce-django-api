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

    # Send email 
    email = models.FromEmail.objects.all()[0].email
    password = models.FromEmail.objects.all()[0].password
    emailer = Email_manager (email, password)
    emailer.send_email ([user.to_email], subject, message)

    # Save in history
    register = models.History (user=user, subject=subject)
    register.save()

    return HttpResponseRedirect(form_data["redirect"]) 
