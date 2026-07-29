"""Módulo de la clase Cuenta."""

from dataclasses import dataclass, field
from typing import List
from datetime import datetime
import uuid

from orbitpay.domain.transaccion import Transaccion
from orbitpay.domain.suscripcion import Suscripcion


class SaldoInsuficienteError(Exception):
    """Excepción cuando el saldo es insuficiente para una operación."""
    pass


class MontoInvalidoError(Exception):
    """Excepción cuando el monto es inválido (negativo o cero)."""
    pass


@dataclass
class Cuenta:
    """Representa una cuenta de usuario en OrbitPay.
    
    Atributos:
        id: Identificador único de la cuenta
        titular: Nombre del propietario de la cuenta
        _saldo: Saldo actual (protegido, acceder via @property)
        transacciones: Historial de transacciones
        suscripciones: Suscripciones activas del usuario
    """
    
    id: str
    titular: str
    _saldo: float = 0.0
    transacciones: List[Transaccion] = field(default_factory=list)
    suscripciones: List[Suscripcion] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Validar invariantes después de la creación."""
        if self._saldo < 0:
            raise ValueError(f"El saldo inicial no puede ser negativo: {self._saldo}")
        
        if not self.titular or not self.titular.strip():
            raise ValueError("El titular no puede estar vacío")
    
    @property
    def saldo(self) -> float:
        """Obtener el saldo actual de la cuenta (lectura)."""
        return self._saldo
    
    def depositar(self, monto: float, descripcion: str = "Depósito") -> Transaccion:
        """Depositar dinero en la cuenta.
        
        Args:
            monto: Cantidad a depositar (debe ser positiva)
            descripcion: Descripción del depósito
            
        Returns:
            Transacción generada
            
        Raises:
            MontoInvalidoError: Si el monto es negativo o cero
        """
        if monto <= 0:
            raise MontoInvalidoError(f"Monto debe ser positivo: {monto}")
        
        self._saldo += monto
        
        transaccion = Transaccion(
            id=str(uuid.uuid4()),
            monto=monto,
            tipo="ingreso",
            fecha=datetime.now(),
            descripcion=descripcion,
            estado="completada"
        )
        
        # ✅ AGREGAR TRANSACCIÓN AL HISTORIAL
        self.transacciones.append(transaccion)
        
        return transaccion
    
    def retirar(self, monto: float, descripcion: str = "Retiro") -> Transaccion:
        """Retirar dinero de la cuenta.
        
        Args:
            monto: Cantidad a retirar (debe ser positiva)
            descripcion: Descripción del retiro
            
        Returns:
            Transacción generada
            
        Raises:
            MontoInvalidoError: Si el monto es negativo o cero
            SaldoInsuficienteError: Si el saldo es insuficiente
        """
        if monto <= 0:
            raise MontoInvalidoError(f"Monto debe ser positivo: {monto}")
        
        if monto > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente: ${self._saldo:.2f} < ${monto:.2f}"
            )
        
        self._saldo -= monto
        
        transaccion = Transaccion(
            id=str(uuid.uuid4()),
            monto=monto,
            tipo="egreso",
            fecha=datetime.now(),
            descripcion=descripcion,
            estado="completada"
        )
        
        # ✅ AGREGAR TRANSACCIÓN AL HISTORIAL
        self.transacciones.append(transaccion)
        
        return transaccion
    
    def agregar_transaccion(self, transaccion: Transaccion) -> None:
        """Agregar una transacción al historial (para casos especiales)."""
        self.transacciones.append(transaccion)
    
    def agregar_suscripcion(self, suscripcion: Suscripcion) -> None:
        """Agregar una suscripción a la cuenta."""
        self.suscripciones.append(suscripcion)
    
    def obtener_historial(self) -> List[Transaccion]:
        """Obtener el historial completo de transacciones."""
        return self.transacciones.copy()
    
    def obtener_suscripciones_activas(self) -> List[Suscripcion]:
        """Obtener las suscripciones activas."""
        return [s for s in self.suscripciones if s.activa]
    
    def __repr__(self) -> str:
        """Representación legible de la cuenta."""
        return (
            f"Cuenta(id='{self.id[:8]}...', "
            f"titular='{self.titular}', "
            f"saldo=${self._saldo:.2f}, "
            f"transacciones={len(self.transacciones)}, "
            f"suscripciones={len(self.suscripciones)})"
        )
    
    def __eq__(self, other: object) -> bool:
        """Comparar cuentas por ID."""
        if not isinstance(other, Cuenta):
            return NotImplemented
        return self.id == other.id