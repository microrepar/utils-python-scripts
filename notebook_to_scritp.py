import argparse
import re
import sys
from pathlib import Path

from nbconvert.exporters.script import ScriptExporter

# print('>>>>>>>>>>>>>>>>>>', sys.executable)
# BEGIN SPINNER_THREAD
import threading
import itertools
import time


DELAY = .1  # seconds


def spin(msg, computation):  # <1>
    for i, char in enumerate(itertools.cycle('⠇⠋⠙⠸⠴⠦')):  # <3>
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        if computation.wait(DELAY):  # <5>
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')


def convert_notebooks_to_scripts(notebook_list):
    arquivos_convertidos = list()
    exporter = ScriptExporter()
    for i, notebook in enumerate(notebook_list, 1):
        notebook_path = Path(notebook)
        base = notebook_path.stem
        output_script = notebook_path.parent / ('script_' + str(i).zfill(3) + '_' + base + '.py')  # Formata o número do prefixo
        arquivos_convertidos.append(f"{notebook_path.name} | to -> {output_script.name}")
        output, resources = exporter.from_filename(notebook)

        # Substitui o método display por print no script convertido
        output_with_replacement = re.sub(r'(^|\b)display\(', '\\1print(', output)
       
        # Comenta todas as chamadas de dfSummary() no script convertido
        output_with_comments = re.sub(r'(^|.+|\b)dfSummary\((\)|[^)]+\))', r'# \g<0>', output_with_replacement)
       
        # Comenta todas as chamadas de %matplotlib no script convertido
        # Adicionando comentário à linha com %matplotlib inline
        output_with_comments = re.sub(r'(^|\s*)%matplotlib inline', r'# %matplotlib inline', output_with_comments)

        # Comenta todas as chamadas de get_ipython().run_line_magic() no script convertido
        output_with_comments = re.sub(r'get_ipython\(\)\.run_line_magic\([^)]+\)', '# \\g<0>', output_with_comments)

        # Especifica a codificação ao abrir o arquivo para escrita
        with open(output_script, 'w', encoding='utf-8') as f:
            f.write(output_with_comments)
    return arquivos_convertidos


def supervisor(diretorio_atual):
    print("Diretório de conversão:", diretorio_atual)
    
    computation = threading.Event()
    spinner = threading.Thread(target=spin,
                               args=('Converting!', computation))
    spinner.start()  # <11>
    
    # Lista de notebooks a serem convertidos
    notebooks = [p for p in Path(diretorio_atual).glob('*.ipynb') if not p.name.startswith('_')]

    # Executa a conversão
    result = convert_notebooks_to_scripts(notebooks)

    computation.set()  # <13>
    spinner.join()  # <14>
    return result


if __name__ == "__main__":
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Script para converter notebooks jupyter para scripts.')

    # Define o argumento para o diretório
    parser.add_argument('diretorio', type=str, help='Diretório a ser passado como argumento. Use "." para o diretório atual.')

    # Faz o parse dos argumentos da linha de comando
    args = parser.parse_args()

    # Obtém o diretório atual usando Pathlib
    diretorio_atual = str(Path.cwd()) if args.diretorio == "." else args.diretorio

    # Chama a função main com o diretório passado como argumento
    result = supervisor(diretorio_atual)
    for r in result:
        time.sleep(.1)
        print(r)
    print(f"{' ' + str(len(result))+' NOTEBOOKS CONVERTIDOS PARA SCRIPTS ':*^50}")
