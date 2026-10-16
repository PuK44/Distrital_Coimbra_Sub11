import os
import sys

def iniciar_aplicacao():
    caminho_interface = os.path.join("src", "interface.py")
    
    if not os.path.exists(caminho_interface):
        print(f"Erro: O ficheiro '{caminho_interface}' não foi encontrado!")
        sys.exit(1)

    print("A iniciar a aplicação no navegador...")
    # Define a diretoria raiz no PYTHONPATH antes de lançar o Streamlit
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(".")
    
    os.system(f"streamlit run {caminho_interface}")

if __name__ == "__main__":
    iniciar_aplicacao()