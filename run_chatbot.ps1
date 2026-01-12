# Verifica se uv está instalado
$uvExists = Get-Command uv -ErrorAction SilentlyContinue

if (-not $uvExists) {
    Write-Host "uv não encontrado. Instalando via pipx..."

    # Verifica se pipx existe
    $pipxExists = Get-Command pipx -ErrorAction SilentlyContinue
    if (-not $pipxExists) {
        Write-Error "pipx não está instalado. Instale pipx antes de continuar."
        exit 1
    }

    pipx install uv
} else {
    Write-Host "uv encontrado."
}

# Caminho do projeto
$projectPath = "C:\Users\Callidus\Documents\GitHub\gestock\llm_module"

Set-Location $projectPath

# Sincroniza dependências
Write-Host "Rodando uv sync..."
uv sync

# Executa o script Python usando a venv criada pelo uv
$pythonPath = "$projectPath\.venv\Scripts\python.exe"
$scriptPath = "$projectPath\src\llm_module\models\chatbot.py"

Write-Host "Executando chatbot..."
& $pythonPath $scriptPath
Write-Host "Execução concluída."