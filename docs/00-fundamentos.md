
---
```markdown
# Fundamentos de la Espiral y Diseño OO

## Plan de Espiral

El proyecto OrbitPay OO se desarrollará siguiendo la Metodología Espiral, con 7 vueltas principales (más una fase de cierre). Cada vuelta representa una fase del proyecto con objetivos claros, identificación de riesgos y entregables concretos.

### Vuelta 0: Fundamentos y Planificación (Fase 1)
- **Objetivo**: Establecer las bases del proyecto, definir el plan de espiral y el dominio inicial
- **Riesgos**: Falta de claridad en el alcance, mala definición de las clases del dominio
- **Mitigación**: Documentación detallada, diagramas conceptuales, revisión del modelo antes de codificar
- **Entregable**: `docs/00-fundamentos.md`, estructura del proyecto, esqueletos iniciales

### Vuelta 1: Análisis y Modelado (Fase 2)
- **Objetivo**: Levantar requisitos completos y crear el diagrama de clases detallado
- **Riesgos**: Modelado incorrecto, relaciones mal definidas entre clases
- **Mitigación**: Uso de tarjetas CRC, validación del modelo con casos de uso
- **Entregable**: `docs/01-modelado.md`, esqueletos de clases (`pass`)

### Vuelta 2: Análisis de Riesgos y Prototipado (Fase 3)
- **Objetivo**: Identificar riesgos técnicos y prototipar la arquitectura crítica
- **Riesgos**: Riesgos no identificados, arquitectura inadecuada
- **Mitigación**: Registro formal de riesgos, prototipos desechables para validar decisiones
- **Entregable**: `docs/02-riesgos.md`, código en `spikes/`

### Vuelta 3: Ingeniería - Encapsulamiento (Fase 4)
- **Objetivo**: Implementar el núcleo del dominio con encapsulamiento real
- **Riesgos**: Invariantes rotas, mutación de estado desde fuera
- **Mitigación**: @property, validaciones en setters, atributos protegidos
- **Entregable**: Clases del dominio funcionales, `docs/03-encapsulamiento.md`

### Vuelta 4: Ingeniería - Herencia y Polimorfismo (Fase 5)
- **Objetivo**: Crear la jerarquía de métodos de pago con ABC y polimorfismo
- **Riesgos**: Violación de LSP, acoplamiento a implementaciones concretas
- **Mitigación**: Definición de contratos abstractos claros, tests de sustitución
- **Entregable**: Jerarquía MetodoPago, `docs/04-herencia-polimorfismo.md`

### Vuelta 5: Ingeniería - SOLID y Patrones (Fase 6)
- **Objetivo**: Refactorizar para aplicar SOLID y patrones de diseño
- **Riesgos**: Over-engineering, complejidad innecesaria
- **Mitigación**: Aplicación gradual de patrones, justificación documentada
- **Entregable**: Código con patrones Factory, Strategy, Observer; `docs/05-solid-patrones.md`

### Vuelta 6: Evaluación y Refactorización (Fase 7)
- **Objetivo**: Construir suite de pruebas y refactorizar code smells
- **Riesgos**: Tests insuficientes, refactor que rompe funcionalidad
- **Mitigación**: Cobertura ≥80%, refactor con tests en verde
- **Entregable**: Suite de pruebas, `docs/06-testing-refactor.md`

### Vuelta 7: Integración y Cierre (Fase 8)
- **Objetivo**: Integrar todo, empaquetar y planificar la siguiente espiral
- **Riesgos**: Integración fallida, paquete no instalable
- **Mitigación**: Tests de integración, CI/CD
- **Entregable**: Paquete instalable, `docs/07-cierre.md`

---

## Pilares de la Programación Orientada a Objetos Aplicados a OrbitPay

### Abstracción
La abstracción en OrbitPay se manifiesta en la capacidad de representar conceptos del dominio real (cuentas, pagos, suscripciones) como objetos en el código. Cada clase abstrae la esencia de su contraparte del mundo real, ocultando los detalles de implementación.

**Aplicación en OrbitPay**:
- `Cuenta` abstrae el concepto de una cuenta de usuario, ocultando cómo se gestiona el saldo internamente
- `Transacción` abstrae el concepto de una operación financiera, sin exponer los mecanismos de validación
- `MetodoPago` es una abstracción pura que define qué es un método de pago sin especificar cómo funciona cada uno

### Encapsulamiento
El encapsulamiento protege el estado interno de los objetos, permitiendo que solo ellos mismos modifiquen sus atributos críticos. Esto garantiza que las reglas de negocio (invariantes) siempre se cumplan.

**Aplicación en OrbitPay**:
- Atributos como `_saldo` en `Cuenta` serán privados, accesibles solo mediante `@property`
- Operaciones que modifican el estado (ej. `retirar()`, `depositar()`) incluirán validaciones
- `Transacción` será inmutable una vez creada, protegiendo la integridad financiera

### Herencia
La herencia permite crear jerarquías de clases, donde las subclases reutilizan y extienden el comportamiento de la clase base.

**Aplicación en OrbitPay**:
- `MetodoPago` (ABC) será la clase base abstracta
- `Tarjeta`, `Transferencia`, `Wallet` heredarán de `MetodoPago`
- Cada subclase implementará su propia lógica de `procesar()` y `validar()`

### Polimorfismo
El polimorfismo permite tratar objetos de diferentes clases de manera uniforme, siempre que compartan una interfaz común.

**Aplicación en OrbitPay**:
- El motor de pagos procesará cualquier objeto que sea `MetodoPago`, sin importar su tipo concreto
- No se usarán `if tipo ==` para determinar el comportamiento
- Cada método de pago sabe cómo procesarse a sí mismo

---

## Dominio Inicial: Clases Candidatas

### 1. Cuenta
**Responsabilidad**: Gestionar el estado financiero de un usuario, incluyendo saldo, transacciones y suscripciones.

**Atributos principales**:
- `id`: Identificador único
- `titular`: Nombre del propietario
- `_saldo`: Monto disponible (protegido)
- `transacciones`: Historial de movimientos

**Métodos principales**:
- `depositar(monto)`: Incrementa el saldo
- `retirar(monto)`: Decrementa el saldo (validando que no quede negativo)
- `consultar_saldo()`: Obtener saldo actual

### 2. Transacción
**Responsabilidad**: Representar un movimiento financiero, garantizando la inmutabilidad y trazabilidad de cada operación.

**Atributos principales**:
- `id`: Identificador único
- `monto`: Cantidad movida
- `tipo`: "ingreso" o "egreso"
- `fecha`: Momento de la transacción
- `descripcion`: Contexto de la operación

**Métodos principales**:
- `__repr__`, `__eq__`, `__lt__`: Métodos dunder para comparación y representación

### 3. Suscripción
**Responsabilidad**: Gestionar servicios recurrentes asociados a una cuenta, incluyendo facturación periódica.

**Atributos principales**:
- `id`: Identificador único
- `nombre`: Descripción de la suscripción
- `monto`: Costo periódico
- `periodicidad`: Mensual, trimestral, anual
- `activa`: Estado actual

**Métodos principales**:
- `renovar()`: Renovar suscripción
- `cancelar()`: Cancelar suscripción
- `calcular_proximo_pago()`: Determinar próxima fecha de cobro

### 4. MetodoPago (Abstracto)
**Responsabilidad**: Definir el contrato para cualquier método de pago que pueda procesarse en el sistema.

**Métodos abstractos**:
- `procesar(monto)`: Ejecutar el pago
- `validar()`: Verificar que el método está en condiciones de ser usado

**Subtipos previstos**:
- `Tarjeta`: Pago con tarjeta de crédito/débito
- `Transferencia`: Pago mediante transferencia bancaria
- `Wallet`: Pago mediante billetera digital

### 5. Engine (Motor de Pagos)
**Responsabilidad**: Orquestar el flujo completo de pago, coordinando los diferentes componentes del sistema.

**Colaboraciones**:
- Usa `Cuenta` para verificar saldo y registrar transacciones
- Usa `MetodoPago` (polimórficamente) para procesar el pago
- Usa estrategias de comisión para calcular costos
- Notifica eventos mediante el patrón Observer

---

## Estructura del Repositorio Inicial
orbitpay-oo/
├── orbitpay/
│ ├── init.py # Exportaciones del paquete
│ └── domain/
│ └── init.py # Módulo de dominio
├── docs/
│ └── 00-fundamentos.md # Este archivo
├── tests/
│ └── init.py
├── spikes/
│ └── init.py
├── pyproject.toml # Configuración del paquete y herramientas
├── README.md # Documentación principal
└── .gitignore # Archivos ignorados por Git

## Verificación de la Fase

Para considerar completada la Fase 1, se debe verificar:

1. ✅ `import orbitpay` funciona (el paquete es importable)
2. ✅ Estructura de archivos según el diagrama
3. ✅ `pyproject.toml` completo con todas las configuraciones
4. ✅ `docs/00-fundamentos.md` con el plan de espiral y dominio inicial
5. ✅ README.md actualizado con el estado del proyecto
6. ✅ Configuración inicial de herramientas de calidad (black, ruff, mypy)

---

## Reflexión Personal

Esta fase establece las bases conceptuales y estructurales del proyecto. La planificación cuidadosa de la espiral es crucial porque cada vuelta construye sobre la anterior, y los riesgos identificados temprano pueden mitigarse antes de que impacten el desarrollo. El dominio inicial con las 5 clases candidatas cubre los aspectos fundamentales del motor de pagos, y la aplicación consciente de los pilares OO desde el diseño garantiza un sistema robusto y mantenible.

La decisión de estructurar el proyecto con un módulo `domain` separado facilita la evolución futura hacia una arquitectura más compleja (ej. hexágono) si es necesario, mientras que el uso de la metodología espiral permite ajustar el curso en cada iteración, absorbiendo el feedback y los aprendizajes del proceso.