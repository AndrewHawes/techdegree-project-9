from datetime import date

from django.db import models


class ActiveMenuManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            .prefetch_related('items')
            .exclude(expiration_date__lt=date.today())
        )
