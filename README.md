# Conversor de MP3 para PCM 🎵

Uma ferramenta simples e rápida desenvolvida em Python para converter lotes de arquivos de áudio `.mp3` para o formato bruto `.pcm` (RAW PCM), ideal para sistemas de telefonia, telemetria e hardwares embarcados.

## O que a ferramenta faz?
Ela transforma um arquivo `.zip` contendo áudios MP3 em um novo `.zip` com os áudios já convertidos e padronizados com as seguintes especificações:
- **Formato:** RAW PCM (`.pcm`)
- **Canais:** Mono
- **Taxa de Amostragem (Sample Rate):** 16000 Hz
- **Profundidade (Bit Depth):** 16-bit Signed (s16le)

## Como usar

1. Certifique-se de ter o **Python** instalado em sua máquina.
2. Instale as bibliotecas necessárias rodando no terminal:
   ```bash
   pip install streamlit imageio-ffmpeg
   ```
3. Inicie o aplicativo executando:
   ```bash
   streamlit run app_conversor.py
   ```
4. O seu navegador abrirá automaticamente. Basta arrastar o seu arquivo `.zip` com os MP3 para a tela, processar e baixar o resultado!