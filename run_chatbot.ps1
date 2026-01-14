Write-Host "=== Setup e execução do LLM Module ===`n"

# -----------------------------
# Verifica uv
# -----------------------------
$uvExists = Get-Command uv -ErrorAction SilentlyContinue

if (-not $uvExists) {
    Write-Host "uv não encontrado. Tentando instalar via pipx..."

    $pipxExists = Get-Command pipx -ErrorAction SilentlyContinue
    if (-not $pipxExists) {
        Write-Error "pipx não está instalado. Instale pipx antes de continuar."
        exit 1
    }

    pipx install uv

    # Verifica se ollama existe antes de usar
    if (Get-Command ollama -ErrorAction SilentlyContinue) {
        Write-Host "Baixando modelo qwen2.5:7B..."
        ollama pull qwen2.5:7B
    } else {
        Write-Warning "Ollama não encontrado. Pulei o download do modelo."
    }
} else {
    Write-Host "uv encontrado."
}

# -----------------------------
# Caminho do projeto (portável)
# -----------------------------
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$projectPath   = Join-Path $documentsPath "gestock\llm_module"

if (-not (Test-Path $projectPath)) {
    Write-Error "Projeto não encontrado em: $projectPath"
    exit 1
}

Set-Location $projectPath
Write-Host "Diretório do projeto: $projectPath"

# -----------------------------
# Sincroniza dependências
# -----------------------------
Write-Host "`nRodando uv sync..."
uv sync

# -----------------------------
# Executa o chatbot
# -----------------------------
$venvPython = Join-Path $projectPath ".venv\Scripts\python.exe"
$scriptPath = Join-Path $projectPath "src\llm_module\models\chatbot.py"

if (-not (Test-Path $venvPython)) {
    Write-Error "Python da virtualenv não encontrado. uv sync falhou?"
    exit 1
}

if (-not (Test-Path $scriptPath)) {
    Write-Error "Script chatbot.py não encontrado."
    exit 1
}

Write-Host "`nExecutando chatbot..."
& $venvPython $scriptPath

Write-Host "`nExecução concluída com sucesso."
