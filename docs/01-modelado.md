# Fase 2: Modelado de Clases y Requisitos

## 1. Requisitos del Sistema

### Requisitos Funcionales

| ID | Requisito | Prioridad | Descripción |
|----|-----------|-----------|-------------|
| RF-01 | Procesar pago | Alta | El sistema debe permitir procesar un pago usando cualquier método de pago soportado |
| RF-02 | Calcular comisión | Alta | El sistema debe calcular la comisión aplicable a cada transacción según reglas de negocio |
| RF-03 | Registrar transacción | Alta | Cada operación debe quedar registrada con fecha, monto, tipo y estado |
| RF-04 | Gestionar suscripción | Media | El sistema debe permitir crear, renovar y cancelar suscripciones |
| RF-05 | Consultar saldo | Alta | El usuario debe poder consultar el saldo disponible de su cuenta |
| RF-06 | Validar método de pago | Alta | Antes de procesar, el sistema debe validar que el método de pago es válido |
| RF-07 | Notificar eventos | Media | El sistema debe notificar eventos importantes (pago aprobado/rechazado) |
| RF-08 | Soportar múltiples métodos de pago | Alta | Tarjeta, Transferencia, Wallet (extensible a más) |
| RF-09 | Manejar errores de pago | Alta | El sistema debe manejar elegantemente fallos de pago (saldo insuficiente, tarjeta rechazada) |
| RF-10 | Historial de transacciones | Media | El usuario debe poder ver su historial de transacciones |

### Requisitos No Funcionales

| ID | Requisito | Prioridad | Descripción |
|----|-----------|-----------|-------------|
| RNF-01 | Integridad de datos | Crítica | El saldo nunca debe quedar negativo; las transacciones son inmutables |
| RNF-02 | Testeabilidad | Alta | El sistema debe tener cobertura de pruebas ≥80% |
| RNF-03 | Extensibilidad | Alta | Agregar nuevos métodos de pago no debe requerir modificar el núcleo |
| RNF-04 | Mantenibilidad | Alta | Código limpio, principios SOLID, patrones de diseño |
| RNF-05 | Documentación | Media | Documentación clara de todas las clases y métodos públicos |
| RNF-06 | Tipo seguro | Media | Uso de type hints y mypy --strict |
| RNF-07 | Desacoplamiento | Alta | Las capas deben estar desacopladas (dominio, patrones, motor) |
| RNF-08 | Rendimiento | Baja | El sistema debe procesar pagos en < 100ms (en memoria) |

---

## 2. Diagrama de Clases

### Diagrama UML
┌─────────────────────────────────────────────────────────────────┐
│ ENGINE │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ +procesar_pago(cuenta, metodo_pago, monto) │ │
│ │ +crear_suscripcion(cuenta, suscripcion_data) │ │
│ │ +consultar_historial(cuenta) │ │
│ └─────────────────────────────────────────────────────────┘ │
│ │ │
│ ┌───────────────────┼───────────────────┐ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ ┌──────────────┐ ┌──────────────────┐ ┌──────────────┐ │
│ │ Cuenta │ │ MetodoPago │ │ Suscripción │ │
│ │ │ │ <<abstract>> │ │ │ │
│ │ -_saldo │ │ │ │ -nombre │ │
│ │ -titular │ │ +procesar() │ │ -monto │ │
│ │ -transacciones│ │ +validar() │ │ -periodicidad│ │
│ │ -suscripciones│ │ │ │ -activa │ │
│ │ │ │ △ │ │ -fecha_inicio│ │
│ │ +depositar() │ │ │ │ │ -fecha_fin │ │
│ │ +retirar() │ │ │ │ │ │ │
│ │ +saldo │ │ │ │ │ +renovar() │ │
│ │ @property │ │ │ │ │ +cancelar() │ │
│ └──────────────┘ │ │ │ │ +proximo_pago│ │
│ 1 │ ┌────┴────┐ │ └──────────────┘ │
│ │ │ │ │ │ 1 │
│ │ │ ▼ ▼ │ │ │
│ └──────────┤ Tarjeta │Transferencia│ │ │
│ │ Wallet │ │ │ │
│ └─────────┘ │ │ │
│ │ │ │
│ ┌───────────┴──────────┴───┐ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ ┌──────────────┐ ┌──────────┐ ┌─────────┐│
│ │ Transacción │ │Factory │ │Observer ││
│ │ │ │ │ │ ││
│ │ -id │ │+crear() │ │+update()││
│ │ -monto │ │ │ │ ││
│ │ -tipo │ └──────────┘ └─────────┘│
│ │ -fecha │ │
│ │ -descripcion │ │
│ │ -estado │ │
│ │ │ │
│ │ +repr() │ │
│ │ +eq() │ │
│ │ +lt() │ │
│ └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘


### Relaciones entre Clases

