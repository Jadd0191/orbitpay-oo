#!/usr/bin/env python
"""
Prototipo para validar la integridad del saldo.

Riesgo: R-02 (Saldo inconsistente)
Objetivo: Demostrar que el saldo nunca queda negativo.
"""

from dataclasses import dataclass, field
from typing import List


class SaldoNegativoError(Exception):
    """Excepción cuando el saldo quedaría negativo."""
    pass


@dataclass
class CuentaConValidacion:
    """Cuenta con validación estricta de saldo."""
    
    id: str
    titular: str
    _saldo: float = 0.0
    _historial_saldos: List[float] = field(default_factory=list)
    
    @property
    def saldo(self) -> float:
        return self._saldo
    
    @property
    def historial_saldos(self) -> List[float]:
        return self._historial_saldos.copy()
    
    def _validar_saldo(self, monto: float) -> None:
        """Validar que el saldo no quede negativo."""
        if self._saldo - monto < 0:
            raise SaldoNegativoError(
                f"Saldo quedaría negativo: {self._saldo} - {monto} = {self._saldo - monto}"
            )
    
    def retirar(self, monto: float) -> None:
        """Retirar con validación de saldo."""
        if monto <= 0:
            raise ValueError("Monto debe ser positivo")
        
        # VALIDACIÓN CRÍTICA
        self._validar_saldo(monto)
        
        # Ejecutar operación
        self._saldo -= monto
        self._historial_saldos.append(self._saldo)
    
    def depositar(self, monto: float) -> None:
        """Depositar dinero."""
        if monto <= 0:
            raise ValueError("Monto debe ser positivo")
        
        self._saldo += monto
        self._historial_saldos.append(self._saldo)


def demo_prototipo():
    """Demostrar el prototipo."""
    print("=" * 60)
    print("🔬 PROTOTIPO: Validación de Saldo")
    print("=" * 60)
    
    cuenta = CuentaConValidacion(
        id="demo-002",
        titular="Usuario Validación",
        _saldo=500.0
    )
    
    print(f"\n✅ Cuenta creada: {cuenta.titular}")
    print(f"💰 Saldo inicial: ${cuenta.saldo:.2f}")
    
    print("\n" + "=" * 60)
    print("🧪 ESCENARIO: Operaciones mixtas")
    print("=" * 60)
    
    operaciones = [
        ("Depósito", 200.0),
        ("Retiro", 100.0),
        ("Retiro", 300.0),
        ("Depósito", 50.0),
        ("Retiro", 400.0),  # Este debería fallar
        ("Depósito", 1000.0),
    ]
    
    for i, (tipo, monto) in enumerate(operaciones, 1):
        print(f"\n{i}. {tipo} ${monto:.2f}")
        print(f"   Saldo actual: ${cuenta.saldo:.2f}")
        
        try:
            if tipo == "Depósito":
                cuenta.depositar(monto)
            else:
                cuenta.retirar(monto)
            print(f"   ✅ Operación exitosa")
            print(f"   Nuevo saldo: ${cuenta.saldo:.2f}")
        except SaldoNegativoError as e:
            print(f"   ❌ Error (esperado): {e}")
            print(f"   Saldo no modificado: ${cuenta.saldo:.2f}")
        except ValueError as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("📊 ANÁLISIS DE INTEGRIDAD")
    print("=" * 60)
    
    # Verificar que ningún saldo es negativo
    saldos_negativos = [s for s in cuenta.historial_saldos if s < 0]
    
    print(f"💰 Saldo final: ${cuenta.saldo:.2f}")
    print(f"📊 Total operaciones: {len(cuenta.historial_saldos)}")
    print(f"🔍 Saldos negativos detectados: {len(saldos_negativos)}")
    
    if len(saldos_negativos) == 0:
        print("\n✅ VALIDACIÓN EXITOSA: Ningún saldo negativo registrado")
        print("   - Las operaciones que hubieran causado saldo negativo fueron bloqueadas")
    else:
        print(f"\n❌ ERROR: Se detectaron {len(saldos_negativos)} saldos negativos")
        print(f"   Historial: {saldos_negativos}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo_prototipo()