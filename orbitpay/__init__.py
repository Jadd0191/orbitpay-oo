"""OrbitPay OO - Motor de pagos orientado a objetos."""

__version__ = "0.6.0"

# Domain
from orbitpay.domain import (
    Cuenta,
    Transaccion,
    Suscripcion,
    SaldoInsuficienteError,
    MontoInvalidoError,
)

# Payments
from orbitpay.payments import (
    MetodoPago,
    Tarjeta,
    Transferencia,
    Wallet,
)

# Patterns
from orbitpay.patterns import (
    MetodoPagoFactory,
    ComisionStrategy,
    ComisionFija,
    ComisionPorcentual,
    ComisionEscalonada,
    EventoPago,
    ObservadorPago,
    ObservadorCorreo,
    ObservadorContabilidad,
    ObservadorLogger,
    GestorEventos,
)

# Engine
from orbitpay.engine import Engine

__all__ = [
    # Domain
    "Cuenta",
    "Transaccion",
    "Suscripcion",
    "SaldoInsuficienteError",
    "MontoInvalidoError",
    # Payments
    "MetodoPago",
    "Tarjeta",
    "Transferencia",
    "Wallet",
    # Patterns
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
    # Engine
    "Engine",
    "__version__",
]