| Relación | Clase A | Clase B | Tipo | Descripción |
|----------|---------|---------|------|-------------|
| Composición | Cuenta | Transacción | 1 → * | Una cuenta tiene muchas transacciones |
| Composición | Cuenta | Suscripción | 1 → * | Una cuenta puede tener muchas suscripciones |
| Asociación | Engine | Cuenta | 1 → 1 | El motor usa una cuenta específica |
| Asociación | Engine | MetodoPago | 1 → 1 | El motor usa un método de pago para procesar |
| Herencia | MetodoPago | Tarjeta | - | Tarjeta es un tipo de MetodoPago |
| Herencia | MetodoPago | Transferencia | - | Transferencia es un tipo de MetodoPago |
| Herencia | MetodoPago | Wallet | - | Wallet es un tipo de MetodoPago |
| Dependencia | Engine | Factory | 1 → 1 | El motor usa Factory para crear métodos de pago |
| Dependencia | Engine | Strategy | 1 → 1 | El motor usa Strategy para calcular comisiones |
| Dependencia | Engine | Observer | 1 → * | El motor notifica a múltiples observers |

---

## 3. Responsabilidades de Clases (SRP)

### Cuenta
**Responsabilidad Única**: Gestionar el estado financiero de un usuario.

**Qué hace**:
- Mantiene el saldo y garantiza su integridad
- Registra transacciones asociadas
- Gestiona suscripciones activas

**Qué NO hace**:
- No procesa pagos directamente
- No calcula comisiones
- No notifica eventos

### Transacción
**Responsabilidad Única**: Representar un movimiento financiero inmutable.

**Qué hace**:
- Almacena los datos de una operación
- Proporciona métodos para comparación y representación
- Garantiza que los datos no cambien después de la creación

**Qué NO hace**:
- No modifica saldos (eso es responsabilidad de Cuenta)
- No valida reglas de negocio complejas

### Suscripción
**Responsabilidad Única**: Gestionar servicios recurrentes.

**Qué hace**:
- Mantiene el estado de una suscripción (activa/inactiva)
- Calcula próxima fecha de pago
- Permite renovación y cancelación

**Qué NO hace**:
- No procesa cobros (eso es del Engine)
- No consulta saldos

### MetodoPago (ABC)
**Responsabilidad Única**: Definir el contrato para procesar pagos.

**Qué hace**:
- Establece la interfaz que todos los métodos de pago deben implementar
- Garantiza polimorfismo en el sistema

**Qué NO hace**:
- No implementa lógica de pago específica
- No conoce los detalles de implementación de sus subtipos

### Tarjeta, Transferencia, Wallet
**Responsabilidad Única**: Implementar la lógica específica de cada método de pago.

**Qué hace**:
- Cada uno sabe cómo procesarse a sí mismo
- Cada uno valida sus propios datos

**Qué NO hace**:
- No conocen el saldo de la cuenta
- No calculan comisiones

### Engine (Motor de Pagos)
**Responsabilidad Única**: Orquestar el flujo completo de pago.

**Qué hace**:
- Coordina la interacción entre Cuenta, MetodoPago, y otros componentes
- Aplica estrategias de comisión
- Notifica eventos

**Qué NO hace**:
- No implementa lógica de pago específica
- No almacena datos de forma persistente

### Factory (MetodoPagoFactory)
**Responsabilidad Única**: Crear instancias de métodos de pago.

**Qué hace**:
- Encapsula la lógica de creación
- Aísla al Engine de las clases concretas

**Qué NO hace**:
- No procesa pagos
- No valida datos de negocio

### Strategy (ComisionStrategy)
**Responsabilidad Única**: Calcular comisiones según diferentes reglas.

**Qué hace**:
- Define una interfaz para calcular comisiones
- Permite intercambiar algoritmos

**Qué NO hace**:
- No procesa pagos
- No modifica el estado de la cuenta

### Observer
**Responsabilidad Única**: Notificar eventos a suscriptores.

**Qué hace**:
- Gestiona una lista de observadores
- Notifica cuando ocurren eventos

**Qué NO hace**:
- No procesa la lógica de negocio
- No decide qué eventos ocurren

---

## 4. Detalle de Clases y Métodos

### Cuenta

```python
@dataclass
class Cuenta:
    id: str
    titular: str
    _saldo: float = 0.0
    transacciones: List[Transaccion] = field(default_factory=list)
    suscripciones: List[Suscripcion] = field(default_factory=list)
    
    @property
    def saldo(self) -> float:
        """Obtener saldo actual."""
        return self._saldo
    
    def depositar(self, monto: float) -> None:
        """Depositar dinero en la cuenta."""
        # Validar monto > 0
        # Actualizar saldo
        # Crear y registrar transacción
    
    def retirar(self, monto: float) -> None:
        """Retirar dinero de la cuenta."""
        # Validar monto > 0
        # Validar saldo suficiente
        # Actualizar saldo
        # Crear y registrar transacción
    
    def agregar_transaccion(self, transaccion: Transaccion) -> None:
        """Agregar transacción al historial."""
    
    def agregar_suscripcion(self, suscripcion: Suscripcion) -> None:
        """Agregar suscripción a la cuenta."""