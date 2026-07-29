#!/usr/bin/env python
"""Pruebas unitarias para métodos de pago."""

from orbitpay.payments import Tarjeta, Transferencia, Wallet
from orbitpay.payments.metodo_pago import MetodoPago


def test_tarjeta_valida():
    """Probar tarjeta válida."""
    tarjeta = Tarjeta(
        numero="4111111111111111",
        titular="Juan Perez",
        cvv="123",
        fecha_exp="12/26",
        saldo_disponible=1000.0
    )
    assert tarjeta.validar() is True
    assert tarjeta.procesar(100.0) is True
    assert tarjeta.saldo_disponible == 900.0
    print("✅ test_tarjeta_valida OK")


def test_tarjeta_invalida():
    """Probar tarjeta inválida."""
    # Número incorrecto
    tarjeta1 = Tarjeta("1234", "Juan", "123", "12/26")
    assert tarjeta1.validar() is False
    
    # CVV incorrecto
    tarjeta2 = Tarjeta("4111111111111111", "Juan", "12", "12/26")
    assert tarjeta2.validar() is False
    
    # Fecha expirada
    tarjeta3 = Tarjeta("4111111111111111", "Juan", "123", "12/20")
    assert tarjeta3.validar() is False
    
    print("✅ test_tarjeta_invalida OK")


def test_transferencia_valida():
    """Probar transferencia válida."""
    transferencia = Transferencia(
        banco="Banco Ejemplo",
        cuenta="1234567890",
        clabe="123456789012345678",
        saldo_disponible=5000.0
    )
    assert transferencia.validar() is True
    assert transferencia.procesar(200.0) is True
    assert transferencia.saldo_disponible == 4800.0
    print("✅ test_transferencia_valida OK")


def test_transferencia_invalida():
    """Probar transferencia inválida."""
    # CLABE incorrecta
    t1 = Transferencia("Banco", "123", "1234")
    assert t1.validar() is False
    
    # Banco vacío
    t2 = Transferencia("", "1234567890", "123456789012345678")
    assert t2.validar() is False
    
    print("✅ test_transferencia_invalida OK")


def test_wallet_valida():
    """Probar wallet válida."""
    wallet = Wallet(
        email="usuario@ejemplo.com",
        saldo_disponible=1000.0
    )
    assert wallet.validar() is True
    assert wallet.procesar(50.0) is True
    assert wallet.saldo_disponible == 950.0
    print("✅ test_wallet_valida OK")


def test_wallet_invalida():
    """Probar wallet inválida."""
    # Email inválido
    w1 = Wallet("usuario")
    assert w1.validar() is False
    
    w2 = Wallet("usuario@")
    assert w2.validar() is False
    
    print("✅ test_wallet_invalida OK")


def test_polimorfismo():
    """Probar que todos los métodos son MetodoPago."""
    metodos = [
        Tarjeta("4111111111111111", "Juan", "123", "12/26"),
        Transferencia("Banco", "123", "123456789012345678"),
        Wallet("user@example.com"),
    ]
    
    for metodo in metodos:
        assert isinstance(metodo, MetodoPago)
        # Todos tienen los métodos requeridos
        assert hasattr(metodo, 'procesar')
        assert hasattr(metodo, 'validar')
        assert callable(metodo.procesar)
        assert callable(metodo.validar)
    
    print("✅ test_polimorfismo OK")


def test_lsp():
    """Probar Liskov Substitution Principle."""
    def usar_metodo(metodo: MetodoPago, monto: float) -> bool:
        """Función que usa cualquier MetodoPago."""
        if not metodo.validar():
            return False
        return metodo.procesar(monto)
    
    # Todos los subtipos deben funcionar igual
    assert usar_metodo(
        Tarjeta("4111111111111111", "Juan", "123", "12/26", 1000.0),
        100.0
    ) is True
    
    assert usar_metodo(
        Transferencia("Banco", "123", "123456789012345678", 1000.0),
        100.0
    ) is True
    
    assert usar_metodo(
        Wallet("user@example.com", 1000.0),
        100.0
    ) is True
    
    print("✅ test_lsp OK")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 EJECUTANDO PRUEBAS DE MÉTODOS DE PAGO")
    print("=" * 60)
    
    test_tarjeta_valida()
    test_tarjeta_invalida()
    test_transferencia_valida()
    test_transferencia_invalida()
    test_wallet_valida()
    test_wallet_invalida()
    test_polimorfismo()
    test_lsp()
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS PASARON")
    print("=" * 60)