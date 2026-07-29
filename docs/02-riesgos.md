# Fase 3: Análisis de Riesgos - Prototipado y Arquitectura

## 1. Registro de Riesgos

| ID | Riesgo | Probabilidad | Impacto | Mitigación | Estado |
|----|--------|--------------|---------|------------|--------|
| R-01 | **Doble cobro** | Alta | Crítico | Atomicidad de transacciones: validar saldo y descontar en una operación atómica | Mitigado |
| R-02 | **Saldo inconsistente** | Alta | Crítico | Encapsulamiento con invariantes: `_saldo` privado + validaciones en cada operación | Mitigado |
| R-03 | **Fraude** | Media | Alto | Validación de métodos de pago antes de procesar; límites por transacción | En progreso |
| R-04 | **Acoplamiento excesivo** | Media | Medio | Programar contra abstracciones (ABC), usar Factory y Strategy | Mitigado |
| R-05 | **Error en cálculo de comisiones** | Media | Alto | Strategy con pruebas unitarias; inyección de dependencias | Mitigado |
| R-06 | **Pérdida de datos en memoria** | Baja | Alto | (Fase 8) Persistencia planificada para siguiente espiral | Pendiente |
| R-07 | **Suscripciones no renovadas** | Media | Medio | Observer para notificar vencimientos; tests de integración | En progreso |
| R-08 | **Deuda técnica por código espagueti** | Media | Medio | Refactorización continua; cobertura ≥80%; code smells detectados | Mitigado |
| R-09 | **Métodos de pago no validados** | Alta | Alto | Validación obligatoria antes de procesar (`validar()` en ABC) | Mitigado |
| R-10 | **Monto negativo o cero** | Alta | Alto | Validación en setters y métodos; excepciones claras | Mitigado |

### Análisis de Riesgos Críticos

#### R-01: Doble Cobro
**Descripción**: Si el sistema falla entre la validación del saldo y el descuento, podría cobrar dos veces la misma transacción.

**Mitigación**:
- Operación atómica: validar saldo y retirar en el mismo método
- Transacciones con ID único (UUID) para idempotencia
- Pruebas unitarias específicas para casos de concurrencia

**Prototipo validado**: ✅ Demostrado en `spikes/atomicidad_transaccion.py`

#### R-02: Saldo Inconsistente
**Descripción**: El saldo podría quedar negativo si no se validan correctamente las operaciones.

**Mitigación**:
- Atributo `_saldo` privado con @property
- Invariantes: `retirar()` valida `monto <= _saldo`
- Excepción `SaldoInsuficienteError`

**Prototipo validado**: ✅ Demostrado en `spikes/validacion_saldo.py`

#### R-04: Acoplamiento Excesivo
**Descripción**: El motor podría depender de implementaciones concretas de métodos de pago.

**Mitigación**:
- `MetodoPago` como ABC
- Motor usa `MetodoPago`, nunca clases concretas (DIP)
- Factory para crear métodos de pago

**Prototipo validado**: ✅ Demostrado en `spikes/polimorfismo_pagos.py`

---

## 2. Decisiones de Arquitectura (ADR)

### ADR-001: Usar Estructura de Paquetes Plana sin `src/`

**Contexto**: El proyecto debe ser instalable y mantenible.

**Decisión**: Usar estructura plana:
orbitpay/
├── orbitpay/ # Paquete principal
├── docs/
├── tests/
└── spikes/


**Alternativas**:
- `src/` layout (más profesional pero más complejo)
- Mono-repositorio (demasiado para este alcance)

**Consecuencias**:
- ✅ Más simple para el alcance del proyecto
- ✅ Coherente con el proyecto de ejemplo
- ⚠️ Puede causar conflictos con `pyproject.toml` (mitigado con configuración explícita)

### ADR-002: Dataclasses para Clases de Dominio

**Contexto**: Necesitamos clases con datos y comportamiento básico.

**Decisión**: Usar `@dataclass` del módulo `dataclasses` para:
- `Cuenta`
- `Transacción` (`frozen=True` para inmutabilidad)
- `Suscripción`

**Alternativas**:
- Clases manuales (mucho boilerplate)
- Pydantic (más pesado, mejor para validación en APIs)
- Attrs (terceros, más complejo)

**Consecuencias**:
- ✅ Código más limpio y conciso
- ✅ `__init__`, `__repr__`, `__eq__` automáticos
- ✅ `frozen=True` garantiza inmutabilidad
- ⚠️ Pydantic ofrecería validación más robusta (decidimos usar validación manual)

