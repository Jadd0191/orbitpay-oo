"""Módulo con el patrón Observer para eventos de pago."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime


class EventoPago:
    """Representa un evento de pago."""
    
    def __init__(
        self,
        tipo: str,
        datos: Dict[str, Any],
        timestamp: datetime = None
    ):
        self.tipo = tipo  # "aprobado", "rechazado", "fallido"
        self.datos = datos
        self.timestamp = timestamp or datetime.now()


class ObservadorPago(ABC):
    """Observador abstracto para eventos de pago."""
    
    @abstractmethod
    def actualizar(self, evento: EventoPago) -> None:
        """Reaccionar a un evento de pago."""
        pass


class ObservadorCorreo(ObservadorPago):
    """Observador que envía correos electrónicos."""
    
    def __init__(self, email_remitente: str = "noreply@orbitpay.com"):
        self.email_remitente = email_remitente
    
    def actualizar(self, evento: EventoPago) -> None:
        """Enviar correo según el evento."""
        if evento.tipo == "aprobado":
            print(f"  ✉️ Enviando correo de confirmación a {evento.datos.get('email', 'usuario')}")
            print(f"     Asunto: Pago aprobado por ${evento.datos.get('monto', 0):.2f}")
        elif evento.tipo == "rechazado":
            print(f"  ✉️ Enviando correo de rechazo a {evento.datos.get('email', 'usuario')}")
            print(f"     Asunto: Pago rechazado - ${evento.datos.get('monto', 0):.2f}")
        else:
            print(f"  ✉️ Enviando correo de notificación a {evento.datos.get('email', 'usuario')}")


class ObservadorContabilidad(ObservadorPago):
    """Observador que registra eventos para contabilidad."""
    
    def __init__(self):
        self.eventos: List[EventoPago] = []
    
    def actualizar(self, evento: EventoPago) -> None:
        """Registrar evento para contabilidad."""
        self.eventos.append(evento)
        print(f"  📊 Registro contable: {evento.tipo} - ${evento.datos.get('monto', 0):.2f}")
        print(f"     Total eventos registrados: {len(self.eventos)}")
    
    def obtener_eventos(self) -> List[EventoPago]:
        """Obtener todos los eventos registrados."""
        return self.eventos.copy()


class ObservadorLogger(ObservadorPago):
    """Observador que escribe logs del sistema."""
    
    def __init__(self):
        self.logs: List[str] = []
    
    def actualizar(self, evento: EventoPago) -> None:
        """Escribir log del evento."""
        mensaje = (
            f"[{evento.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Evento: {evento.tipo} | "
            f"Monto: ${evento.datos.get('monto', 0):.2f} | "
            f"Método: {evento.datos.get('metodo', 'desconocido')}"
        )
        self.logs.append(mensaje)
        print(f"  📝 Log: {mensaje}")


class GestorEventos:
    """Gestor de eventos que implementa el patrón Observer."""
    
    def __init__(self):
        self._observadores: List[ObservadorPago] = []
    
    def suscribir(self, observador: ObservadorPago) -> None:
        """Agregar un observador."""
        self._observadores.append(observador)
    
    def desuscribir(self, observador: ObservadorPago) -> None:
        """Eliminar un observador."""
        if observador in self._observadores:
            self._observadores.remove(observador)
    
    def notificar(self, evento: EventoPago) -> None:
        """Notificar a todos los observadores."""
        for observador in self._observadores:
            observador.actualizar(evento)