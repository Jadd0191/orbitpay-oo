"""Pruebas unitarias para la clase Cuenta."""

import pytest
import uuid
from datetime import datetime

from orbitpay.domain import Cuenta, Transaccion, Suscripcion
from orbitpay.domain.cuenta import SaldoInsuficienteError, MontoInvalidoError


class TestCuenta:
    """Pruebas para la clase Cuenta."""
    
    def test_creacion_cuenta_valida(self):
        """Probar creación de cuenta válida."""
        cuenta = Cuenta("test-1", "Juan Perez", _saldo=1000.0)
        assert cuenta.id == "test-1"
        assert cuenta.titular == "Juan Perez"
        assert cuenta.saldo == 1000.0
        assert len(cuenta.transacciones) == 0
        assert len(cuenta.suscripciones) == 0
    
    def test_creacion_cuenta_saldo_negativo(self):
        """Probar que no se puede crear cuenta con saldo negativo."""
        with pytest.raises(ValueError, match="saldo inicial no puede ser negativo"):
            Cuenta("test-2", "Maria", _saldo=-100.0)
    
    def test_creacion_cuenta_titular_vacio(self):
        """Probar que no se puede crear cuenta con titular vacío."""
        with pytest.raises(ValueError, match="titular no puede estar vacío"):
            Cuenta("test-3", "")
    
    def test_depositar_valido(self):
        """Probar depósito válido."""
        cuenta = Cuenta("test-4", "Carlos", _saldo=500.0)
        transaccion = cuenta.depositar(200.0, "Depósito prueba")
        
        assert cuenta.saldo == 700.0
        assert transaccion.monto == 200.0
        assert transaccion.tipo == "ingreso"
        assert len(cuenta.transacciones) == 1
    
    def test_depositar_monto_invalido(self):
        """Probar depósito con monto inválido."""
        cuenta = Cuenta("test-5", "Ana", _saldo=500.0)
        
        with pytest.raises(MontoInvalidoError, match="Monto debe ser positivo"):
            cuenta.depositar(0)
        
        with pytest.raises(MontoInvalidoError, match="Monto debe ser positivo"):
            cuenta.depositar(-50.0)
        
        assert cuenta.saldo == 500.0  # Saldo no modificado
    
    def test_retirar_valido(self):
        """Probar retiro válido."""
        cuenta = Cuenta("test-6", "Luis", _saldo=500.0)
        transaccion = cuenta.retirar(300.0, "Retiro prueba")
        
        assert cuenta.saldo == 200.0
        assert transaccion.monto == 300.0
        assert transaccion.tipo == "egreso"
        assert len(cuenta.transacciones) == 1
    
    def test_retirar_saldo_insuficiente(self):
        """Probar retiro con saldo insuficiente."""
        cuenta = Cuenta("test-7", "Sofia", _saldo=100.0)
        
        with pytest.raises(SaldoInsuficienteError, match="Saldo insuficiente"):
            cuenta.retirar(200.0)
        
        assert cuenta.saldo == 100.0  # Saldo no modificado
        assert len(cuenta.transacciones) == 0
    
    def test_retirar_monto_invalido(self):
        """Probar retiro con monto inválido."""
        cuenta = Cuenta("test-8", "Pedro", _saldo=500.0)
        
        with pytest.raises(MontoInvalidoError, match="Monto debe ser positivo"):
            cuenta.retirar(0)
        
        with pytest.raises(MontoInvalidoError, match="Monto debe ser positivo"):
            cuenta.retirar(-50.0)
        
        assert cuenta.saldo == 500.0  # Saldo no modificado
    
    def test_agregar_suscripcion(self):
        """Probar agregar suscripción a cuenta."""
        cuenta = Cuenta("test-9", "Lucia", _saldo=1000.0)
        suscripcion = Suscripcion(
            id="sub-1",
            nombre="Netflix",
            monto=99.0,
            periodicidad="mensual",
            fecha_inicio=datetime.now()
        )
        
        cuenta.agregar_suscripcion(suscripcion)
        assert len(cuenta.suscripciones) == 1
        assert cuenta.suscripciones[0] == suscripcion
    
    def test_obtener_suscripciones_activas(self):
        """Probar obtener solo suscripciones activas."""
        cuenta = Cuenta("test-10", "Mario", _saldo=1000.0)
        
        suscripcion1 = Suscripcion(
            id="sub-1",
            nombre="Netflix",
            monto=99.0,
            periodicidad="mensual",
            fecha_inicio=datetime.now(),
            activa=True
        )
        suscripcion2 = Suscripcion(
            id="sub-2",
            nombre="Spotify",
            monto=89.0,
            periodicidad="mensual",
            fecha_inicio=datetime.now(),
            activa=False
        )
        
        cuenta.agregar_suscripcion(suscripcion1)
        cuenta.agregar_suscripcion(suscripcion2)
        
        activas = cuenta.obtener_suscripciones_activas()
        assert len(activas) == 1
        assert activas[0].nombre == "Netflix"
    
    def test_obtener_historial(self):
        """Probar obtención de historial."""
        cuenta = Cuenta("test-11", "Elena", _saldo=1000.0)
        
        cuenta.depositar(200.0, "Depósito 1")
        cuenta.retirar(100.0, "Retiro 1")
        cuenta.depositar(50.0, "Depósito 2")
        
        historial = cuenta.obtener_historial()
        assert len(historial) == 3
        assert isinstance(historial, list)
    
    def test_repr(self):
        """Probar representación de cuenta."""
        cuenta = Cuenta("test-12", "Rosa", _saldo=1000.0)
        repr_str = repr(cuenta)
        
        assert "Cuenta" in repr_str
        assert "Rosa" in repr_str
        assert "1000.00" in repr_str
    
    def test_eq(self):
        """Probar comparación de cuentas."""
        cuenta1 = Cuenta("test-13", "Ana", _saldo=1000.0)
        cuenta2 = Cuenta("test-13", "Ana", _saldo=2000.0)  # Mismo ID
        cuenta3 = Cuenta("test-14", "Carlos", _saldo=1000.0)
        
        assert cuenta1 == cuenta2  # Mismo ID
        assert cuenta1 != cuenta3  # Diferente ID
        assert cuenta1 != "otra_cosa"