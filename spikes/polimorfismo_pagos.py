#!/usr/bin/env python
"""
Prototipo para validar el polimorfismo de métodos de pago.

Riesgo: R-04 (Acoplamiento excesivo)
Objetivo: Demostrar que el motor puede procesar diferentes métodos de pago
sin conocer sus implementaciones concretas.
"""

from abc import ABC, abstractmethod
from typing import List


class MetodoPago(ABC):
    """Interfaz abstracta para métodos de pago."""
    
    @abstractmethod
    def procesar(self, monto: float) -> bool:
        """Procesar el pago."""
        pass
    
    @abstractmethod
    def validar(self) -> bool:
        """Validar que el método es operable."""
        pass


class Tarjeta(MetodoPago):
    """Pago con tarjeta de crédito."""
    
    def __init__(self, numero: str, titular: str, cvv: str):
        self.numero = numero
        self.titular = titular
        self.cvv = cvv
    
    def procesar(self, monto: float) -> bool:
        print(f"  💳 Procesando tarjeta {self.numero[-4:]} por ${monto:.2f}")
        # Simular autorización
        return True
    
    def validar(self) -> bool:
        print(f"  ✅ Validando tarjeta {self.numero[-4:]}")
        return len(self.numero) == 16 and len(self.cvv) == 3


class Transferencia(MetodoPago):
    """Pago con transferencia bancaria."""
    
    def __init__(self, banco: str, clabe: str):
        self.banco = banco
        self.clabe = clabe
    
    def procesar(self, monto: float) -> bool:
        print(f"  🏦 Procesando transferencia {self.banco} por ${monto:.2f}")
        return True
    
    def validar(self) -> bool:
        print(f"  ✅ Validando CLABE {self.clabe[:4]}...")
        return len(self.clabe) == 18


class Wallet(MetodoPago):
    """Pago con billetera digital."""
    
    def __init__(self, email: str):
        self.email = email
    
    def procesar(self, monto: float) -> bool:
        print(f"  📱 Procesando wallet {self.email} por ${monto:.2f}")
        return True
    
    def validar(self) -> bool:
        print(f"  ✅ Validando email {self.email}")
        return "@" in self.email


class MotorPagos:
    """Motor que procesa pagos polimórficamente."""
    
    def __init__(self):
        self.historial: List[dict] = []
    
    def procesar_pago(self, metodo: MetodoPago, monto: float) -> bool:
        """
        Procesar pago usando cualquier método que implemente MetodoPago.
        
        POLIMORFISMO: No importa el tipo concreto, solo importa que
        implemente la interfaz MetodoPago.
        """
        print(f"\n📦 Procesando pago de ${monto:.2f}")
        
        # Validar antes de procesar
        if not metodo.validar():
            print("  ❌ Método de pago inválido")
            return False
        
        # Procesar polimórficamente
        resultado = metodo.procesar(monto)
        
        # Registrar
        self.historial.append({
            "metodo": metodo.__class__.__name__,
            "monto": monto,
            "resultado": resultado
        })
        
        return resultado
    
    def mostrar_historial(self):
        """Mostrar historial de pagos."""
        print("\n" + "=" * 60)
        print("📊 HISTORIAL DE PAGOS")
        print("=" * 60)
        for i, pago in enumerate(self.historial, 1):
            estado = "✅" if pago["resultado"] else "❌"
            print(f"{i}. {estado} {pago['metodo']:12} | ${pago['monto']:8.2f}")


def demo_prototipo():
    """Demostrar el prototipo."""
    print("=" * 60)
    print("🔬 PROTOTIPO: Polimorfismo de Pagos")
    print("=" * 60)
    
    # Crear motor
    motor = MotorPagos()
    
    # Crear diferentes métodos de pago
    metodos = [
        Tarjeta("4111111111111111", "Juan Perez", "123"),
        Transferencia("Banco Ejemplo", "123456789012345678"),
        Wallet("usuario@ejemplo.com"),
        Tarjeta("1234", "Invalido", "12"),  # Tarjeta inválida
    ]
    
    # Pagos con diferentes métodos
    montos = [100.0, 250.0, 50.0, 75.0]
    
    print("\n🔄 Procesando pagos con diferentes métodos...")
    for metodo, monto in zip(metodos, montos):
        motor.procesar_pago(metodo, monto)
    
    motor.mostrar_historial()
    
    print("\n" + "=" * 60)
    print("✅ PROTOTIPO EXITOSO: Polimorfismo demostrado")
    print("   - El motor procesa cualquier MetodoPago")
    print("   - Sin condicionales (if/elif) por tipo")
    print("   - Cada método sabe cómo procesarse a sí mismo")
    print("=" * 60)


if __name__ == "__main__":
    demo_prototipo()