from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task

@shared_task
def check_overdue_tasks():
    now = timezone.now()
    overdue_tasks = Task.objects.filter(
        due_date__lte=now.date(),
        due_time__lte=now.time(),
        completed=False
    )
    for task in overdue_tasks:
        subject = f"Task Overdue: {task.title}"
        message = f"Dear {task.user.username},\n\nYour task '{task.title}' was due on {task.due_date} at {task.due_time}. It is still incomplete.\n\nPlease complete it soon.\n\nRegards,\nTo-Do App Team"
        send_mail(
            subject,
            message,
            'your-email@gmail.com',
            [task.user.email],
            fail_silently=False,
        )