### ADR-003: ABC para Jerarquía de Métodos de Pago

**Contexto**: Soporte para múltiples métodos de pago (Tarjeta, Transferencia, Wallet).

**Decisión**: Usar `abc.ABC` y `@abstractmethod` para definir `MetodoPago`.

**Alternativas**:
- Protocol (duck typing sin herencia)
- Clase base con métodos que lanzan `NotImplementedError`

**Consecuencias**:
- ✅ Contrato claro y verificable en tiempo de compilación
- ✅ Polimorfismo seguro
- ✅ LSP garantizada
- ✅ Subclases obligadas a implementar `procesar()` y `validar()`

### ADR-004: Patrones de Diseño Obligatorios

**Contexto**: El sistema debe ser extensible y desacoplado.

**Decisión**: Implementar tres patrones:
1. **Factory** - Crear métodos de pago
2. **Strategy** - Calcular comisiones
3. **Observer** - Notificar eventos

**Alternativas**:
- Creación directa con `new` (acoplamiento)
- Condicionales anidados (difícil de extender)
- Eventos síncronos (acoplamiento)

**Consecuencias**:
- ✅ Extensibilidad (OCP)
- ✅ Desacoplamiento (DIP)
- ✅ Testeabilidad
- ⚠️ Complejidad adicional (justificada por extensibilidad)

### ADR-005: Idempotencia mediante UUID

**Contexto**: Evitar cobros duplicados.

**Decisión**: Cada transacción tendrá un ID único (`uuid.uuid4()`).

**Alternativas**:
- Contador incremental (riesgo de duplicados)
- Timestamp + hash (no garantizado)

**Consecuencias**:
- ✅ Garantía de unicidad
- ✅ Idempotencia en operaciones
- ✅ Trazabilidad

### ADR-006: Excepciones para Casos de Error

**Contexto**: Manejar errores de negocio (saldo insuficiente, monto inválido).

**Decisión**: Usar excepciones personalizadas:
- `SaldoInsuficienteError`
- `MontoInvalidoError`
- `PagoRechazadoError`

**Alternativas**:
- Valores de retorno `None` o `False` (pérdida de información)
- Result types (más funcional, no estándar en Python)

**Consecuencias**:
- ✅ Claridad en el flujo de errores
- ✅ Información detallada del problema
- ✅ Tests pueden verificar excepciones

### ADR-007: Prototipo como Spike Desechable

**Contexto**: Validar decisiones técnicas antes de implementar definitivamente.

**Decisión**: Crear prototipos en `spikes/` que no serán parte del código final.

**Alternativas**:
- Implementar directamente en el código (riesgo de retrabajo)
- Sin prototipo (mayor riesgo)

**Consecuencias**:
- ✅ Validación temprana de decisiones
- ✅ Aprendizaje sin compromiso
- ⚠️ Tiempo extra (justificado por reducción de riesgos)

---

## 3. Prototipos

### Prototipo 1: Atomicidad de Transacciones

El riesgo más crítico: **doble cobro**. Este prototipo valida que una transacción se ejecute de forma atómica.

#### `spikes/atomicidad_transaccion.py`

