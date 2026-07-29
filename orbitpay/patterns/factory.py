"""Módulo con el patrón Factory para crear métodos de pago."""

from typing import Dict, Any, Optional
from orbitpay.payments import Tarjeta, Transferencia, Wallet
from orbitpay.payments.metodo_pago import MetodoPago


class MetodoPagoFactory:
    """Factory para crear métodos de pago.
    
    Encapsula la lógica de creación, aislando al motor
    de las clases concretas (OCP + DIP).
    """
    
    @staticmethod
    def crear_tarjeta(
        numero: str,
        titular: str,
        cvv: str,
        fecha_exp: str,
        saldo_disponible: float = 10000.0
    ) -> Tarjeta:
        """Crear un método de pago con tarjeta."""
        return Tarjeta(numero, titular, cvv, fecha_exp, saldo_disponible)
    
    @staticmethod
    def crear_transferencia(
        banco: str,
        cuenta: str,
        clabe: str,
        saldo_disponible: float = 10000.0
    ) -> Transferencia:
        """Crear un método de pago con transferencia."""
        return Transferencia(banco, cuenta, clabe, saldo_disponible)
    
    @staticmethod
    def crear_wallet(
        email: str,
        saldo_disponible: float = 5000.0
    ) -> Wallet:
        """Crear un método de pago con wallet."""
        return Wallet(email, saldo_disponible)
    
    @staticmethod
    def crear_por_tipo(tipo: str, datos: Dict[str, Any]) -> Optional[MetodoPago]:
        """Crear un método de pago según el tipo especificado.
        
        Args:
            tipo: "tarjeta", "transferencia" o "wallet"
            datos: Diccionario con los datos necesarios
            
        Returns:
            Método de pago creado o None si el tipo no es soportado
            
        Raises:
            ValueError: Si faltan datos requeridos
        """
        if tipo == "tarjeta":
            required = ["numero", "titular", "cvv", "fecha_exp"]
            for campo in required:
                if campo not in datos:
                    raise ValueError(f"Falta campo requerido: {campo}")
            
            return MetodoPagoFactory.crear_tarjeta(
                numero=datos["numero"],
                titular=datos["titular"],
                cvv=datos["cvv"],
                fecha_exp=datos["fecha_exp"],
                saldo_disponible=datos.get("saldo_disponible", 10000.0)
            )
        
        elif tipo == "transferencia":
            required = ["banco", "cuenta", "clabe"]
            for campo in required:
                if campo not in datos:
                    raise ValueError(f"Falta campo requerido: {campo}")
            
            return MetodoPagoFactory.crear_transferencia(
                banco=datos["banco"],
                cuenta=datos["cuenta"],
                clabe=datos["clabe"],
                saldo_disponible=datos.get("saldo_disponible", 10000.0)
            )
        
        elif tipo == "wallet":
            if "email" not in datos:
                raise ValueError("Falta campo requerido: email")
            
            return MetodoPagoFactory.crear_wallet(
                email=datos["email"],
                saldo_disponible=datos.get("saldo_disponible", 5000.0)
            )
        
        else:
            return None