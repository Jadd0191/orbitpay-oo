"""Pruebas unitarias para el Engine."""

import pytest
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
    Engine
)
from orbitpay.domain.cuenta import SaldoInsuficienteError


class TestEngine:
    """Pruebas para el Engine."""
    
    def setup_method(self):
        """Configuración antes de cada prueba."""
        self.cuenta = Cuenta(
            id=str(uuid.uuid4()),
            titular="Juan Perez",
            _saldo=1000.0
        )
        self.tarjeta = MetodoPagoFactory.crear_tarjeta(
            numero="4111111111111111",
            titular="Juan Perez",
            cvv="123",
            fecha_exp="12/26",
            saldo_disponible=2000.0
        )
        self.engine = Engine()
    
    def test_procesar_pago_exitoso(self):
        """Probar pago exitoso."""
        resultado = self.engine.procesar_pago(
            cuenta=self.cuenta,
            metodo_pago=self.tarjeta,
            monto=100.0,
            descripcion="Prueba"
        )
        
        assert resultado is True
        assert self.cuenta.saldo == 897.5  # 1000 - (100 + 2.5% comisión)
        assert len(self.cuenta.transacciones) == 1
    
    def test_procesar_pago_saldo_insuficiente(self):
        """Probar pago con saldo insuficiente."""
        resultado = self.engine.procesar_pago(
            cuenta=self.cuenta,
            metodo_pago=self.tarjeta,
            monto=2000.0,
            descripcion="Prueba"
        )
        
        assert resultado is False
        assert self.cuenta.saldo == 1000.0  # Saldo no modificado
        assert len(self.cuenta.transacciones) == 0
    
    def test_procesar_pago_metodo_invalido(self):
        """Probar pago con método inválido."""
        tarjeta_invalida = MetodoPagoFactory.crear_tarjeta(
            numero="1234",  # Inválido
            titular="Juan",
            cvv="12",  # Inválido
            fecha_exp="12/26"
        )
        
        resultado = self.engine.procesar_pago(
            cuenta=self.cuenta,
            metodo_pago=tarjeta_invalida,
            monto=100.0,
            descripcion="Prueba"
        )
        
        assert resultado is False
        assert self.cuenta.saldo == 1000.0
        assert len(self.cuenta.transacciones) == 0
    
    def test_procesar_pago_monto_negativo(self):
        """Probar pago con monto negativo."""
        with pytest.raises(ValueError, match="monto debe ser positivo"):
            self.engine.procesar_pago(
                cuenta=self.cuenta,
                metodo_pago=self.tarjeta,
                monto=-100.0,
                descripcion="Prueba"
            )
    
    def test_cambiar_estrategia(self):
        """Probar cambio de estrategia de comisión."""
        # Estrategia inicial: 2.5%
        self.engine.procesar_pago(
            cuenta=self.cuenta,
            metodo_pago=self.tarjeta,
            monto=100.0,
            descripcion="Pago 1"
        )
        saldo_despues_1 = self.cuenta.saldo
        
        # Resetear cuenta
        self.cuenta = Cuenta(
            id=str(uuid.uuid4()),
            titular="Juan Perez",
            _saldo=1000.0
        )
        
        # Cambiar a comisión fija
        self.engine.cambiar_estrategia(ComisionFija(10.0))
        
        self.engine.procesar_pago(
            cuenta=self.cuenta,
            metodo_pago=self.tarjeta,
            monto=100.0,
            descripcion="Pago 2"
        )
        
        # Comisión fija es más alta que 2.5% en este caso
        assert self.cuenta.saldo == 890.0  # 1000 - (100 + 10)
    
    def test_agregar_observadores(self):
        """Probar agregar observadores."""
        gestor = self.engine.gestor_eventos
        
        # Inicialmente no hay observadores
        assert len(gestor._observadores) == 0
        
        # Agregar observadores
        self.engine.agregar_observador(ObservadorCorreo())
        self.engine.agregar_observador(ObservadorContabilidad())
        
        assert len(gestor._observadores) == 2
        
        # Procesar pago (no debería lanzar errores)
        self.engine.procesar_pago(
            cuenta=self.cuenta,
            metodo_pago=self.tarjeta,
            monto=100.0,
            descripcion="Prueba con observadores"
        )
    
    def test_strategy_injection(self):
        """Probar inyección de estrategia en constructor."""
        engine = Engine(ComisionFija(5.0))
        assert engine.strategy.__class__.__name__ == "ComisionFija"
        
        engine = Engine(ComisionPorcentual(1.0))
        assert engine.strategy.__class__.__name__ == "ComisionPorcentual"
        
        engine = Engine(ComisionEscalonada())
        assert engine.strategy.__class__.__name__ == "ComisionEscalonada"
    
    def test_pago_con_diferentes_metodos(self):
        """Probar pago con diferentes métodos de pago."""
        # Tarjeta
        resultado1 = self.engine.procesar_pago(
            cuenta=self.cuenta,
            metodo_pago=self.tarjeta,
            monto=100.0,
            descripcion="Pago con Tarjeta"
        )
        assert resultado1 is True
        
        # Resetear cuenta (crear nueva)
        cuenta2 = Cuenta(
            id=str(uuid.uuid4()),
            titular="Juan Perez",
            _saldo=1000.0
        )
        
        # Transferencia
        transferencia = MetodoPagoFactory.crear_transferencia(
            banco="Banco",
            cuenta="123",
            clabe="123456789012345678",
            saldo_disponible=2000.0
        )
        resultado2 = self.engine.procesar_pago(
            cuenta=cuenta2,
            metodo_pago=transferencia,
            monto=100.0,
            descripcion="Pago con Transferencia"
        )
        assert resultado2 is True
        
        # Wallet
        cuenta3 = Cuenta(
            id=str(uuid.uuid4()),
            titular="Juan Perez",
            _saldo=1000.0
        )
        wallet = MetodoPagoFactory.crear_wallet(
            email="user@example.com",
            saldo_disponible=500.0
        )
        resultado3 = self.engine.procesar_pago(
            cuenta=cuenta3,
            metodo_pago=wallet,
            monto=100.0,
            descripcion="Pago con Wallet"
        )
        assert resultado3 is True