from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
import uuid

@dataclass
class FacturaItem:
    id_producto: str
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float

@dataclass
class FacturaModel:
    id_tienda: str
    items: List[FacturaItem] = field(default_factory=list)
    total: float = 0.0
    fecha: str = field(default_factory=lambda: datetime.now().isoformat())
    id_venta: str = field(default_factory=lambda: str(uuid.uuid4()))
