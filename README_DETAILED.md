# Conversor Avançado de MP3 para PCM 🚀

Este projeto é uma aplicação web local construída com **Streamlit** que automatiza a conversão de arquivos de áudio para hardwares embarcados e sistemas de telefonia. 

Ele substitui fluxos de trabalho manuais complexos (como usar o *Audacity* para ajustar taxas de amostragem + *360converter* para remover cabeçalhos), realizando todo o processo em segundos através de processamento em lote (arquivos `.zip`).

## ⚙️ Especificações Técnicas do Áudio de Saída

Os arquivos gerados (`.pcm`) atendem rigorosamente aos seguintes parâmetros industriais:
* **Remoção de Cabeçalho (Headerless):** Gera RAW PCM puro, sem encapsulamento RIFF/WAV.
* **Canais (Channels):** Convertido de Estéreo para **Mono**, reduzindo pela metade o tamanho do arquivo final.
* **Sample Rate:** **16000 Hz** (16 kHz).
* **Codec/Codificação:** **16-bit Signed Little-Endian** (`pcm_s16le`).

## 🛠️ Tecnologias Utilizadas

* **Python 3+**: Linguagem base.
* **Streamlit**: Para renderização da interface web interativa.
* **FFmpeg (via `imageio-ffmpeg`)**: Motor de processamento de áudio. A utilização desta biblioteca específica garante que o binário do FFmpeg seja baixado e embutido automaticamente, eliminando a necessidade de configurar variáveis de ambiente (PATH) no Windows.
* **Bibliotecas Nativas (`os`, `zipfile`, `tempfile`, `subprocess`)**: Para manipulação segura de arquivos, garantindo que o disco não seja preenchido com resíduos após a conversão.

## 🚀 Instalação e Configuração

### 1. Pré-requisitos
* Python instalado (Recomenda-se adicionar o Python e a pasta Scripts ao `PATH` do sistema).

### 2. Instalação das Dependências
Abra o seu terminal (CMD ou PowerShell) na pasta do projeto e execute:
```bash
pip install streamlit imageio-ffmpeg
```
*(Nota: Se o comando `pip` não for reconhecido ou for bloqueado pela Microsoft Store, utilize o caminho absoluto do seu executável Python, como: `C:\Caminho\Para\O\Python\python.exe -m pip install streamlit imageio-ffmpeg`)*

### 3. Executando o Aplicativo
Inicie o servidor local do Streamlit com o comando:
```bash
streamlit run app_conversor.py
```

## 💡 Como Funciona (Under the hood)

O coração da conversão utiliza uma chamada `subprocess` diretamente ao FFmpeg com a seguinte flag estrutural:
`ffmpeg -y -i <entrada.mp3> -f s16le -ac 1 -ar 16000 -acodec pcm_s16le <saida.pcm>`

1. O usuário faz upload do ZIP;
2. O aplicativo extrai o conteúdo para um diretório temporário invisível;
3. O FFmpeg é acionado para cada arquivo iterativamente;
4. O resultado é zipado e devolvido via download;
5. O diretório temporário é apagado automaticamente para manter o sistema limpo.