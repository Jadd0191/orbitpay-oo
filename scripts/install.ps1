# scripts/install.ps1
# Script de instalación para Windows

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🚀 ORBITPAY OO - INSTALACIÓN" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# 1. Verificar Python
Write-Host "`n📋 1. Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python no encontrado. Instala Python 3.11 o superior." -ForegroundColor Red
    exit 1
}
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# 2. Crear entorno virtual
Write-Host "`n📋 2. Creando entorno virtual..." -ForegroundColor Yellow
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al crear entorno virtual" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Entorno virtual creado" -ForegroundColor Green

# 3. Activar entorno virtual
Write-Host "`n📋 3. Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✅ Entorno virtual activado" -ForegroundColor Green

# 4. Instalar dependencias
Write-Host "`n📋 4. Instalando dependencias..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al instalar dependencias" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencias instaladas" -ForegroundColor Green

# 5. Ejecutar pruebas
Write-Host "`n📋 5. Ejecutando pruebas..." -ForegroundColor Yellow
python -m pytest tests/ -v --cov=orbitpay --cov-report=term
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Pruebas fallidas" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Todas las pruebas pasaron" -ForegroundColor Green

# 6. Ejecutar demo
Write-Host "`n📋 6. Ejecutando demo..." -ForegroundColor Yellow
python scripts/demo_completa.py

Write-Host "`n" + "=" * 70 -ForegroundColor Cyan
Write-Host "✅ INSTALACIÓN COMPLETADA EXITOSAMENTE" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "`nPara activar el entorno virtual: .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "Para ejecutar las pruebas: pytest" -ForegroundColor Yellow
Write-Host "Para ejecutar la demo: python scripts/demo_completa.py" -ForegroundColor Yellow