# Script de inicialização do ENERGYX Dashboard
Write-Host "Iniciando ENERGYX Dashboard..." -ForegroundColor Cyan
Set-Location $PSScriptRoot
& .\.venv\Scripts\Activate.ps1

Write-Host "Abrindo navegador em 6 segundos..." -ForegroundColor Yellow

# Iniciar Streamlit em background
Start-Job -ScriptBlock { 
    Set-Location $using:PSScriptRoot
    & .\.venv\Scripts\python.exe -m streamlit run app.py 
} | Out-Null

# Aguardar inicialização
Start-Sleep -Seconds 6

# Abrir navegador
Start-Process "http://localhost:8501"

Write-Host "`nDashboard aberto no navegador!" -ForegroundColor Green
Write-Host "Pressione qualquer tecla para fechar o dashboard..." -ForegroundColor Cyan

$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

# Parar jobs ao fechar
Get-Job | Stop-Job
Get-Job | Remove-Job
