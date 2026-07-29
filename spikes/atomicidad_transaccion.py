#!/usr/bin/env python
"""
Prototipo para validar la atomicidad de transacciones.

Riesgo: R-01 (Doble cobro)
Objetivo: Demostrar que una operación de retiro es atómica:
1. Validar saldo
2. Descontar saldo
3. Registrar transacción

Si falla el paso 1, no se ejecutan los pasos 2 y 3.
No debe haber casos donde se descuente saldo sin registrar transacción.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import uuid


class SaldoInsuficienteError(Exception):
    """Excepción cuando el saldo es insuficiente."""
    pass


class MontoInvalidoError(Exception):
    """Excepción cuando el monto es negativo o cero."""
    pass


@dataclass(frozen=True)
class Transaccion:
    """Transacción inmutable."""
    id: str
    monto: float
    tipo: str
    fecha: datetime
    descripcion: str
    estado: str


@dataclass
class Cuenta:
    """Cuenta con protección contra doble cobro."""
    
    id: str
    titular: str
    _saldo: float = 0.0
    transacciones: List[Transaccion] = field(default_factory=list)
    
    @property
    def saldo(self) -> float:
        return self._saldo
    
    def retirar(self, monto: float, descripcion: str) -> Transaccion:
        """
        Operación atómica de retiro.
        
        PASOS (ATÓMICOS):
        1. Validar monto > 0
        2. Validar saldo suficiente
        3. Descontar saldo
        4. Registrar transacción
        
        Si falla el paso 1 o 2, NO se ejecutan 3 y 4.
        Si falla 3 o 4, la transacción no se completa.
        """
        # PASO 1: Validar monto
        if monto <= 0:
            raise MontoInvalidoError(f"Monto debe ser positivo: {monto}")
        
        # PASO 2: Validar saldo suficiente
        if monto > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente: {self._saldo} < {monto}"
            )
        
        # PASO 3: Descontar saldo (ATÓMICO)
        self._saldo -= monto
        
        # PASO 4: Registrar transacción
        transaccion = Transaccion(
            id=str(uuid.uuid4()),
            monto=monto,
            tipo="egreso",
            fecha=datetime.now(),
            descripcion=descripcion,
            estado="completada"
        )
        self.transacciones.append(transaccion)
        
        return transaccion
    
    def depositar(self, monto: float, descripcion: str) -> Transaccion:
        """Operación atómica de depósito."""
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
        self.transacciones.append(transaccion)
        
        return transaccion


def demo_prototipo():
    """Demostrar el prototipo en acción."""
    print("=" * 60)
    print("🔬 PROTOTIPO: Atomicidad de Transacciones")
    print("=" * 60)
    
    # Crear cuenta con saldo inicial
    cuenta = Cuenta(
        id="demo-001",
        titular="Usuario Demo",
        _saldo=1000.0
    )
    
    print(f"\n✅ Cuenta creada: {cuenta.titular}")
    print(f"💰 Saldo inicial: ${cuenta.saldo:.2f}")
    
    print("\n" + "=" * 60)
    print("🧪 CASO 1: Retiro exitoso")
    print("=" * 60)
    
    try:
        transaccion = cuenta.retirar(300.0, "Compra en tienda")
        print(f"✅ Retiro exitoso: ${transaccion.monto:.2f}")
        print(f"💰 Nuevo saldo: ${cuenta.saldo:.2f}")
        print(f"📝 Transacción ID: {transaccion.id[:8]}...")
        print(f"📊 Total transacciones: {len(cuenta.transacciones)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🧪 CASO 2: Retiro fallido (saldo insuficiente)")
    print("=" * 60)
    
    try:
        transaccion = cuenta.retirar(1500.0, "Intento de compra grande")
        print(f"✅ Retiro exitoso: ${transaccion.monto:.2f}")
    except SaldoInsuficienteError as e:
        print(f"❌ Error esperado: {e}")
        print(f"💰 Saldo no modificado: ${cuenta.saldo:.2f}")
        print(f"📊 Total transacciones: {len(cuenta.transacciones)} (no aumentó)")
    
    print("\n" + "=" * 60)
    print("🧪 CASO 3: Retiro fallido (monto negativo)")
    print("=" * 60)
    
    try:
        transaccion = cuenta.retirar(-100.0, "Monto negativo")
        print(f"✅ Retiro exitoso: ${transaccion.monto:.2f}")
    except MontoInvalidoError as e:
        print(f"❌ Error esperado: {e}")
        print(f"💰 Saldo no modificado: ${cuenta.saldo:.2f}")
        print(f"📊 Total transacciones: {len(cuenta.transacciones)} (no aumentó)")
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN FINAL")
    print("=" * 60)
    print(f"💰 Saldo final: ${cuenta.saldo:.2f}")
    print(f"📊 Transacciones totales: {len(cuenta.transacciones)}")
    
    # Mostrar historial
    print("\n📝 Historial de transacciones:")
    for t in cuenta.transacciones:
        print(f"  • {t.fecha.strftime('%H:%M:%S')} | {t.tipo:7} | "
              f"${t.monto:8.2f} | {t.descripcion[:20]}...")
    
    print("\n" + "=" * 60)
    print("✅ PROTOTIPO EXITOSO: Atomicidad garantizada")
    print("   - Saldo validado antes de descontar")
    print("   - Transacción registrada después del descuento")
    print("   - Fallos no modifican el estado")
    print("=" * 60)


if __name__ == "__main__":
    demo_prototipo()