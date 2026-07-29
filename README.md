## Prototipos (Spikes)

Los prototipos en `spikes/` validan decisiones críticas de arquitectura:

- **`atomicidad_transaccion.py`**: Demuestra que las transacciones son atómicas (riesgo de doble cobro)
- **`validacion_saldo.py`**: Valida que el saldo nunca quede negativo (integridad de datos)
- **`polimorfismo_pagos.py`**: Demuestra el procesamiento polimórfico sin condicionales (desacoplamiento)

Ejecutar prototipos:
```bash
python spikes/atomicidad_transaccion.py
python spikes/validacion_saldo.py
python spikes/polimorfismo_pagos.py


---

### Paso 5: Subir a GitHub con Tag

```powershell
# 1. Verificar estado
git status

# 2. Añadir todos los archivos
git add .

# 3. Commit
git commit -m "Fase 3: Análisis de Riesgos - Prototipado y Arquitectura

- docs/02-riesgos.md con registro de riesgos y ADR
- Prototipos: atomicidad_transaccion.py, validacion_saldo.py, polimorfismo_pagos.py
- Validación de riesgos críticos: doble cobro, saldo inconsistente, acoplamiento
- README actualizado con sección de prototipos"

# 4. Actualizar versión en __init__.py a 0.3.0
# (Edita orbitpay/__init__.py)

# 5. Commit de la versión
git add orbitpay/__init__.py
git commit -m "chore: actualizar versión a 0.3.0"

# 6. Crear tag
git tag -a v0.3.0 -m "Fase 3: Análisis de Riesgos - Prototipado y Arquitectura"

# 7. Subir todo
git push origin main
git push origin v0.3.0