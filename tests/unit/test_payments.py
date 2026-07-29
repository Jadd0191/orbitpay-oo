"""Pruebas unitarias para métodos de pago."""

import pytest

from orbitpay.payments import Tarjeta, Transferencia, Wallet, MetodoPago


class TestTarjeta:
    """Pruebas para la clase Tarjeta."""
    
    def test_tarjeta_valida(self):
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
    
    def test_tarjeta_numero_invalido(self):
        """Probar tarjeta con número inválido."""
        tarjeta = Tarjeta("1234", "Juan", "123", "12/26")
        assert tarjeta.validar() is False
    
    def test_tarjeta_cvv_invalido(self):
        """Probar tarjeta con CVV inválido."""
        tarjeta = Tarjeta("4111111111111111", "Juan", "12", "12/26")
        assert tarjeta.validar() is False
    
    def test_tarjeta_fecha_expirada(self):
        """Probar tarjeta con fecha expirada."""
        tarjeta = Tarjeta("4111111111111111", "Juan", "123", "12/20")
        assert tarjeta.validar() is False
    
    def test_tarjeta_saldo_insuficiente(self):
        """Probar tarjeta con saldo insuficiente."""
        tarjeta = Tarjeta(
            "4111111111111111",
            "Juan",
            "123",
            "12/26",
            saldo_disponible=100.0
        )
        
        assert tarjeta.validar() is True
        assert tarjeta.procesar(200.0) is False
        assert tarjeta.saldo_disponible == 100.0  # No modificado
    
    def test_tarjeta_monto_negativo(self):
        """Probar tarjeta con monto negativo."""
        tarjeta = Tarjeta("4111111111111111", "Juan", "123", "12/26")
        
        with pytest.raises(ValueError, match="monto debe ser positivo"):
            tarjeta.procesar(-50.0)
    
    def test_tarjeta_repr(self):
        """Probar representación de tarjeta."""
        tarjeta = Tarjeta("4111111111111111", "Juan Perez", "123", "12/26")
        repr_str = repr(tarjeta)
        
        assert "Tarjeta" in repr_str
        assert "1111" in repr_str  # Últimos 4 dígitos
        assert "Juan Perez" in repr_str


class TestTransferencia:
    """Pruebas para la clase Transferencia."""
    
    def test_transferencia_valida(self):
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
    
    def test_transferencia_clabe_invalida(self):
        """Probar transferencia con CLABE inválida."""
        t1 = Transferencia("Banco", "123", "1234")
        assert t1.validar() is False
    
    def test_transferencia_banco_vacio(self):
        """Probar transferencia con banco vacío."""
        t2 = Transferencia("", "1234567890", "123456789012345678")
        assert t2.validar() is False
    
    def test_transferencia_cuenta_vacia(self):
        """Probar transferencia con cuenta vacía."""
        t3 = Transferencia("Banco", "", "123456789012345678")
        assert t3.validar() is False
    
    def test_transferencia_saldo_insuficiente(self):
        """Probar transferencia con saldo insuficiente."""
        transferencia = Transferencia(
            "Banco",
            "1234567890",
            "123456789012345678",
            saldo_disponible=100.0
        )
        
        assert transferencia.validar() is True
        assert transferencia.procesar(200.0) is False
        assert transferencia.saldo_disponible == 100.0
    
    def test_transferencia_repr(self):
        """Probar representación de transferencia."""
        transferencia = Transferencia("Banco Ejemplo", "1234567890", "123456789012345678")
        repr_str = repr(transferencia)
        
        assert "Transferencia" in repr_str
        assert "Banco Ejemplo" in repr_str


class TestWallet:
    """Pruebas para la clase Wallet."""
    
    def test_wallet_valida(self):
        """Probar wallet válida."""
        wallet = Wallet("usuario@ejemplo.com", saldo_disponible=1000.0)
        
        assert wallet.validar() is True
        assert wallet.procesar(50.0) is True
        assert wallet.saldo_disponible == 950.0
    
    def test_wallet_email_invalido(self):
        """Probar wallet con email inválido."""
        w1 = Wallet("usuario")
        assert w1.validar() is False
        
        w2 = Wallet("usuario@")
        assert w2.validar() is False
        
        w3 = Wallet("@ejemplo.com")
        assert w3.validar() is False
    
    def test_wallet_saldo_insuficiente(self):
        """Probar wallet con saldo insuficiente."""
        wallet = Wallet("user@example.com", saldo_disponible=100.0)
        
        assert wallet.validar() is True
        assert wallet.procesar(200.0) is False
        assert wallet.saldo_disponible == 100.0
    
    def test_wallet_repr(self):
        """Probar representación de wallet."""
        wallet = Wallet("usuario@ejemplo.com")
        repr_str = repr(wallet)
        
        assert "Wallet" in repr_str
        assert "usuario@ejemplo.com" in repr_str


class TestPolimorfismo:
    """Pruebas de polimorfismo entre métodos de pago."""
    
    def test_todos_son_metodo_pago(self):
        """Probar que todos los métodos implementan MetodoPago."""
        metodos = [
            Tarjeta("4111111111111111", "Juan", "123", "12/26"),
            Transferencia("Banco", "123", "123456789012345678"),
            Wallet("user@example.com"),
        ]
        
        for metodo in metodos:
            assert isinstance(metodo, MetodoPago)
            assert hasattr(metodo, 'procesar')
            assert hasattr(metodo, 'validar')
            assert callable(metodo.procesar)
            assert callable(metodo.validar)
    
    def test_liskov_substitution(self):
        """Probar Liskov Substitution Principle."""
        def usar_metodo(metodo: MetodoPago, monto: float) -> bool:
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