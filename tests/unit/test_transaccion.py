"""Pruebas unitarias para la clase Transaccion."""

import pytest
from datetime import datetime

from orbitpay.domain import Transaccion


class TestTransaccion:
    """Pruebas para la clase Transaccion."""
    
    def test_creacion_transaccion_valida(self):
        """Probar creación de transacción válida."""
        transaccion = Transaccion(
            id="test-1",
            monto=100.0,
            tipo="ingreso",
            fecha=datetime.now(),
            descripcion="Test",
            estado="completada"
        )
        
        assert transaccion.id == "test-1"
        assert transaccion.monto == 100.0
        assert transaccion.tipo == "ingreso"
        assert transaccion.estado == "completada"
    
    def test_transaccion_monto_negativo(self):
        """Probar que no se puede crear transacción con monto negativo."""
        with pytest.raises(ValueError, match="monto debe ser positivo"):
            Transaccion(
                id="test-2",
                monto=-100.0,
                tipo="ingreso",
                fecha=datetime.now(),
                descripcion="Test",
                estado="completada"
            )
    
    def test_transaccion_tipo_invalido(self):
        """Probar que no se puede crear transacción con tipo inválido."""
        with pytest.raises(ValueError, match="Tipo inválido"):
            Transaccion(
                id="test-3",
                monto=100.0,
                tipo="invalido",
                fecha=datetime.now(),
                descripcion="Test",
                estado="completada"
            )
    
    def test_transaccion_estado_invalido(self):
        """Probar que no se puede crear transacción con estado inválido."""
        with pytest.raises(ValueError, match="Estado inválido"):
            Transaccion(
                id="test-4",
                monto=100.0,
                tipo="ingreso",
                fecha=datetime.now(),
                descripcion="Test",
                estado="invalido"
            )
    
    def test_transaccion_inmutable(self):
        """Probar que Transacción es inmutable."""
        transaccion = Transaccion(
            id="test-5",
            monto=100.0,
            tipo="ingreso",
            fecha=datetime.now(),
            descripcion="Test",
            estado="completada"
        )
        
        with pytest.raises(AttributeError):
            transaccion.monto = 200.0
    
    def test_transaccion_repr(self):
        """Probar representación de transacción."""
        fecha = datetime(2026, 1, 1, 12, 0)
        transaccion = Transaccion(
            id="test-6",
            monto=100.0,
            tipo="ingreso",
            fecha=fecha,
            descripcion="Test",
            estado="completada"
        )
        
        repr_str = repr(transaccion)
        assert "Transaccion" in repr_str
        assert "100.00" in repr_str
        assert "ingreso" in repr_str
    
    def test_transaccion_eq(self):
        """Probar comparación de transacciones."""
        fecha = datetime.now()
        t1 = Transaccion("eq-1", 100.0, "ingreso", fecha, "Test1", "completada")
        t2 = Transaccion("eq-1", 200.0, "egreso", fecha, "Test2", "completada")
        t3 = Transaccion("eq-2", 100.0, "ingreso", fecha, "Test3", "completada")
        
        assert t1 == t2  # Mismo ID
        assert t1 != t3  # Diferente ID
        assert t1 != "otra_cosa"
    
    def test_transaccion_lt(self):
        """Probar ordenamiento de transacciones por monto."""
        fecha = datetime.now()
        t1 = Transaccion("lt-1", 50.0, "ingreso", fecha, "Test1", "completada")
        t2 = Transaccion("lt-2", 150.0, "ingreso", fecha, "Test2", "completada")
        t3 = Transaccion("lt-3", 100.0, "ingreso", fecha, "Test3", "completada")
        
        transacciones = [t1, t2, t3]
        ordenadas = sorted(transacciones)
        
        assert ordenadas == [t1, t3, t2]  # 50, 100, 150
    
    def test_transaccion_hash(self):
        """Probar que Transacción se puede usar como clave de diccionario."""
        fecha = datetime.now()
        t1 = Transaccion("hash-1", 100.0, "ingreso", fecha, "Test1", "completada")
        
        # Usar como clave de diccionario
        diccionario = {t1: "valor"}
        assert diccionario[t1] == "valor"