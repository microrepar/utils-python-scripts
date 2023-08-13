import subprocess
import argparse
from pathlib import Path
import sys

def execute_converted_notebooks(directory):
    directory_path = Path(directory)
    for script in directory_path.glob('*.py'):
        if not script.name.startswith('script_'): continue
        print(f">>>>>>Executing... ->{script.name}")
        try:
            # Executa o script usando o interpretador Python
            subprocess.run([r'C:\ProgramData\anaconda3\python.exe', str(script)], check=True)  # Adicione check=True para verificar se houve erro
        except subprocess.CalledProcessError as e:
            print(f"Error executing {script}: {e}")
            sys.exit(1)  # Sai do script imediatamente em caso de erro


if __name__ == "__main__":
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Script para executar os scripts convertidos.')

    # Define o argumento para o diretório
    parser.add_argument('diretorio', type=str, help='Diretório a ser passado como argumento. Use "." para o diretório atual.')

    # Faz o parse dos argumentos da linha de comando
    args = parser.parse_args()

    # Obtém o diretório atual usando Pathlib
    diretorio_atual = str(Path.cwd()) if args.diretorio == "." else args.diretorio
    
    # Executa os notebooks convertidos no diretório
    execute_converted_notebooks(diretorio_atual)

    print(f"{'SUCESSO NA OPERACAO':*^50}")