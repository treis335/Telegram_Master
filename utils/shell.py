import subprocess

def run_cmd(cmd: str) -> str:
    """Executa comando shell e retorna output (stdout+stderr)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "Comando demorou demasiado tempo."
    except Exception as e:
        return f"Erro: {e}"