"""Pruebas de integración para el flujo completo de OrbitPay."""

import uuid
from datetime import datetime, timedelta

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
    GestorEventos,
    Engine,
    Suscripcion,
)


class TestFlujoCompleto:
    """Pruebas de integración del flujo completo."""
    
    def test_flujo_pago_completo(self):
        """Probar flujo completo de pago."""
        # 1. Crear cuenta
        cuenta = Cuenta(
            id=str(uuid.uuid4()),
            titular="Maria Gonzalez",
            _saldo=2000.0
        )
        
        # 2. Configurar motor
        engine = Engine(ComisionEscalonada())
        engine.agregar_observador(ObservadorCorreo())
        engine.agregar_observador(ObservadorContabilidad())
        
        # 3. Crear método de pago con Factory
        tarjeta = MetodoPagoFactory.crear_tarjeta(
            numero="4111111111111111",
            titular="Maria Gonzalez",
            cvv="123",
            fecha_exp="12/26",
            saldo_disponible=3000.0
        )
        
        # 4. Procesar pago
        resultado = engine.procesar_pago(
            cuenta=cuenta,
            metodo_pago=tarjeta,
            monto=150.0,
            descripcion="Compra en tienda online"
        )
        
        # 5. Verificar resultados
        assert resultado is True
        assert cuenta.saldo == 1845.5  # 2000 - (150 + 4.5 comisión 3%)
        assert len(cuenta.transacciones) == 1
        assert cuenta.transacciones[0].monto == 154.5  # Monto + comisión
    
    def test_flujo_pago_con_suscripcion(self):
        """Probar flujo completo con suscripción."""
        # 1. Crear cuenta
        cuenta = Cuenta(
            id=str(uuid.uuid4()),
            titular="Carlos Ruiz",
            _saldo=3000.0
        )
        
        # 2. Crear suscripción
        suscripcion = Suscripcion(
            id=str(uuid.uuid4()),
            nombre="Netflix Premium",
            monto=99.0,
            periodicidad="mensual",
            fecha_inicio=datetime.now()
        )
        cuenta.agregar_suscripcion(suscripcion)
        
        # 3. Configurar motor
        engine = Engine(ComisionFija(3.0))
        engine.agregar_observador(ObservadorLogger())
        
        # 4. Crear método de pago
        wallet = MetodoPagoFactory.crear_wallet(
            email="carlos@email.com",
            saldo_disponible=1000.0
        )
        
        # 5. Procesar pago de suscripción
        resultado = engine.procesar_pago(
            cuenta=cuenta,
            metodo_pago=wallet,
            monto=suscripcion.monto,
            descripcion=f"Suscripción: {suscripcion.nombre}"
        )
        
        # 6. Verificar resultados
        assert resultado is True
        assert cuenta.saldo == 2898.0  # 3000 - (99 + 3)
        assert len(cuenta.transacciones) == 1
        assert suscripcion in cuenta.suscripciones
    
    def test_flujo_pago_con_cambio_estrategia(self):
        """Probar cambio de estrategia en tiempo de ejecución."""
        cuenta = Cuenta(
            id=str(uuid.uuid4()),
            titular="Ana Torres",
            _saldo=1000.0
        )
        
        engine = Engine()
        
        # Crear método de pago
        tarjeta = MetodoPagoFactory.crear_tarjeta(
            numero="4111111111111111",
            titular="Ana Torres",
            cvv="123",
            fecha_exp="12/26"
        )
        
        # Pago 1: Estrategia por defecto (2.5%)
        resultado1 = engine.procesar_pago(
            cuenta=cuenta,
            metodo_pago=tarjeta,
            monto=100.0,
            descripcion="Pago 1 - 2.5% comisión"
        )
        assert resultado1 is True
        saldo_despues_1 = cuenta.saldo
        
        # Resetear cuenta
        cuenta2 = Cuenta(
            id=str(uuid.uuid4()),
            titular="Ana Torres",
            _saldo=1000.0
        )
        
        # Pago 2: Cambiar a comisión fija
        engine.cambiar_estrategia(ComisionFija(10.0))
        resultado2 = engine.procesar_pago(
            cuenta=cuenta2,
            metodo_pago=tarjeta,
            monto=100.0,
            descripcion="Pago 2 - $10 comisión fija"
        )
        assert resultado2 is True
        saldo_despues_2 = cuenta2.saldo
        
        # Verificar que las comisiones son diferentes
        # Pago 1: 100 + 2.5% = 102.5 → saldo 897.5
        # Pago 2: 100 + 10 = 110 → saldo 890.0
        assert saldo_despues_1 != saldo_despues_2
        assert saldo_despues_1 == 897.5
        assert saldo_despues_2 == 890.0
    
    def test_flujo_pago_con_observadores_multiple(self):
        """Probar múltiples observadores reaccionando a eventos."""
        cuenta = Cuenta(
            id=str(uuid.uuid4()),
            titular="Luis Martinez",
            _saldo=1500.0
        )
        
        # Configurar gestor de eventos con múltiples observadores
        gestor = GestorEventos()
        observador_correo = ObservadorCorreo()
        observador_contabilidad = ObservadorContabilidad()
        observador_logger = ObservadorLogger()
        
        gestor.suscribir(observador_correo)
        gestor.suscribir(observador_contabilidad)
        gestor.suscribir(observador_logger)
        
        engine = Engine(gestor_eventos=gestor)
        
        # Crear método de pago
        transferencia = MetodoPagoFactory.crear_transferencia(
            banco="Banco Nacional",
            cuenta="1234567890",
            clabe="123456789012345678",
            saldo_disponible=5000.0
        )
        
        # Procesar pago
        resultado = engine.procesar_pago(
            cuenta=cuenta,
            metodo_pago=transferencia,
            monto=200.0,
            descripcion="Transferencia para proveedor"
        )
        
        # Verificar resultados
        assert resultado is True
        assert len(observador_contabilidad.eventos) == 1
        assert len(observador_logger.logs) == 1
        assert "aprobado" in observador_logger.logs[0]
    
    def test_flujo_pago_fallido_con_reversion(self):
        """Probar que un pago fallido revierte el retiro."""
        cuenta = Cuenta(
            id=str(uuid.uuid4()),
            titular="Pedro Diaz",
            _saldo=500.0
        )
        
        engine = Engine()
        
        tarjeta = MetodoPagoFactory.crear_tarjeta(
            numero="4111111111111111",
            titular="Pedro Diaz",
            cvv="123",
            fecha_exp="12/26",
            saldo_disponible=50.0  # Saldo insuficiente para el pago
        )
        
        saldo_inicial = cuenta.saldo
        
        resultado = engine.procesar_pago(
            cuenta=cuenta,
            metodo_pago=tarjeta,
            monto=100.0,
            descripcion="Pago que fallará"
        )
        
        # Verificar que el pago falló
        assert resultado is False
        
        # Verificar que el saldo fue restaurado (reversión exitosa)
        assert cuenta.saldo == saldo_inicial  # Saldo restaurado
        
        # ✅ CORREGIDO: Verificar que hay transacciones (retiro + reverso)
        # El sistema crea transacciones para mantener trazabilidad
        assert len(cuenta.transacciones) == 2  # Retiro + Reverso
        
        # Verificar que la primera transacción es un egreso (retiro)
        assert cuenta.transacciones[0].tipo == "egreso"
        assert cuenta.transacciones[0].monto == 102.5  # Monto + comisión
        
        # Verificar que la segunda transacción es un ingreso (reverso)
        assert cuenta.transacciones[1].tipo == "ingreso"
        assert cuenta.transacciones[1].monto == 102.5  # Reverso del mismo monto
    
    def test_flujo_pago_con_metodos_heterogeneos(self):
        """Probar flujo con diferentes métodos de pago."""
        cuenta = Cuenta(
            id=str(uuid.uuid4()),
            titular="Sofia Ramirez",
            _saldo=5000.0
        )
        
        engine = Engine(ComisionEscalonada())
        
        # Diferentes métodos de pago
        metodos = [
            MetodoPagoFactory.crear_tarjeta(
                "4111111111111111", "Sofia", "123", "12/26", 2000.0
            ),
            MetodoPagoFactory.crear_transferencia(
                "Banco", "123", "123456789012345678", 3000.0
            ),
            MetodoPagoFactory.crear_wallet(
                "sofia@email.com", 1000.0
            )
        ]
        
        montos = [100.0, 200.0, 50.0]
        descripciones = ["Pago 1", "Pago 2", "Pago 3"]
        
        # Procesar todos los pagos
        for metodo, monto, desc in zip(metodos, montos, descripciones):
            resultado = engine.procesar_pago(
                cuenta=cuenta,
                metodo_pago=metodo,
                monto=monto,
                descripcion=desc
            )
            assert resultado is True
        
        # Verificar que todos los pagos se procesaron
        assert len(cuenta.transacciones) == 3
        assert cuenta.saldo < 5000.0  # Se descontaron los pagos