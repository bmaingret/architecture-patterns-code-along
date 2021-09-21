from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry  # type: ignore
from sqlalchemy.orm import relationship
from allocations.domain.model import OrderLine, Batch

metadata_obj = MetaData()
mapper_registry = registry(metadata_obj)

batches_table = Table(
    "batches",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("reference", String(50)),
    Column("sku", String(50)),
    Column("available_quantity", Integer),
)

order_lines_table = Table(
    "order_lines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_reference", String(50)),
    Column("sku", String(50)),
    Column("quantity", Integer),
)

allocations_table = Table(
    "allocations",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("batch_id", Integer, ForeignKey("batches.id")),
    Column("order_line_id", Integer, ForeignKey("order_lines.id")),
)


def map_allocations():
    mapper_registry.map_imperatively(OrderLine, order_lines_table)
    mapper_registry.map_imperatively(
        Batch,
        batches_table,
        properties={
            "_allocated_order_lines": relationship(
                OrderLine,
                secondary=allocations_table,
                collection_class=set,
            )
        },
    )


map_allocations()
