from django.db import models


class SyncLog(models.Model):
    date = models.DateField(primary_key=True)
    new_events = models.IntegerField(default=0)
    updated_events = models.IntegerField(default=0)

    def __str__(self):
        return (
            f"Sync at {self.date}: new-{self.new_events}, updated-{self.updated_events}"
        )
