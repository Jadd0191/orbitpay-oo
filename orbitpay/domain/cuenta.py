"""Módulo de la clase Cuenta."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from orbitpay.domain.transaccion import Transaccion
from orbitpay.domain.suscripcion import Suscripcion


@dataclass
class Cuenta:
    """Representa una cuenta de usuario en OrbitPay."""
    
    id: str
    titular: str
    _saldo: float = 0.0
    transacciones: List[Transaccion] = field(default_factory=list)
    suscripciones: List[Suscripcion] = field(default_factory=list)
    
    @property
    def saldo(self) -> float:
        """Obtener el saldo actual de la cuenta."""
        return self._saldo
    
    def depositar(self, monto: float) -> None:
        """Depositar dinero en la cuenta.
        
        Args:
            monto: Cantidad a depositar (debe ser positiva)
            
        Raises:
            ValueError: Si el monto es negativo o cero
        """
        ...
    
    def retirar(self, monto: float) -> None:
        """Retirar dinero de la cuenta.
        
        Args:
            monto: Cantidad a retirar (debe ser positiva)
            
        Raises:
            ValueError: Si el monto es negativo, cero o excede el saldo
        """
        ...
    
    def agregar_transaccion(self, transaccion: Transaccion) -> None:
        """Agregar una transacción al historial."""
        ...
    
    def agregar_suscripcion(self, suscripcion: Suscripcion) -> None:
        """Agregar una suscripción a la cuenta."""
        ...