"""Módulo con la clase abstracta MetodoPago."""

from abc import ABC, abstractmethod
from typing import Optional


class MetodoPago(ABC):
    """Clase abstracta que define el contrato para todos los métodos de pago.
    
    Todos los métodos de pago deben implementar:
        - procesar(): Ejecutar el pago
        - validar(): Verificar que el método es operable
    """
    
    @abstractmethod
    def procesar(self, monto: float) -> bool:
        """Procesar el pago por el monto especificado.
        
        Args:
            monto: Cantidad a cobrar (debe ser positiva)
            
        Returns:
            True si el pago fue exitoso, False en caso contrario
            
        Raises:
            ValueError: Si el monto es inválido
        """
        pass
    
    @abstractmethod
    def validar(self) -> bool:
        """Validar que el método de pago está en condiciones de ser usado.
        
        Returns:
            True si el método es válido, False en caso contrario
        """
        pass
    
    def __repr__(self) -> str:
        """Representación legible del método de pago."""
        return f"{self.__class__.__name__}({self._repr_params()})"
    
    def _repr_params(self) -> str:
        """Parámetros para __repr__ (sobrescribir en subtipos)."""
        return ""