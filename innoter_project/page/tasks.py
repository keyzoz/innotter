from celery import shared_task
from django.utils import timezone

from .models import Page


@shared_task
def unblock_pages():
    curr_time = timezone.now()
    blocked_pages = Page.objects.filter(is_blocked=True, unblock_date__lte=curr_time)
    for page in blocked_pages:
        page.is_blocked = False
        page.unblock_date = None
        page.save()
