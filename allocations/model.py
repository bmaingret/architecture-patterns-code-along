from typing import List, Optional, Set
from dataclasses import dataclass, field
from datetime import date, MINYEAR

class OutOfStock(Exception):
    pass

@dataclass(unsafe_hash=True)
class OrderLine:
    order_reference: str
    sku: str
    quantity: int

# class Order:
#     order_reference: str
#     order_lines: List[OrderLine]

@dataclass
class Batch:
    reference: str
    sku: str
    available_quantity: int
    eta: Optional[date] = None
    _allocated_order_lines: Set[OrderLine] = field(default_factory=set, init=False)

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line):
            if order_line not in self._allocated_order_lines:
                self._allocated_order_lines.add(order_line)
                self.available_quantity -= order_line.quantity
        
    def can_allocate(self, order_line: OrderLine):
        available_quantity_enough = self.available_quantity>=order_line.quantity
        sku_matches = self.sku == order_line.sku
        return available_quantity_enough and sku_matches

def allocate(order_line: OrderLine, batches: List[Batch]):
    sorted_batches = sorted(batches, key=lambda batch: batch.eta or date(MINYEAR,1,1))
    for batch in sorted_batches:
        if batch.can_allocate(order_line):
            batch.allocate(order_line)
            return batch.reference
    raise OutOfStock(f'No stock left for order_line {order_line.order_reference}, sku {order_line.sku}')