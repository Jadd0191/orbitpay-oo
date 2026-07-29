#!/usr/bin/env python
"""Prueba de integración completa del sistema."""

import uuid
from datetime import datetime

from orbitpay import (
    Cuenta,
    Tarjeta,
    Transferencia,
    Wallet,
    MetodoPagoFactory,
    ComisionFija,
    ComisionPorcentual,
    ComisionEscalonada,
    ObservadorCorreo,
    ObservadorContabilidad,
    ObservadorLogger,
    Engine,
)


def demo_sistema_completo():
    """Demostrar el sistema completo con todos los patrones."""
    print("=" * 70)
    print("🚀 ORBITPAY OO - DEMOSTRACIÓN COMPLETA")
    print("=" * 70)
    
    # 1. Crear cuenta
    print("\n📋 1. CREANDO CUENTA")
    print("-" * 50)
    cuenta = Cuenta(
        id=str(uuid.uuid4()),
        titular="Juan Perez",
        _saldo=1000.0
    )
    print(f"✅ Cuenta creada: {cuenta.titular}")
    print(f"💰 Saldo inicial: ${cuenta.saldo:.2f}")
    
    # 2. Crear motor con estrategia y observadores
    print("\n⚙️ 2. CONFIGURANDO MOTOR")
    print("-" * 50)
    
    # Strategy: Comisión escalonada
    estrategia = ComisionEscalonada()
    print(f"✅ Estrategia de comisión: Escalonada")
    
    # Observer: Gestor de eventos
    gestor = GestorEventos()
    
    # Observadores
    observador_correo = ObservadorCorreo()
    observador_contabilidad = ObservadorContabilidad()
    observador_logger = ObservadorLogger()
    
    gestor.suscribir(observador_correo)
    gestor.suscribir(observador_contabilidad)
    gestor.suscribir(observador_logger)
    print(f"✅ Observadores: Correo, Contabilidad, Logger")
    
    # Crear motor
    engine = Engine(strategy=estrategia, gestor_eventos=gestor)
    print(f"✅ Motor creado")
    
    # 3. Crear método de pago con Factory
    print("\n🏦 3. CREANDO MÉTODO DE PAGO")
    print("-" * 50)
    
    # Usando Factory para crear una tarjeta
    tarjeta = MetodoPagoFactory.crear_tarjeta(
        numero="4111111111111111",
        titular="Juan Perez",
        cvv="123",
        fecha_exp="12/26",
        saldo_disponible=2000.0
    )
    print(f"✅ Método de pago: {tarjeta.__class__.__name__}")
    print(f"   {tarjeta}")
    
    # 4. Procesar pago
    print("\n💳 4. PROCESANDO PAGO")
    print("-" * 50)
    
    resultado = engine.procesar_pago(
        cuenta=cuenta,
        metodo_pago=tarjeta,
        monto=150.0,
        descripcion="Compra en tienda online"
    )
    
    # 5. Mostrar resultados
    print("\n📊 5. RESULTADOS FINALES")
    print("-" * 50)
    print(f"💰 Saldo final: ${cuenta.saldo:.2f}")
    print(f"📝 Transacciones: {len(cuenta.transacciones)}")
    
    # Mostrar historial de transacciones
    print("\n📝 Historial de transacciones:")
    for t in cuenta.transacciones:
        print(f"  • {t.fecha.strftime('%H:%M:%S')} | {t.tipo:7} | "
              f"${t.monto:8.2f} | {t.descripcion[:30]}...")
    
    # 6. Cambiar estrategia y probar otro pago
    print("\n🔄 6. CAMBIANDO ESTRATEGIA DE COMISIÓN")
    print("-" * 50)
    
    engine.cambiar_estrategia(ComisionFija(3.0))
    print(f"✅ Nueva estrategia: Comisión Fija (${3.0:.2f})")
    
    # Crear otro método de pago con Factory
    wallet = MetodoPagoFactory.crear_wallet(
        email="juan.perez@email.com",
        saldo_disponible=500.0
    )
    print(f"✅ Nuevo método: {wallet.__class__.__name__}")
    
    # Procesar segundo pago
    resultado2 = engine.procesar_pago(
        cuenta=cuenta,
        metodo_pago=wallet,
        monto=50.0,
        descripcion="Suscripción mensual"
    )
    
    # 7. Mostrar resumen final
    print("\n📊 7. RESUMEN FINAL")
    print("=" * 70)
    print(f"💰 Saldo final: ${cuenta.saldo:.2f}")
    print(f"📊 Total transacciones: {len(cuenta.transacciones)}")
    print(f"📧 Correos enviados: {len(observador_contabilidad.eventos)} eventos registrados")
    print(f"📝 Logs generados: {len(observador_logger.logs)}")
    
    print("\n✅ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)


if __name__ == "__main__":
    demo_sistema_completo()