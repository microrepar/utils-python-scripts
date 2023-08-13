import argparse
import re
import sys
from pathlib import Path

from nbconvert.exporters.script import ScriptExporter

# print('>>>>>>>>>>>>>>>>>>', sys.executable)


def convert_notebooks_to_scripts(notebook_list):
    exporter = ScriptExporter()
    for i, notebook in enumerate(notebook_list, 1):
        notebook_path = Path(notebook)
        base = notebook_path.stem
        output_script = notebook_path.parent / ('script_' + str(i).zfill(3) + '_' + base + '.py')  # Formata o número do prefixo
        print(f">>>>>>>>>>Converting {notebook_path.name} | to -> {output_script.name}")
        output, resources = exporter.from_filename(notebook)

       # Substitui o método display por print no script convertido
        output_with_replacement = re.sub(r'(^|\b)display\(', '\\1print(', output)

        # Comenta todas as chamadas de get_ipython().run_line_magic() no script convertido
        output_with_comments = re.sub(r'get_ipython\(\)\.run_line_magic\([^)]+\)', '# \\g<0>', output_with_replacement)

        # Especifica a codificação ao abrir o arquivo para escrita
        with open(output_script, 'w', encoding='utf-8') as f:
            f.write(output_with_comments)


def main(diretorio_atual):
    print("Diretório passado como argumento:", diretorio_atual)
    
    # Lista de notebooks a serem convertidos
    notebooks = [p for p in Path(diretorio_atual).glob('*.ipynb') if not p.name.startswith('__')]

    # Executa a conversão
    convert_notebooks_to_scripts(notebooks)


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
    main(diretorio_atual)

