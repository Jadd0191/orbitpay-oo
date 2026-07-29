# Fase 4: Encapsulamiento e Invariantes

## 1. Estrategia de Encapsulamiento

### Atributos Protegidos
- `Cuenta._saldo`: Protegido con `_` para indicar que es interno
- Acceso solo mediante `@property`
- Modificación solo mediante métodos `depositar()` y `retirar()`

### Validaciones (Invariantes)

#### Cuenta
- `_saldo` nunca es negativo (validado en `retirar()`)
- `titular` no está vacío
- `_saldo` inicial no es negativo

#### Transacción
- `monto` siempre es positivo (validado en `__post_init__`)
- `tipo` es "ingreso" o "egreso"
- `estado` es "pendiente", "completada" o "fallida"
- Objeto inmutable (`frozen=True`)

#### Suscripción
- `monto` siempre es positivo
- `periodicidad` es válida
- `fecha_fin` > `fecha_inicio` si existe

## 2. Métodos Dunder Implementados

### `__repr__()`
Proporciona representación legible para debugging.

```python
>>> cuenta = Cuenta("123", "Juan Perez", _saldo=1000.0)
>>> cuenta
Cuenta(id='123...', titular='Juan Perez', saldo=$1000.00, transacciones=0, suscripciones=0)