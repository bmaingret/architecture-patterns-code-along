from typing import Dict, Type, List, Callable
from allocations.domain import events
from allocations.domain.model import OutOfStock

_handlers = {}  # type: Dict[Type[events.Event], List[Callable]]


def handlers(event_type: Type[events.Event]) -> List[Callable]:
    return _handlers.get(event_type, [])


def add_handler(event_type: Type[events.Event], handler: Callable):
    _handlers[event_type] = _handlers.get(event_type, []).append(handler)  # type: ignore


add_handler(events.OutOfStockEvent, lambda: (_ for _ in ()).throw(OutOfStock()))
