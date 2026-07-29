"""Módulo de la clase Suscripción."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class Suscripcion:
    """Representa una suscripción a un servicio.
    
    Atributos:
        id: Identificador único
        nombre: Nombre del servicio
        monto: Costo periódico (debe ser positivo)
        periodicidad: "mensual", "trimestral" o "anual"
        fecha_inicio: Fecha de inicio de la suscripción
        fecha_fin: Fecha de fin (None si no tiene)
        activa: Estado de la suscripción
    """
    
    id: str
    nombre: str
    monto: float
    periodicidad: str  # "mensual" | "trimestral" | "anual"
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    activa: bool = True
    
    def __post_init__(self) -> None:
        """Validar invariantes después de la creación."""
        # Validar monto positivo
        if self.monto <= 0:
            raise ValueError(f"El monto debe ser positivo: {self.monto}")
        
        # Validar periodicidad válida
        if self.periodicidad not in ("mensual", "trimestral", "anual"):
            raise ValueError(f"Periodicidad inválida: {self.periodicidad}")
        
        # Validar que fecha_fin sea posterior a fecha_inicio si existe
        if self.fecha_fin and self.fecha_fin <= self.fecha_inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
    
    def renovar(self, duracion: int) -> None:
        """Renovar la suscripción por un número de períodos.
        
        Args:
            duracion: Número de períodos a renovar (debe ser > 0)
            
        Raises:
            ValueError: Si la suscripción no está activa o duracion es inválida
        """
        if not self.activa:
            raise ValueError("No se puede renovar una suscripción inactiva")
        
        if duracion <= 0:
            raise ValueError(f"La duración debe ser positiva: {duracion}")
        
        # Calcular nueva fecha de fin
        if self.fecha_fin is None:
            # Si no tiene fecha fin, usar fecha_inicio
            base_fecha = self.fecha_inicio
        else:
            base_fecha = self.fecha_fin
        
        # Extender según periodicidad
        if self.periodicidad == "mensual":
            self.fecha_fin = base_fecha + timedelta(days=30 * duracion)
        elif self.periodicidad == "trimestral":
            self.fecha_fin = base_fecha + timedelta(days=90 * duracion)
        elif self.periodicidad == "anual":
            self.fecha_fin = base_fecha + timedelta(days=365 * duracion)
        
        self.activa = True
    
    def cancelar(self) -> None:
        """Cancelar la suscripción."""
        self.activa = False
        self.fecha_fin = datetime.now()
    
    def calcular_proximo_pago(self) -> datetime:
        """Calcular la próxima fecha de cobro.
        
        Returns:
            Fecha del próximo pago
            
        Raises:
            ValueError: Si la suscripción no está activa
        """
        if not self.activa:
            raise ValueError("La suscripción no está activa")
        
        if self.fecha_fin is None:
            # Si no tiene fecha fin, calcular desde fecha_inicio
            base = self.fecha_inicio
        else:
            base = self.fecha_fin
        
        # Calcular próximo pago según periodicidad
        if self.periodicidad == "mensual":
            return base + timedelta(days=30)
        elif self.periodicidad == "trimestral":
            return base + timedelta(days=90)
        elif self.periodicidad == "anual":
            return base + timedelta(days=365)
        else:
            raise ValueError(f"Periodicidad no soportada: {self.periodicidad}")
    
    def __repr__(self) -> str:
        """Representación legible de la suscripción."""
        estado = "activa" if self.activa else "inactiva"
        return (
            f"Suscripcion(id='{self.id[:8]}...', "
            f"nombre='{self.nombre}', "
            f"monto=${self.monto:.2f}, "
            f"periodicidad='{self.periodicidad}', "
            f"estado='{estado}')"
        )
    
    def __eq__(self, other: object) -> bool:
        """Comparar suscripciones por ID."""
        if not isinstance(other, Suscripcion):
            return NotImplemented
        return self.id == other.id