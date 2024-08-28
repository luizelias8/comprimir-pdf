# Compressor de PDFs com Ghostscript e PySimpleGUI

## Funcionalidades

- **Compressão de PDFs**: O script utiliza Ghostscript para reduzir o tamanho de arquivos PDF, mantendo a qualidade ajustada conforme necessário.
- **Interface Gráfica**: Fácil de usar, permite a seleção de arquivos e configuração de opções de compressão.
- **Configurações de Qualidade**: Permite escolher entre diferentes níveis de qualidade como `screen`, `ebook`, `printer`, `prepress` e `default`.
- **Detecção Automática do Ghostscript**: O script localiza automaticamente o executável do Ghostscript no sistema.

## Requisitos

- Python 3.6 ou superior
- [Ghostscript](https://www.ghostscript.com/) instalado no sistema
- Bibliotecas Python: `PySimpleGUI`, `ghostscript`, `shutil`

## Instalação

Clone o repositório e instale as dependências necessárias:

```
git clone https://github.com/luizelias8/comprimir-pdf.git
cd comprimir-pdf
pip install -r requirements.txt
```

## Uso

Execute o script principal para abrir a interface gráfica:

```
python comprimir_pdf.py
```

## Contribuição

Contribuições são bem-vindas!

## Autor

- [Luiz Elias](https://github.com/luizelias8)