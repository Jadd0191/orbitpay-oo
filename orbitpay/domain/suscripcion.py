"""Módulo de la clase Suscripción."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Suscripcion:
    """Representa una suscripción a un servicio."""
    
    id: str
    nombre: str
    monto: float
    periodicidad: str  # "mensual" | "trimestral" | "anual"
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    activa: bool = True
    
    def renovar(self, duracion: int) -> None:
        """Renovar la suscripción por un número de períodos.
        
        Args:
            duracion: Número de períodos a renovar
        """
        ...
    
    def cancelar(self) -> None:
        """Cancelar la suscripción."""
        ...
    
    def calcular_proximo_pago(self) -> datetime:
        """Calcular la próxima fecha de cobro.
        
        Returns:
            Fecha del próximo pago
        """
        ...