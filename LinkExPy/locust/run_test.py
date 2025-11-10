import subprocess
import time
from datetime import datetime
import os
import signal
import sys

def run_load_test(duration_seconds=60, users=10):
    """
    Executa o teste de carga com o Locust via linha de comando
    
    Args:
        duration_seconds: Duração do teste em segundos (default: 60s = 1min)
        users: Número de usuários simultâneos (default: 50)
    """
    # Cria diretório para resultados se não existir
    results_dir = "test_results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Nome do arquivo baseado na data/hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_base = f"results_{timestamp}"
    csv_stats = os.path.join(results_dir, f"{csv_base}_stats.csv")
    csv_history = os.path.join(results_dir, f"{csv_base}_history.csv")
    
    try:
        # Comando do Locust para executar o teste headless (sem interface web)
        cmd = [
            "docker-compose", "run", "--rm",
            "-e", f"LOCUST_USERS={users}",
            "-e", f"LOCUST_RUN_TIME={duration_seconds}s",
            "locust",
            "--headless",
            "--host", "http://web",
            "--csv", csv_base,  # Locust adiciona _stats e _history automaticamente
            "--csv-full-history"
        ]
        
        print(f"\nIniciando teste de carga:")
        print(f"- Usuários: {users}")
        print(f"- Duração: {duration_seconds}s")
        print("\nResultados serão salvos em:")
        print(f"- Estatísticas: {csv_stats}")
        print(f"- Histórico: {csv_history}")
        
        # Executa o comando
        process = subprocess.Popen(cmd)
        
        # Aguarda o término do teste
        process.wait()
        
        if process.returncode == 0:
            print("\nTeste concluído com sucesso!")
            print(f"Resultados salvos em: {results_dir}/")
        else:
            print("\nErro ao executar o teste")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nTeste interrompido pelo usuário")
        process.send_signal(signal.SIGINT)
        sys.exit(1)

if __name__ == "__main__":
    # Parâmetros do teste
    DURATION = 60    # 1 minuto
    USERS = 50       # 50 usuários simultâneos
    
    run_load_test(
        duration_seconds=DURATION,
        users=USERS
    )