import os
import PySimpleGUI as sg
import ghostscript
import shutil

def encontrar_diretorio_ghostscript():
    """Função para encontrar o diretório do executável do Ghostscript."""
    # Lista de possíveis nomes de executáveis do Ghostscript
    nomes_ghostscript = ['gs', 'gswin32', 'gswin64']

     # Iterar sobre cada nome na lista de possíveis executáveis
    for nome_ghostscript in nomes_ghostscript:
        # Verificar se o executável está disponível no PATH do sistema
        diretorio_ghostscript = shutil.which(nome_ghostscript)

        # Se encontrado, retornar o caminho completo do executável
        if diretorio_ghostscript:
            return diretorio_ghostscript

    # Se nenhum executável for encontrado, levanta uma exceção com uma mensagem de erro
    raise FileNotFoundError(
        f"Nenhum executável do GhostScript foi encontrado ({'/'.join(nomes_ghostscript)})"
    )

def comprimir_pdf(caminho_entrada, caminho_saida, qualidade='printer'):
    """Função para comprimir um PDF usando a biblioteca Ghostscript do Python."""

    # Encontrar o executável do Ghostscript
    gs = encontrar_diretorio_ghostscript()

    tamanho_inicial = os.path.getsize(caminho_entrada)

    args = [
        gs,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{qualidade}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={caminho_saida}",
        caminho_entrada
    ]

    try:
        # Executa o Ghostscript através da API Python
        ghostscript.Ghostscript(*args)

        tamanho_final = os.path.getsize(caminho_saida)
        razao = 1 - (tamanho_final / tamanho_inicial)

        return caminho_saida, razao, tamanho_final / 1000000
    except ghostscript.GhostscriptError as e:
        sg.popup_error(f'Erro ao compilar o PDF: {e}')
        return None, None, None

def criar_interface():
    """Função para criar a interface gráfica."""
    layout = [
        [sg.Text('Arquivo PDF de entrada:'), sg.InputText(key='caminho_entrada'), sg.FileBrowse(file_types=(('PDF Files', '*.pdf'),))],
        [sg.Text('Arquivo PDF de saída (opcional):'), sg.InputText(key='caminho_saida'), sg.FileSaveAs(file_types=(('PDF Files', '*.pdf'),))],
        [sg.Text('Qualidade de compressão:'), sg.Combo(['screen', 'ebook', 'printer', 'prepress', 'default'], default_value='printer', key='qualidade')],
        [sg.Button('Comprimir PDF'), sg.Button('Cancelar')]
    ]

    janela = sg.Window('Compressor de PDF', layout)

    while True:
        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED or evento == 'Cancelar':
            break
        elif evento == 'Comprimir PDF':
            caminho_entrada = valores['caminho_entrada']
            caminho_saida = valores['caminho_saida']
            qualidade = valores['qualidade']

            if not caminho_entrada or not os.path.isfile(caminho_entrada):
                sg.popup_error(f'Erro: "{caminho_entrada}" não é um arquivo ou não existe.')
                continue

            if not caminho_entrada.lower().endswith('.pdf'):
                sg.popup_error(f'Erro: "{caminho_entrada}" não é um arquivo PDF.')
                continue

            if not caminho_saida:
                dir_entrada = os.path.dirname(caminho_entrada)
                nome_arquivo_saida = os.path.splitext(os.path.basename(caminho_entrada))[0] + '_comprimido.pdf'
                caminho_saida = os.path.join(dir_entrada, nome_arquivo_saida)
            else:
                dir_saida = os.path.dirname(os.path.abspath(caminho_saida))
                if not os.path.isdir(dir_saida):
                    sg.popup_error(f'Erro: o diretório de saída "{dir_saida}" não existe.')
                    continue

                if not caminho_saida.lower().endswith('.pdf'):
                    sg.popup_error(f'Erro: o arquivo de saída "{caminho_saida}" deve ter extensão ".pdf".')
                    continue

                if os.path.abspath(caminho_entrada) == os.path.abspath(caminho_saida):
                    sg.popup('Aviso', 'O arquivo de saída é o mesmo que o arquivo de entrada. Alterando o nome do arquivo de saída.')
                    nome_arquivo_saida = os.path.splitext(os.path.basename(caminho_saida))[0] + '_comprimido.pdf'
                    caminho_saida = os.path.join(dir_saida, nome_arquivo_saida)

            caminho, razao, tamanho_final = comprimir_pdf(caminho_entrada, caminho_saida, qualidade)
            if caminho:
                sg.popup('Sucesso', f'PDF comprimido com sucesso: {caminho}\n'
                                    f'Compressão de {razao:.0%}\n'
                                    f'Tamanho final do arquivo é {tamanho_final:.5f} MB.')
            else:
                sg.popup_error('Falha ao comprimir o PDF.')

    janela.close()

if __name__ == '__main__':
    criar_interface()