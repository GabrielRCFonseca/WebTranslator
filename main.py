import os
import time
from google_trans_new import google_translator
from bs4 import BeautifulSoup


def traduz_arquivo_html(arquivo_entrada, limite_caracteres):

    # Checks if the file has already been translated to Hindi
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        conteudo = f.read()
        if 'lang="hi"' in conteudo:
            print(f"Arquivo {arquivo_entrada} já traduzido para hindi. Pulando para o próximo arquivo.")
            return

    # Initializes the translator
    tradutor = google_translator(timeout=90)

    # Opens the input HTML file and loads the content into a string
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Parses the HTML content
    soup = BeautifulSoup(conteudo, 'html.parser')

    # Splits the content into chunks of up to character_limit characters
    trechos = [str(tag.string) for tag in soup.find_all(string=True) if not tag.parent.name in ['script', 'style', 'link']]
    trechos = [trecho for trecho in trechos if not trecho.startswith("<script") and not trecho.startswith("<style") and not trecho.startswith("<link")]
    trechos = [trecho for trecho in trechos if len(trecho.strip()) > 0] # Ignores empty chunks

    # Translates each chunk and replaces the tag's content with the translated content
    for i, trecho in enumerate(trechos):
        try:
            traducao = tradutor.translate(trecho, lang_tgt='hi')
            # Creates a new tag with the translated content
            tag_traduzida = soup.new_tag("span")
            tag_traduzida.string = traducao
            # Replaces the original tag's content with the translated content
            soup.find_all(string=trecho)[0].replace_with(tag_traduzida)
            # Waits for one second before making the next translation request
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao traduzir {arquivo_entrada}: {e}")

    # Writes the file with the translated content
    with open(arquivo_entrada, 'w', encoding="utf-8") as f:
        f.write(str(soup))

    # Checks the content of the file after translation
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        conteudo_traduzido = f.read()
        print(f"Conteúdo traduzido de {arquivo_entrada}:")
        print(conteudo_traduzido)


if __name__ == '__main__':
    # Sets the input folder path
    pasta_entrada = r'C:\My Web Sites\Nova pasta'

    # Recursively goes through the input folder and translates any HTML files found.
    for raiz, diretorios, arquivos in os.walk(pasta_entrada):
        for arquivo in arquivos:
            if arquivo.endswith('.html'):
                caminho_entrada = os.path.join(raiz, arquivo)

                traduz_arquivo_html(caminho_entrada, limite_caracteres=4997)