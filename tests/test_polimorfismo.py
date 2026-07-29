#!/usr/bin/env python
"""Demostración de polimorfismo con métodos de pago."""

from orbitpay.payments import Tarjeta, Transferencia, Wallet
from orbitpay.payments.metodo_pago import MetodoPago


def procesar_pagos(metodos: list[MetodoPago], montos: list[float]) -> None:
    """Procesar pagos polimórficamente.
    
    Esta función demuestra POLIMORFISMO: procesa cualquier objeto
    que implemente MetodoPago, sin importar su tipo concreto.
    
    Args:
        metodos: Lista de métodos de pago (cualquier subtipo de MetodoPago)
        montos: Lista de montos a procesar
    """
    print("\n" + "=" * 60)
    print("🔄 PROCESANDO PAGOS POLIMÓRFICAMENTE")
    print("=" * 60)
    
    for i, (metodo, monto) in enumerate(zip(metodos, montos), 1):
        print(f"\n{i}. Método: {metodo.__class__.__name__}")
        print(f"   Monto: ${monto:.2f}")
        print(f"   Representación: {metodo}")
        
        # VALIDAR: Verificar que el método es válido
        es_valido = metodo.validar()
        print(f"   ✅ Validación: {'Válido' if es_valido else 'Inválido'}")
        
        if not es_valido:
            print("   ❌ Pago rechazado: método inválido")
            continue
        
        # PROCESAR: Polimorfismo en acción
        # Python decide qué método procesar() ejecutar según el tipo real
        resultado = metodo.procesar(monto)
        print(f"   {'✅ Pago exitoso' if resultado else '❌ Pago fallido'}")
        print(f"   Saldo restante: ${metodo.saldo_disponible:.2f}")


def demo_polimorfismo():
    """Demostrar polimorfismo con diferentes métodos de pago."""
    print("=" * 60)
    print("🔬 DEMOSTRACIÓN DE POLIMORFISMO")
    print("=" * 60)
    
    # Crear diferentes métodos de pago (todos son MetodoPago)
    metodos = [
        Tarjeta(
            numero="4111111111111111",
            titular="Juan Perez",
            cvv="123",
            fecha_exp="12/26",
            saldo_disponible=2000.0
        ),
        Transferencia(
            banco="Banco Ejemplo",
            cuenta="1234567890",
            clabe="123456789012345678",
            saldo_disponible=5000.0
        ),
        Wallet(
            email="usuario@ejemplo.com",
            saldo_disponible=1000.0
        ),
        # Tarjeta inválida (número incorrecto)
        Tarjeta(
            numero="1234",
            titular="Invalido",
            cvv="12",
            fecha_exp="12/26",
            saldo_disponible=1000.0
        ),
    ]
    
    # Montos para cada pago
    montos = [150.0, 300.0, 50.0, 100.0]
    
    # Procesar pagos (POLIMORFISMO)
    procesar_pagos(metodos, montos)
    
    print("\n" + "=" * 60)
    print("✅ POLIMORFISMO DEMOSTRADO")
    print("=" * 60)
    print("   - El motor procesa cualquier MetodoPago")
    print("   - Sin condicionales (if/elif) por tipo")
    print("   - Cada método sabe cómo procesarse a sí mismo")
    print("   - Liskov (LSP): cualquier subtipo puede sustituir a la base")
    print("=" * 60)


if __name__ == "__main__":
    demo_polimorfismo()