import sys
import os

# 1. Adicionar o caminho raiz para garantir que encontra o pacote 'src'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# 2. Executar diretamente o ficheiro de interface gráfica
caminho_interface = os.path.join(os.path.dirname(__file__), "src", "interface.py")

with open(caminho_interface, encoding="utf-8") as f:
    code = compile(f.read(), caminho_interface, 'exec')
    exec(code, globals())