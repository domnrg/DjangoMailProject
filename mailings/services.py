from django.core.cache import cache
from mailings.models import Mailing, Client


def get_statistics():
    stats = cache.get("mailing_stats")

    if stats is None:
        stats = {
            "total_mailings": Mailing.objects.count(),
            "active_mailings": Mailing.objects.filter(status="запущена").count(),
            "unique_recipients": Client.objects.distinct().count(),
        }
        cache.set("mailing_stats", stats, 300)

    return stats
