"""Módulo de patrones de diseño de OrbitPay."""

from orbitpay.patterns.factory import MetodoPagoFactory
from orbitpay.patterns.strategy import (
    ComisionStrategy,
    ComisionFija,
    ComisionPorcentual,
    ComisionEscalonada,
)
from orbitpay.patterns.observer import (
    EventoPago,
    ObservadorPago,
    ObservadorCorreo,
    ObservadorContabilidad,
    ObservadorLogger,
    GestorEventos,
)

__all__ = [
    "MetodoPagoFactory",
    "ComisionStrategy",
    "ComisionFija",
    "ComisionPorcentual",
    "ComisionEscalonada",
    "EventoPago",
    "ObservadorPago",
    "ObservadorCorreo",
    "ObservadorContabilidad",
    "ObservadorLogger",
    "GestorEventos",
]