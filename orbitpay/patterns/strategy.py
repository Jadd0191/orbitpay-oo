"""Módulo con el patrón Strategy para calcular comisiones."""

from abc import ABC, abstractmethod


class ComisionStrategy(ABC):
    """Estrategia abstracta para calcular comisiones."""
    
    @abstractmethod
    def calcular(self, monto: float) -> float:
        """Calcular la comisión para un monto dado.
        
        Args:
            monto: Monto de la transacción
            
        Returns:
            Comisión calculada
        """
        pass


class ComisionFija(ComisionStrategy):
    """Estrategia: comisión fija por transacción."""
    
    def __init__(self, comision: float = 5.0):
        self.comision = comision
    
    def calcular(self, monto: float) -> float:
        """Calcular comisión fija."""
        if monto <= 0:
            return 0.0
        return min(self.comision, monto * 0.5)  # No más del 50%


class ComisionPorcentual(ComisionStrategy):
    """Estrategia: comisión porcentual sobre el monto."""
    
    def __init__(self, porcentaje: float = 2.5):
        self.porcentaje = porcentaje
    
    def calcular(self, monto: float) -> float:
        """Calcular comisión porcentual."""
        if monto <= 0:
            return 0.0
        return (monto * self.porcentaje) / 100.0


class ComisionEscalonada(ComisionStrategy):
    """Estrategia: comisión escalonada según el monto."""
    
    def calcular(self, monto: float) -> float:
        """Calcular comisión con escalas.
        
        - Montos <= 100: 5% 
        - Montos <= 500: 3%
        - Montos > 500: 1.5%
        """
        if monto <= 0:
            return 0.0
        elif monto <= 100:
            return (monto * 5.0) / 100.0
        elif monto <= 500:
            return (monto * 3.0) / 100.0
        else:
            return (monto * 1.5) / 100.0