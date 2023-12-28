import argparse
import itertools
import multiprocessing
import os
import subprocess
import sys
import time
from pathlib import Path

DELAY = .1  # seconds

def spin(msg, computation):  # <1>
    for char in itertools.cycle('⠇⠋⠙⠸⠴⠦'):  # <3>
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        if computation.wait(DELAY):  # <5>
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')


def execute_converted_notebooks(directory):
    os.chdir(directory)
    directory_path = Path(os.getcwd())
    for script in directory_path.glob('*.py'):
        if not script.name.startswith('script_'): continue
        print(f">>>>>{script.name}")
        try:
            # Executa o script usando o interpretador Python
            subprocess.run([sys.executable, str(script)], check=True)   # Adicione check=True para verificar se houve erro
        except subprocess.CalledProcessError as e:
            return f"Error executing {script}: {e}"


def supervisor():  # <9>
    computation = multiprocessing.Event()
    spinner = multiprocessing.Process(target=spin,
                               args=('Executing!', computation))
    print('spinner object:', spinner)  # <10>
    spinner.start()  # <11>

    computation.set()  # <13>
    spinner.join()  # <14>
   


if __name__ == "__main__":
    try:
        computation = multiprocessing.Event()
        spinner = multiprocessing.Process(target=spin,
                                args=('thinking!', computation))
        print('spinner object:', spinner)  # <10>
        spinner.start()  # <11>


        # Configura o parser de argumentos
        parser = argparse.ArgumentParser(description='Script para executar os scripts convertidos.')

        # Define o argumento para o diretório
        parser.add_argument('diretorio', type=str, help='Diretório a ser passado como argumento. Use "." para o diretório atual.')

        # Faz o parse dos argumentos da linha de comando
        args = parser.parse_args()

        # Obtém o diretório atual usando Pathlib
        diretorio_atual = str(Path.cwd()) if args.diretorio == "." else args.diretorio
        
        # Executa os notebooks convertidos no diretório
        result = execute_converted_notebooks(diretorio_atual)


        if result is None:
            print(f"{'SUCESSO NA OPERACAO':*^50}")
        else:
            print(f"{str(result):*^50}")
    finally:
        computation.set()  # <13>
        spinner.join()  # <14>   