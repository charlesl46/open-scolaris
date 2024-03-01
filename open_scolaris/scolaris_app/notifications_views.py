from notifications.models import Notification
from notifications.signals import notify
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt


@login_required
def notifications_view(request : HttpRequest):
    notifs = request.user.notifications
    return render(request,'notifications.html',{"qs" : notifs,"active" : "notifications"})

@login_required
def mark_all_as_read(request : HttpRequest):
    notifs = request.user.notifications
    notifs.mark_all_as_read()
    return redirect('notifications')

@login_required
@csrf_exempt
def mark_as_read(request : HttpRequest, id : int):
    try:
        notif = get_object_or_404(Notification, id=id)
        notif.mark_as_read()
        notif.save()
        unread = request.user.notifications.unread()
        if unread:
            unread_count = unread.count()
        else:
            unread_count = 0
        return JsonResponse({"status" : "ok","unread_count" : unread_count})
    except Exception as e:
        print(e.with_traceback())
        return JsonResponse({"status" : "error"})