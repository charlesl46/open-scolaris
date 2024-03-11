from .models import OpenScolarisMessage, OSMessageAttachment, OSMessageRecipient
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, JsonResponse, FileResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.contrib.messages import success
from datetime import datetime
from django.utils import timezone
from notifications.signals import notify


@login_required
def write_message(request: HttpRequest):
    print(request.method)
    if request.method == "POST":
        data = request.POST
        message = OpenScolarisMessage.objects.create(sender=request.user)
        message.subject = data.get("subject")
        message.content = data.get("content")
        recipients = data.getlist("recipients")[0].split(
            ","
        )  # pour gérer le comportement bizarre
        recipients_objs = []
        for r in recipients:
            recipient = User.objects.get(username=r)
            notify.send(
                request.user,
                recipient=recipient,
                verb=f"Nouveau message",
                level="info",
                description=f"Vous avez reçu un message de {request.user}",
            )
            recipients_objs.append(recipient)
        message.recipients.set(recipients_objs)
        attachments = []
        for f in request.FILES.getlist("attachments"):
            attachment = OSMessageAttachment.objects.create(file=f)
            attachment.save()
            attachments.append(attachment)
        message.attachments.set(attachments)
        message.save()
        success(request, "Votre message a été envoyé avec succès")
        return redirect("home")
    else:
        users = User.objects.exclude(username=request.user.username).all()
        return render(request, "scolaris_app/messages/write_message.html", {"users": users})


@login_required
@csrf_exempt
def search_recipients(request: HttpRequest):
    if request.method == "POST":
        query = request.POST.get("query")
        qs = (
            User.objects.filter(first_name__icontains=query)
            | User.objects.filter(last_name__icontains=query)
            | User.objects.filter(username__icontains=query)[:5]
        )
        results = [
            {
                "id": user.id,
                "user_found": f"{user.first_name} {user.last_name} ({user.username})",
                "username": user.username,
            }
            for user in qs
        ]
        return JsonResponse({"results": results})


@login_required
def message_detail(request: HttpRequest, uuid):
    # on considère qu'une fois le message affiché une fois il est lu
    message = get_object_or_404(OpenScolarisMessage, uuid=uuid)
    osmr = OSMessageRecipient.objects.get(message=message, recipient=request.user)
    if not osmr.read_at:
        osmr.read_at = timezone.now()
        osmr.save()
    return render(request, "scolaris_app/messages/message.html", {"message": message})


@login_required
def messages(request: HttpRequest):
    messages_objs = [
        (message, message.was_read_by(request.user))
        for message in OpenScolarisMessage.objects.filter(recipients=request.user)
        .order_by("-sent_at")
        .all()
    ]
    return render(
        request, "scolaris_app/messages/message_list.html", {"message_list": messages_objs}
    )


@login_required
def download_attachment(request: HttpRequest, uuid, id: int):
    attachment = get_object_or_404(OSMessageAttachment, pk=id)
    return FileResponse(attachment.file)


@login_required
@csrf_exempt
def message_toggle_read(request: HttpRequest):
    if request.method == "POST":
        uuid = request.POST.get("message_uuid")
        message = get_object_or_404(OpenScolarisMessage, uuid=uuid)
        read = message.toggle_read(request.user)
        return JsonResponse({"read": read})
