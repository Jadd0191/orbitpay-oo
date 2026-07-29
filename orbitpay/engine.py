"""Módulo con el motor de pagos que orquesta todo el sistema."""

from typing import Optional
from orbitpay.domain import Cuenta, SaldoInsuficienteError, MontoInvalidoError
from orbitpay.payments import MetodoPago
from orbitpay.patterns.factory import MetodoPagoFactory
from orbitpay.patterns.strategy import ComisionStrategy, ComisionPorcentual
from orbitpay.patterns.observer import GestorEventos, EventoPago, ObservadorPago


class Engine:
    """Motor de pagos que orquesta el procesamiento completo.
    
    Principios SOLID aplicados:
    - SRP: Solo orquesta el pago
    - OCP: Extensible con nuevas estrategias y observadores
    - DIP: Depende de abstracciones (MetodoPago, ComisionStrategy, Observador)
    """
    
    def __init__(
        self,
        strategy: ComisionStrategy = None,
        gestor_eventos: GestorEventos = None
    ):
        """Inicializar el motor.
        
        Args:
            strategy: Estrategia de comisión (Strategy Pattern)
            gestor_eventos: Gestor de eventos (Observer Pattern)
        """
        self.strategy = strategy or ComisionPorcentual(2.5)
        self.gestor_eventos = gestor_eventos or GestorEventos()
    
    def procesar_pago(
        self,
        cuenta: Cuenta,
        metodo_pago: MetodoPago,
        monto: float,
        descripcion: str = "Pago"
    ) -> bool:
        """Procesar un pago completo.
        
        Flujo:
        1. Validar método de pago
        2. Calcular comisión
        3. Verificar saldo suficiente (monto + comisión)
        4. Retirar monto + comisión de la cuenta
        5. Procesar pago
        6. Notificar eventos
        
        Args:
            cuenta: Cuenta del usuario
            metodo_pago: Método de pago a utilizar
            monto: Monto a pagar
            descripcion: Descripción del pago
            
        Returns:
            True si el pago fue exitoso
            
        Raises:
            ValueError: Si el monto es inválido
            SaldoInsuficienteError: Si el saldo es insuficiente
        """
        if monto <= 0:
            raise ValueError(f"El monto debe ser positivo: {monto}")
        
        print("\n" + "=" * 60)
        print("💳 PROCESANDO PAGO")
        print("=" * 60)
        print(f"Cuenta: {cuenta.titular} (ID: {cuenta.id[:8]}...)")
        print(f"Monto: ${monto:.2f}")
        print(f"Método: {metodo_pago.__class__.__name__}")
        print(f"Descripción: {descripcion}")
        
        # PASO 1: Validar método de pago
        print("\n1️⃣ Validando método de pago...")
        if not metodo_pago.validar():
            print("   ❌ Método de pago inválido")
            self._notificar_evento("rechazado", cuenta, metodo_pago, monto, "Método inválido")
            return False
        print("   ✅ Método válido")
        
        # PASO 2: Calcular comisión (Strategy Pattern)
        print("\n2️⃣ Calculando comisión...")
        comision = self.strategy.calcular(monto)
        total = monto + comision
        print(f"   Comisión: ${comision:.2f}")
        print(f"   Total a cobrar: ${total:.2f}")
        
        # PASO 3: Verificar saldo suficiente
        print("\n3️⃣ Verificando saldo...")
        print(f"   Saldo disponible: ${cuenta.saldo:.2f}")
        if total > cuenta.saldo:
            print(f"   ❌ Saldo insuficiente: ${cuenta.saldo:.2f} < ${total:.2f}")
            self._notificar_evento("rechazado", cuenta, metodo_pago, monto, "Saldo insuficiente")
            return False
        print("   ✅ Saldo suficiente")
        
        # PASO 4: Retirar de la cuenta
        print("\n4️⃣ Retirando de la cuenta...")
        try:
            cuenta.retirar(total, f"{descripcion} (incluye comisión)")
            print(f"   ✅ Retiro exitoso")
            print(f"   Nuevo saldo: ${cuenta.saldo:.2f}")
        except (SaldoInsuficienteError, MontoInvalidoError) as e:
            print(f"   ❌ Error en retiro: {e}")
            self._notificar_evento("fallido", cuenta, metodo_pago, monto, str(e))
            return False
        
        # PASO 5: Procesar el pago con el método de pago
        print("\n5️⃣ Procesando pago...")
        try:
            resultado = metodo_pago.procesar(monto)
            if not resultado:
                # Revertir retiro si el pago falla
                print("   ❌ Pago fallido - Revertiendo retiro...")
                cuenta.depositar(total, "REVERSO: Pago fallido")
                print(f"   Saldo restaurado: ${cuenta.saldo:.2f}")
                self._notificar_evento("fallido", cuenta, metodo_pago, monto, "Pago fallido en procesador")
                return False
            print("   ✅ Pago procesado exitosamente")
        except Exception as e:
            print(f"   ❌ Error en procesamiento: {e}")
            # Revertir retiro
            cuenta.depositar(total, "REVERSO: Error en pago")
            print(f"   Saldo restaurado: ${cuenta.saldo:.2f}")
            self._notificar_evento("fallido", cuenta, metodo_pago, monto, str(e))
            return False
        
        # PASO 6: Notificar eventos (Observer Pattern)
        print("\n6️⃣ Notificando eventos...")
        self._notificar_evento("aprobado", cuenta, metodo_pago, monto, "Pago exitoso")
        
        print("\n" + "=" * 60)
        print("✅ PAGO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print(f"💰 Nuevo saldo: ${cuenta.saldo:.2f}")
        print(f"💳 Comisión cobrada: ${comision:.2f}")
        
        return True
    
    def _notificar_evento(
        self,
        tipo: str,
        cuenta: Cuenta,
        metodo_pago: MetodoPago,
        monto: float,
        mensaje: str
    ) -> None:
        """Notificar evento a los observadores."""
        evento = EventoPago(
            tipo=tipo,
            datos={
                "cuenta_id": cuenta.id,
                "cuenta_titular": cuenta.titular,
                "metodo": metodo_pago.__class__.__name__,
                "monto": monto,
                "mensaje": mensaje,
                "saldo_restante": cuenta.saldo,
                "email": getattr(metodo_pago, 'email', None) or cuenta.titular
            }
        )
        self.gestor_eventos.notificar(evento)
    
    def agregar_observador(self, observador: ObservadorPago) -> None:
        """Agregar un observador de eventos."""
        self.gestor_eventos.suscribir(observador)
    
    def cambiar_estrategia(self, strategy: ComisionStrategy) -> None:
        """Cambiar la estrategia de comisión."""
        self.strategy = strategy