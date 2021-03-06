import requests
from djpubsubhubbub.signals import updated

from .models import Feed, FeedEntry


def update_handler(sender, update, **kwargs):
    """
    Process new content being provided from SuperFeedr

    """

    feeds = Feed.objects.filter(feed_url=sender.topic)

    for feed in feeds:
        for entry in update.entries:
            r = requests.get(entry['link'])
            feed_entry, created = FeedEntry.objects.get_or_create(
                link=r.url,
                feed=feed,
                defaults={
                    'title': entry['title'],
                    'summary': entry['summary']
                }
            )

            if created:
                feed_entry.add_to_kipt()

updated.connect(update_handler, dispatch_uid='superfeedr')
