"""Pruebas unitarias para patrones de diseño."""

import pytest

from orbitpay.patterns.factory import MetodoPagoFactory
from orbitpay.patterns.strategy import ComisionFija, ComisionPorcentual, ComisionEscalonada
from orbitpay.patterns.observer import (
    EventoPago,
    ObservadorCorreo,
    ObservadorContabilidad,
    ObservadorLogger,
    GestorEventos,
)


class TestFactory:
    """Pruebas para el Factory Pattern."""
    
    def test_crear_tarjeta(self):
        """Probar creación de tarjeta."""
        tarjeta = MetodoPagoFactory.crear_tarjeta(
            numero="4111111111111111",
            titular="Juan",
            cvv="123",
            fecha_exp="12/26"
        )
        
        assert tarjeta.__class__.__name__ == "Tarjeta"
        assert tarjeta.validar() is True
    
    def test_crear_transferencia(self):
        """Probar creación de transferencia."""
        transferencia = MetodoPagoFactory.crear_transferencia(
            banco="Banco",
            cuenta="123",
            clabe="123456789012345678"
        )
        
        assert transferencia.__class__.__name__ == "Transferencia"
        assert transferencia.validar() is True
    
    def test_crear_wallet(self):
        """Probar creación de wallet."""
        wallet = MetodoPagoFactory.crear_wallet("user@example.com")
        
        assert wallet.__class__.__name__ == "Wallet"
        assert wallet.validar() is True
    
    def test_crear_por_tipo_tarjeta(self):
        """Probar creación por tipo: tarjeta."""
        datos = {
            "numero": "4111111111111111",
            "titular": "Juan",
            "cvv": "123",
            "fecha_exp": "12/26"
        }
        metodo = MetodoPagoFactory.crear_por_tipo("tarjeta", datos)
        
        assert metodo is not None
        assert metodo.__class__.__name__ == "Tarjeta"
    
    def test_crear_por_tipo_transferencia(self):
        """Probar creación por tipo: transferencia."""
        datos = {
            "banco": "Banco",
            "cuenta": "123",
            "clabe": "123456789012345678"
        }
        metodo = MetodoPagoFactory.crear_por_tipo("transferencia", datos)
        
        assert metodo is not None
        assert metodo.__class__.__name__ == "Transferencia"
    
    def test_crear_por_tipo_wallet(self):
        """Probar creación por tipo: wallet."""
        datos = {"email": "user@example.com"}
        metodo = MetodoPagoFactory.crear_por_tipo("wallet", datos)
        
        assert metodo is not None
        assert metodo.__class__.__name__ == "Wallet"
    
    def test_crear_por_tipo_invalido(self):
        """Probar creación por tipo inválido."""
        metodo = MetodoPagoFactory.crear_por_tipo("invalido", {})
        assert metodo is None
    
    def test_crear_por_tipo_faltan_datos(self):
        """Probar creación con datos faltantes."""
        with pytest.raises(ValueError, match="Falta campo requerido"):
            MetodoPagoFactory.crear_por_tipo("tarjeta", {})


class TestStrategy:
    """Pruebas para el Strategy Pattern."""
    
    def test_comision_fija(self):
        """Probar comisión fija."""
        strategy = ComisionFija(5.0)
        
        assert strategy.calcular(100.0) == 5.0
        assert strategy.calcular(200.0) == 5.0
        assert strategy.calcular(0) == 0.0
        assert strategy.calcular(-50.0) == 0.0
    
    def test_comision_porcentual(self):
        """Probar comisión porcentual."""
        strategy = ComisionPorcentual(2.5)
        
        assert strategy.calcular(100.0) == 2.5
        assert strategy.calcular(200.0) == 5.0
        assert strategy.calcular(0) == 0.0
    
    def test_comision_escalonada(self):
        """Probar comisión escalonada."""
        strategy = ComisionEscalonada()
        
        # Monto <= 100: 5%
        assert strategy.calcular(50.0) == 2.5  # 50 * 0.05
        assert strategy.calcular(100.0) == 5.0  # 100 * 0.05
        
        # Monto <= 500: 3%
        assert strategy.calcular(200.0) == 6.0  # 200 * 0.03
        assert strategy.calcular(500.0) == 15.0  # 500 * 0.03
        
        # Monto > 500: 1.5%
        assert strategy.calcular(600.0) == 9.0  # 600 * 0.015
        assert strategy.calcular(1000.0) == 15.0  # 1000 * 0.015


class TestObserver:
    """Pruebas para el Observer Pattern."""
    
    def test_gestor_eventos(self):
        """Probar gestor de eventos."""
        gestor = GestorEventos()
        
        observador1 = ObservadorCorreo()
        observador2 = ObservadorContabilidad()
        
        gestor.suscribir(observador1)
        gestor.suscribir(observador2)
        
        evento = EventoPago(
            tipo="aprobado",
            datos={"monto": 100.0, "email": "user@example.com"}
        )
        
        # No debería lanzar errores
        gestor.notificar(evento)
    
    def test_suscribir_desuscribir(self):
        """Probar suscripción y desuscripción."""
        gestor = GestorEventos()
        observador = ObservadorLogger()
        
        gestor.suscribir(observador)
        assert len(gestor._observadores) == 1
        
        gestor.desuscribir(observador)
        assert len(gestor._observadores) == 0
    
    def test_observador_contabilidad(self):
        """Probar observador de contabilidad."""
        observador = ObservadorContabilidad()
        
        evento1 = EventoPago("aprobado", {"monto": 100.0})
        evento2 = EventoPago("rechazado", {"monto": 200.0})
        
        observador.actualizar(evento1)
        observador.actualizar(evento2)
        
        assert len(observador.eventos) == 2
        assert observador.eventos[0].tipo == "aprobado"
        assert observador.eventos[1].tipo == "rechazado"
    
    def test_observador_logger(self):
        """Probar observador logger."""
        observador = ObservadorLogger()
        
        evento = EventoPago("aprobado", {"monto": 100.0, "metodo": "Tarjeta"})
        observador.actualizar(evento)
        
        assert len(observador.logs) == 1
        assert "aprobado" in observador.logs[0]
        assert "100.00" in observador.logs[0]