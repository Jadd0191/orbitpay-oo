"""Módulo con la clase Tarjeta."""

from datetime import datetime
from orbitpay.payments.metodo_pago import MetodoPago


class Tarjeta(MetodoPago):
    """Método de pago con tarjeta de crédito/débito.
    
    Atributos:
        numero: Número de la tarjeta (16 dígitos)
        titular: Nombre del titular
        cvv: Código de seguridad (3 dígitos)
        fecha_exp: Fecha de expiración (formato "MM/YY")
        saldo_disponible: Límite o saldo disponible
    """
    
    def __init__(
        self,
        numero: str,
        titular: str,
        cvv: str,
        fecha_exp: str,
        saldo_disponible: float = 10000.0
    ):
        self.numero = numero
        self.titular = titular
        self.cvv = cvv
        self.fecha_exp = fecha_exp
        self.saldo_disponible = saldo_disponible
    
    def validar(self) -> bool:
        """Validar que la tarjeta es operable.
        
        Verifica:
        - Número tiene 16 dígitos
        - CVV tiene 3 dígitos
        - Fecha de expiración es válida (no expirada)
        """
        # Validar número (16 dígitos)
        if not self.numero.isdigit() or len(self.numero) != 16:
            return False
        
        # Validar CVV (3 dígitos)
        if not self.cvv.isdigit() or len(self.cvv) != 3:
            return False
        
        # Validar fecha de expiración
        try:
            mes, anio = self.fecha_exp.split('/')
            mes = int(mes)
            anio = int(anio) + 2000  # Convertir "25" a 2025
            
            # Validar mes (1-12)
            if mes < 1 or mes > 12:
                return False
            
            # Validar que no esté expirada
            fecha_actual = datetime.now()
            if anio < fecha_actual.year:
                return False
            if anio == fecha_actual.year and mes < fecha_actual.month:
                return False
            
            return True
        except (ValueError, IndexError):
            return False
    
    def procesar(self, monto: float) -> bool:
        """Procesar el pago con tarjeta.
        
        Args:
            monto: Cantidad a cobrar
            
        Returns:
            True si el pago fue exitoso
        """
        if monto <= 0:
            raise ValueError(f"El monto debe ser positivo: {monto}")
        
        # Validar tarjeta primero
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
        return f"numero='***{self.numero[-4:]}', titular='{self.titular}'"