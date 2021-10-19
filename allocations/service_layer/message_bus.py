from allocations.domain.events import Event
from .handlers import handlers


def handle(event: Event):
    for handler in handlers(type(event)):
        handler(event)
