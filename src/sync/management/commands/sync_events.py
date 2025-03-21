import datetime

import requests
from django.core.management.base import BaseCommand

from src.events.models import Event
from src.sync.models import SyncLog


class Command(BaseCommand):
    EVENTS_API = "https://events.k3scluster.tech/api/events/"

    def add_arguments(self, parser):
        parser.add_argument("--date")
        parser.add_argument("--all", action="store_true")

    def handle(self, *args, **options):
        if options["all"]:
            url = self.EVENTS_API
        else:
            yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime(
                "%Y-%m-%d"
            )
            url = (
                self.EVENTS_API
                + f"?changed_at={options['date'] if options['date'] else yesterday}"
            )
        self.fetch_url(url)
        self.stdout.write("Синхронизированы ивенты")

    def fetch_url(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            self.stderr.write("Ошибка получения данных")
            return
        next_page = response.json().get("next")
        results = response.json().get("results")
        self.prepare_event(results)
        if next_page:
            self.fetch_url(next_page)

    def prepare_event(self, results):
        for event in results:
            date = datetime.datetime.fromisoformat(event["changed_at"])

            obj, created = Event.objects.update_or_create(
                id=event["id"], name=event["name"], status=event["status"], date=date
            )
            log_date = date.date()

            log, _ = SyncLog.objects.update_or_create(date=log_date)
            if created:
                log.new_events += 1
            else:
                log.updated_events += 1
            log.save()