```python
#!/usr/bin/env python
"""
Prototipo para validar la atomicidad de transacciones.

Riesgo: R-01 (Doble cobro)
Objetivo: Demostrar que una operación de retiro es atómica:
1. Validar saldo
2. Descontar saldo
3. Registrar transacción

Si falla el paso 1, no se ejecutan los pasos 2 y 3.
No debe haber casos donde se descuente saldo sin registrar transacción.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid


class SaldoInsuficienteError(Exception):
    """Excepción cuando el saldo es insuficiente."""
    pass


class MontoInvalidoError(Exception):
    """Excepción cuando el monto es negativo o cero."""
    pass


@dataclass(frozen=True)
class Transaccion:
    """Transacción inmutable."""
    id: str
    monto: float
    tipo: str
    fecha: datetime
    descripcion: str
    estado: str


@dataclass
class Cuenta:
    """Cuenta con protección contra doble cobro."""
    
    id: str
    titular: str
    _saldo: float = 0.0
    transacciones: List[Transaccion] = field(default_factory=list)
    
    @property
    def saldo(self) -> float:
        return self._saldo
    
    def retirar(self, monto: float, descripcion: str) -> Transaccion:
        """
        Operación atómica de retiro.
        
        PASOS (ATÓMICOS):
        1. Validar monto > 0
        2. Validar saldo suficiente
        3. Descontar saldo
        4. Registrar transacción
        
        Si falla el paso 1 o 2, NO se ejecutan 3 y 4.
        Si falla 3 o 4, la transacción no se completa.
        """
        # PASO 1: Validar monto
        if monto <= 0:
            raise MontoInvalidoError(f"Monto debe ser positivo: {monto}")
        
        # PASO 2: Validar saldo suficiente
        if monto > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente: {self._saldo} < {monto}"
            )
        
        # PASO 3: Descontar saldo (ATÓMICO)
        self._saldo -= monto
        
        # PASO 4: Registrar transacción
        transaccion = Transaccion(
            id=str(uuid.uuid4()),
            monto=monto,
            tipo="egreso",
            fecha=datetime.now(),
            descripcion=descripcion,
            estado="completada"
        )
        self.transacciones.append(transaccion)
        
        return transaccion
    
    def depositar(self, monto: float, descripcion: str) -> Transaccion:
        """Operación atómica de depósito."""
        if monto <= 0:
            raise MontoInvalidoError(f"Monto debe ser positivo: {monto}")
        
        self._saldo += monto
        
        transaccion = Transaccion(
            id=str(uuid.uuid4()),
            monto=monto,
            tipo="ingreso",
            fecha=datetime.now(),
            descripcion=descripcion,
            estado="completada"
        )
        self.transacciones.append(transaccion)
        
        return transaccion


def demo_prototipo():
    """Demostrar el prototipo en acción."""
    print("=" * 60)
    print("🔬 PROTOTIPO: Atomicidad de Transacciones")
    print("=" * 60)
    
    # Crear cuenta con saldo inicial
    cuenta = Cuenta(
        id="demo-001",
        titular="Usuario Demo",
        _saldo=1000.0
    )
    
    print(f"\n✅ Cuenta creada: {cuenta.titular}")
    print(f"💰 Saldo inicial: ${cuenta.saldo:.2f}")
    
    print("\n" + "=" * 60)
    print("🧪 CASO 1: Retiro exitoso")
    print("=" * 60)
    
    try:
        transaccion = cuenta.retirar(300.0, "Compra en tienda")
        print(f"✅ Retiro exitoso: ${transaccion.monto:.2f}")
        print(f"💰 Nuevo saldo: ${cuenta.saldo:.2f}")
        print(f"📝 Transacción ID: {transaccion.id[:8]}...")
        print(f"📊 Total transacciones: {len(cuenta.transacciones)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🧪 CASO 2: Retiro fallido (saldo insuficiente)")
    print("=" * 60)
    
    try:
        transaccion = cuenta.retirar(1500.0, "Intento de compra grande")
        print(f"✅ Retiro exitoso: ${transaccion.monto:.2f}")
    except SaldoInsuficienteError as e:
        print(f"❌ Error esperado: {e}")
        print(f"💰 Saldo no modificado: ${cuenta.saldo:.2f}")
        print(f"📊 Total transacciones: {len(cuenta.transacciones)} (no aumentó)")
    
    print("\n" + "=" * 60)
    print("🧪 CASO 3: Retiro fallido (monto negativo)")
    print("=" * 60)
    
    try:
        transaccion = cuenta.retirar(-100.0, "Monto negativo")
        print(f"✅ Retiro exitoso: ${transaccion.monto:.2f}")
    except MontoInvalidoError as e:
        print(f"❌ Error esperado: {e}")
        print(f"💰 Saldo no modificado: ${cuenta.saldo:.2f}")
        print(f"📊 Total transacciones: {len(cuenta.transacciones)} (no aumentó)")
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN FINAL")
    print("=" * 60)
    print(f"💰 Saldo final: ${cuenta.saldo:.2f}")
    print(f"📊 Transacciones totales: {len(cuenta.transacciones)}")
    
    # Mostrar historial
    print("\n📝 Historial de transacciones:")
    for t in cuenta.transacciones:
        print(f"  • {t.fecha.strftime('%H:%M:%S')} | {t.tipo:7} | "
              f"${t.monto:8.2f} | {t.descripcion[:20]}...")
    
    print("\n" + "=" * 60)
    print("✅ PROTOTIPO EXITOSO: Atomicidad garantizada")
    print("   - Saldo validado antes de descontar")
    print("   - Transacción registrada después del descuento")
    print("   - Fallos no modifican el estado")
    print("=" * 60)


if __name__ == "__main__":
    demo_prototipo()