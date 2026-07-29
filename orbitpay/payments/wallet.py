"""Módulo con la clase Wallet."""

import re
from orbitpay.payments.metodo_pago import MetodoPago


class Wallet(MetodoPago):
    """Método de pago con billetera digital.
    
    Atributos:
        email: Email asociado a la wallet
        saldo_disponible: Saldo disponible en la wallet
    """
    
    def __init__(self, email: str, saldo_disponible: float = 5000.0):
        self.email = email
        self.saldo_disponible = saldo_disponible
    
    def validar(self) -> bool:
        """Validar que la wallet es operable.
        
        Verifica:
        - Email tiene formato válido (simple)
        """
        # Validar email (regex simple)
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, self.email))
    
    def procesar(self, monto: float) -> bool:
        """Procesar el pago con wallet.
        
        Args:
            monto: Cantidad a cobrar
            
        Returns:
            True si el pago fue exitoso
        """
        if monto <= 0:
            raise ValueError(f"El monto debe ser positivo: {monto}")
        
        # Validar primero
        if not self.validar():
            return False
        
        # Validar saldo disponible
        if monto > self.saldo_disponible:
            return False
        
        # Simular procesamiento
        self.saldo_disponible -= monto
        return True
    
    def _repr_params(self) -> str:
        """Parámetros para __repr__."""
        return f"email='{self.email}'"