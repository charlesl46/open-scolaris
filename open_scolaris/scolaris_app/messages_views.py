from .models import OpenScolarisMessage,OSMessageAttachment
from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from accounts.models import User

@login_required
def write_message(request : HttpRequest):
    print(request.method)
    if request.method == "POST":
        data = request.POST
        message = OpenScolarisMessage.objects.create(sender=request.user)
        message.subject = data.get("subject")
        message.content = data.get("content")
        recipients = data.getlist('recipients')
        recipients_objs = []
        for r in recipients:
            recipient = User.objects.get(username=r)
            recipients_objs.append(recipient)
        message.recipients.set(recipients_objs)

        attachments = []
        for f in request.FILES.getlist('attachments'):
            attachment = OSMessageAttachment.objects.create(file=f)
            attachment.save()
            attachments.append(attachment)
        message.attachments.set(attachments)
        message.save()
        return redirect('home')
    else:
        users = User.objects.exclude(username=request.user.username).all()
        return render(request,"scolaris_app/write_message.html",{"users" : users})
    
@login_required
@csrf_exempt
def search_recipients(request : HttpRequest):
    if request.method == "POST":
        query = request.POST.get("query")
        qs = User.objects.filter(first_name__icontains=query) | User.objects.filter(last_name__icontains=query) | User.objects.filter(username__icontains=query)[:5]
        results = [{"id": user.id,"user_found": f"{user.first_name} {user.last_name} ({user.username})","username" : user.username} for user in qs]
        return JsonResponse({"results": results})