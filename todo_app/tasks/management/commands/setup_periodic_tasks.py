from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

class Command(BaseCommand):
    help = 'Setup periodic tasks for Celery Beat'

    def handle(self, *args, **options):
        # ১০ মিনিটের ইন্টারভাল তৈরি
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.MINUTES,
        )
        # Periodic Task তৈরি
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Check overdue tasks',
            task='tasks.tasks.check_overdue_tasks',
            defaults={'enabled': True},
        )
        self.stdout.write(self.style.SUCCESS('Periodic tasks setup successfully!'))