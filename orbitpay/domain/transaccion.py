"""Módulo de la clase Transacción."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Transaccion:
    """Representa una transacción financiera inmutable."""
    
    id: str
    monto: float
    tipo: str  # "ingreso" | "egreso"
    fecha: datetime
    descripcion: str
    estado: str  # "pendiente" | "completada" | "fallida"
    
    def __repr__(self) -> str:
        """Representación legible de la transacción."""
        ...
    
    def __eq__(self, other: object) -> bool:
        """Comparar transacciones por ID."""
        ...
    
    def __lt__(self, other: 'Transaccion') -> bool:
        """Comparar transacciones por monto."""
        ...