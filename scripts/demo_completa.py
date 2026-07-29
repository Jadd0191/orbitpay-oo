#!/usr/bin/env python
"""Demo completa del sistema OrbitPay OO.

Este script muestra el flujo completo de pago con todas las funcionalidades.
"""

import uuid
from datetime import datetime
import sys
import os

# Agregar la raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orbitpay import (
    Cuenta,
    MetodoPagoFactory,
    ComisionEscalonada,
    ObservadorCorreo,
    ObservadorContabilidad,
    ObservadorLogger,
    GestorEventos,
    Engine,
    Suscripcion,
)


def main():
    """Ejecutar demostración completa."""
    print("=" * 70)
    print("🚀 ORBITPAY OO - DEMOSTRACIÓN COMPLETA DEL SISTEMA")
    print("=" * 70)
    
    print("\n📋 1. CREANDO CUENTA Y CONFIGURANDO MOTOR")
    print("-" * 50)
    
    # Crear cuenta
    cuenta = Cuenta(
        id=str(uuid.uuid4()),
        titular="Juan Perez",
        _saldo=2000.0
    )
    print(f"✅ Cuenta creada: {cuenta.titular}")
    print(f"💰 Saldo inicial: ${cuenta.saldo:.2f}")
    
    # Configurar motor con estrategia y observadores
    gestor = GestorEventos()
    gestor.suscribir(ObservadorCorreo())
    gestor.suscribir(ObservadorContabilidad())
    gestor.suscribir(ObservadorLogger())
    
    engine = Engine(
        strategy=ComisionEscalonada(),
        gestor_eventos=gestor
    )
    print(f"✅ Motor configurado con comisión escalonada")
    print(f"✅ Observadores: Correo, Contabilidad, Logger")
    
    print("\n🏦 2. CREANDO MÉTODOS DE PAGO CON FACTORY")
    print("-" * 50)
    
    # Crear métodos de pago usando Factory
    tarjeta = MetodoPagoFactory.crear_tarjeta(
        numero="4111111111111111",
        titular="Juan Perez",
        cvv="123",
        fecha_exp="12/26",
        saldo_disponible=3000.0
    )
    print(f"✅ Tarjeta creada: {tarjeta}")
    
    transferencia = MetodoPagoFactory.crear_transferencia(
        banco="Banco Nacional",
        cuenta="1234567890",
        clabe="123456789012345678",
        saldo_disponible=5000.0
    )
    print(f"✅ Transferencia creada: {transferencia}")
    
    wallet = MetodoPagoFactory.crear_wallet(
        email="juan.perez@email.com",
        saldo_disponible=1000.0
    )
    print(f"✅ Wallet creada: {wallet}")
    
    # Crear suscripción
    suscripcion = Suscripcion(
        id=str(uuid.uuid4()),
        nombre="Netflix Premium",
        monto=99.0,
        periodicidad="mensual",
        fecha_inicio=datetime.now()
    )
    cuenta.agregar_suscripcion(suscripcion)
    print(f"✅ Suscripción creada: {suscripcion.nombre} (${suscripcion.monto:.2f}/mes)")
    
    print("\n💳 3. PROCESANDO PAGOS")
    print("-" * 50)
    
    # Pago 1: Compra con tarjeta
    print("\n--- Pago 1: Compra en tienda (Tarjeta) ---")
    resultado1 = engine.procesar_pago(
        cuenta=cuenta,
        metodo_pago=tarjeta,
        monto=150.0,
        descripcion="Compra en tienda online"
    )
    print(f"   Resultado: {'✅ Exitoso' if resultado1 else '❌ Fallido'}")
    
    # Pago 2: Suscripción con wallet
    print("\n--- Pago 2: Suscripción mensual (Wallet) ---")
    resultado2 = engine.procesar_pago(
        cuenta=cuenta,
        metodo_pago=wallet,
        monto=suscripcion.monto,
        descripcion=f"Suscripción: {suscripcion.nombre}"
    )
    print(f"   Resultado: {'✅ Exitoso' if resultado2 else '❌ Fallido'}")
    
    # Pago 3: Transferencia a proveedor
    print("\n--- Pago 3: Transferencia a proveedor (Transferencia) ---")
    resultado3 = engine.procesar_pago(
        cuenta=cuenta,
        metodo_pago=transferencia,
        monto=250.0,
        descripcion="Pago a proveedor"
    )
    print(f"   Resultado: {'✅ Exitoso' if resultado3 else '❌ Fallido'}")
    
    print("\n📊 4. RESUMEN FINAL")
    print("=" * 70)
    print(f"💰 Saldo final: ${cuenta.saldo:.2f}")
    print(f"📊 Transacciones totales: {len(cuenta.transacciones)}")
    print(f"📝 Suscripciones activas: {len(cuenta.obtener_suscripciones_activas())}")
    
    # Mostrar historial de transacciones
    print("\n📝 Historial de transacciones:")
    for i, t in enumerate(cuenta.transacciones, 1):
        print(f"   {i}. {t.fecha.strftime('%Y-%m-%d %H:%M')} | "
              f"{t.tipo:7} | ${t.monto:8.2f} | {t.descripcion[:30]}")
    
    print("\n✅ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print("\n📌 Resumen de características demostradas:")
    print("   ✅ Cuenta con encapsulamiento e invariantes")
    print("   ✅ Jerarquía de métodos de pago (herencia + polimorfismo)")
    print("   ✅ Factory Pattern para creación de métodos")
    print("   ✅ Strategy Pattern para comisiones intercambiables")
    print("   ✅ Observer Pattern para notificaciones")
    print("   ✅ Engine que orquesta todo el flujo")
    print("   ✅ Suscripciones y gestión de servicios recurrentes")
    print("   ✅ Manejo de errores y reversión de transacciones")
    print("=" * 70)


if __name__ == "__main__":
    main()