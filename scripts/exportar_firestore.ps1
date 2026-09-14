# Exporta as colecoes do Firestore pedindo a credencial de membro do portal de forma segura
# (senha mascarada; fica so na memoria do processo e e apagada ao final).
#
#   powershell -ExecutionPolicy Bypass -File scripts/exportar_firestore.ps1

$raiz = Split-Path -Parent $PSScriptRoot
Set-Location $raiz

$email = Read-Host "E-mail de membro do portal (o mesmo do login)"
$senhaSegura = Read-Host "Senha (nao aparece enquanto digita)" -AsSecureString
$senha = [Runtime.InteropServices.Marshal]::PtrToStringBSTR(
  [Runtime.InteropServices.Marshal]::SecureStringToBSTR($senhaSegura))

try {
  $env:FB_EMAIL = $email.Trim()
  $env:FB_SENHA = $senha
  node scripts/exportar_firestore.mjs
  if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Exportacao concluida. Pode avisar o Claude." -ForegroundColor Green
  }
} finally {
  Remove-Item Env:FB_SENHA -ErrorAction SilentlyContinue
  Remove-Item Env:FB_EMAIL -ErrorAction SilentlyContinue
  $senha = $null
}