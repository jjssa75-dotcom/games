$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (Get-Command py -ErrorAction SilentlyContinue) {
    py -m tactical_rpg.web
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    python -m tactical_rpg.web
} else {
    $asterraRuntime = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $asterraRuntime) {
        & $asterraRuntime -m tactical_rpg.web
    } else {
        Write-Error 'Python 3.11 ou superior não foi encontrado.'
    }
}
