# Tarjeta CRC: MetodoPago (Abstracto)

## Clase
**MetodoPago** (ABC)

## Responsabilidades
1. Definir interfaz para procesar pagos
2. Establecer contrato de validación
3. Garantizar polimorfismo

## Colaboradores
1. **Tarjeta**: Implementación concreta
2. **Transferencia**: Implementación concreta
3. **Wallet**: Implementación concreta
4. **Engine**: Usa el método de pago para procesar
5. **Factory**: Crea instancias concretas