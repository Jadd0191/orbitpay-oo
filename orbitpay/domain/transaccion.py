"""Módulo de la clase Transacción."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Transaccion:
    """Representa una transacción financiera inmutable.
    
    Atributos:
        id: Identificador único de la transacción
        monto: Cantidad de dinero movida (siempre positiva)
        tipo: "ingreso" o "egreso"
        fecha: Fecha y hora de la transacción
        descripcion: Descripción textual de la operación
        estado: "pendiente", "completada" o "fallida"
    """
    
    id: str
    monto: float
    tipo: str  # "ingreso" | "egreso"
    fecha: datetime
    descripcion: str
    estado: str  # "pendiente" | "completada" | "fallida"
    
    def __post_init__(self) -> None:
        """Validar invariantes después de la creación."""
        # Validar monto positivo
        if self.monto <= 0:
            raise ValueError(f"El monto debe ser positivo: {self.monto}")
        
        # Validar tipo válido
        if self.tipo not in ("ingreso", "egreso"):
            raise ValueError(f"Tipo inválido: {self.tipo}. Debe ser 'ingreso' o 'egreso'")
        
        # Validar estado válido
        if self.estado not in ("pendiente", "completada", "fallida"):
            raise ValueError(f"Estado inválido: {self.estado}")
    
    def __repr__(self) -> str:
        """Representación legible de la transacción."""
        return (
            f"Transaccion(id='{self.id[:8]}...', "
            f"monto=${self.monto:.2f}, "
            f"tipo='{self.tipo}', "
            f"estado='{self.estado}', "
            f"fecha={self.fecha.strftime('%Y-%m-%d %H:%M')})"
        )
    
    def __eq__(self, other: object) -> bool:
        """Comparar transacciones por ID."""
        if not isinstance(other, Transaccion):
            return NotImplemented
        return self.id == other.id
    
    def __lt__(self, other: 'Transaccion') -> bool:
        """Comparar transacciones por monto (para ordenar)."""
        if not isinstance(other, Transaccion):
            return NotImplemented
        return self.monto < other.monto
    
    def __hash__(self) -> int:
        """Hash basado en ID (por ser frozen)."""
        return hash(self.id)