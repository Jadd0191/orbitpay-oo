"""Módulo con la clase Transferencia."""

from orbitpay.payments.metodo_pago import MetodoPago


class Transferencia(MetodoPago):
    """Método de pago con transferencia bancaria.
    
    Atributos:
        banco: Nombre del banco emisor
        cuenta: Número de cuenta
        clabe: CLABE interbancaria (18 dígitos)
        saldo_disponible: Saldo disponible en la cuenta
    """
    
    def __init__(
        self,
        banco: str,
        cuenta: str,
        clabe: str,
        saldo_disponible: float = 10000.0
    ):
        self.banco = banco
        self.cuenta = cuenta
        self.clabe = clabe
        self.saldo_disponible = saldo_disponible
    
    def validar(self) -> bool:
        """Validar que la transferencia es operable.
        
        Verifica:
        - CLABE tiene 18 dígitos
        - Cuenta no está vacía
        - Banco no está vacío
        """
        # Validar CLABE (18 dígitos)
        if not self.clabe.isdigit() or len(self.clabe) != 18:
            return False
        
        # Validar cuenta no vacía
        if not self.cuenta or not self.cuenta.strip():
            return False
        
        # Validar banco no vacío
        if not self.banco or not self.banco.strip():
            return False
        
        return True
    
    def procesar(self, monto: float) -> bool:
        """Procesar el pago con transferencia.
        
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
        return f"banco='{self.banco}', cuenta='***{self.cuenta[-4:]}'"