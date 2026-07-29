#!/usr/bin/env python
"""Pruebas básicas del dominio para validar encapsulamiento."""

from datetime import datetime
import uuid

from orbitpay.domain import Cuenta, Transaccion, Suscripcion
from orbitpay.domain.cuenta import SaldoInsuficienteError, MontoInvalidoError


def test_cuenta_creacion():
    """Probar creación de cuenta."""
    cuenta = Cuenta("test-1", "Juan Perez", _saldo=1000.0)
    assert cuenta.id == "test-1"
    assert cuenta.titular == "Juan Perez"
    assert cuenta.saldo == 1000.0
    assert len(cuenta.transacciones) == 0
    print("✅ test_cuenta_creacion OK")


def test_cuenta_depositar():
    """Probar depósito en cuenta."""
    cuenta = Cuenta("test-2", "Maria Gomez", _saldo=500.0)
    transaccion = cuenta.depositar(200.0, "Depósito prueba")
    
    assert cuenta.saldo == 700.0
    assert transaccion.monto == 200.0
    assert transaccion.tipo == "ingreso"
    assert len(cuenta.transacciones) == 1
    print("✅ test_cuenta_depositar OK")


def test_cuenta_retirar():
    """Probar retiro de cuenta."""
    cuenta = Cuenta("test-3", "Carlos Ruiz", _saldo=500.0)
    transaccion = cuenta.retirar(300.0, "Retiro prueba")
    
    assert cuenta.saldo == 200.0
    assert transaccion.monto == 300.0
    assert transaccion.tipo == "egreso"
    assert len(cuenta.transacciones) == 1
    print("✅ test_cuenta_retirar OK")


def test_cuenta_saldo_insuficiente():
    """Probar error de saldo insuficiente."""
    cuenta = Cuenta("test-4", "Ana Torres", _saldo=100.0)
    
    try:
        cuenta.retirar(200.0)
        assert False, "Debería haber lanzado SaldoInsuficienteError"
    except SaldoInsuficienteError:
        assert cuenta.saldo == 100.0  # Saldo no modificado
        print("✅ test_cuenta_saldo_insuficiente OK")


def test_cuenta_monto_invalido():
    """Probar error de monto inválido."""
    cuenta = Cuenta("test-5", "Luis Martinez", _saldo=100.0)
    
    try:
        cuenta.depositar(-50.0)
        assert False, "Debería haber lanzado MontoInvalidoError"
    except MontoInvalidoError:
        assert cuenta.saldo == 100.0  # Saldo no modificado
        print("✅ test_cuenta_monto_invalido OK")


def test_transaccion_inmutable():
    """Probar que Transacción es inmutable."""
    transaccion = Transaccion(
        id="test-1",
        monto=100.0,
        tipo="ingreso",
        fecha=datetime.now(),
        descripcion="Test",
        estado="completada"
    )
    
    # Verificar que no se puede modificar
    try:
        transaccion.monto = 200.0
        assert False, "Transacción debería ser inmutable"
    except AttributeError:
        print("✅ test_transaccion_inmutable OK")


def test_transaccion_validacion():
    """Probar validación de Transacción."""
    try:
        Transaccion(
            id="test-1",
            monto=-100.0,  # Monto negativo
            tipo="ingreso",
            fecha=datetime.now(),
            descripcion="Test",
            estado="completada"
        )
        assert False, "Debería haber lanzado ValueError"
    except ValueError:
        print("✅ test_transaccion_validacion OK")


def test_suscripcion_renovar():
    """Probar renovación de suscripción."""
    suscripcion = Suscripcion(
        id="sub-1",
        nombre="Netflix",
        monto=99.0,
        periodicidad="mensual",
        fecha_inicio=datetime.now()
    )
    
    fecha_anterior = suscripcion.fecha_inicio
    suscripcion.renovar(3)
    
    assert suscripcion.activa
    assert suscripcion.fecha_fin is not None
    assert suscripcion.fecha_fin > fecha_anterior
    print("✅ test_suscripcion_renovar OK")


def test_suscripcion_cancelar():
    """Probar cancelación de suscripción."""
    suscripcion = Suscripcion(
        id="sub-2",
        nombre="Spotify",
        monto=89.0,
        periodicidad="mensual",
        fecha_inicio=datetime.now()
    )
    
    suscripcion.cancelar()
    assert not suscripcion.activa
    assert suscripcion.fecha_fin is not None
    print("✅ test_suscripcion_cancelar OK")


def test_suscripcion_proximo_pago():
    """Probar cálculo de próximo pago."""
    fecha_inicio = datetime(2026, 1, 1)
    suscripcion = Suscripcion(
        id="sub-3",
        nombre="Amazon Prime",
        monto=150.0,
        periodicidad="mensual",
        fecha_inicio=fecha_inicio
    )
    
    proximo = suscripcion.calcular_proximo_pago()
    assert proximo > fecha_inicio
    print("✅ test_suscripcion_proximo_pago OK")


def test_metodos_dunder():
    """Probar métodos dunder."""
    # __repr__
    cuenta = Cuenta("test-6", "Pedro Diaz", _saldo=500.0)
    repr_str = repr(cuenta)
    assert "Cuenta" in repr_str
    assert "Pedro Diaz" in repr_str
    
    # __eq__
    t1 = Transaccion("eq-1", 100.0, "ingreso", datetime.now(), "Test", "completada")
    t2 = Transaccion("eq-1", 200.0, "ingreso", datetime.now(), "Test2", "completada")
    assert t1 == t2
    assert t1 != "otra_cosa"
    
    # __lt__
    t3 = Transaccion("lt-1", 50.0, "ingreso", datetime.now(), "Test", "completada")
    t4 = Transaccion("lt-2", 150.0, "ingreso", datetime.now(), "Test", "completada")
    assert t3 < t4
    assert not (t4 < t3)
    
    print("✅ test_metodos_dunder OK")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 EJECUTANDO PRUEBAS DEL DOMINIO")
    print("=" * 60)
    
    test_cuenta_creacion()
    test_cuenta_depositar()
    test_cuenta_retirar()
    test_cuenta_saldo_insuficiente()
    test_cuenta_monto_invalido()
    test_transaccion_inmutable()
    test_transaccion_validacion()
    test_suscripcion_renovar()
    test_suscripcion_cancelar()
    test_suscripcion_proximo_pago()
    test_metodos_dunder()
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS PASARON")
    print("=" * 60)