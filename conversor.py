import streamlit as st
import zipfile
import os
import subprocess
import tempfile
import imageio_ffmpeg

st.set_page_config(page_title="Conversor MP3 para PCM", page_icon="🎵")

st.title("Conversor de MP3 para PCM (G40)")
st.write("Envie um arquivo `.zip` contendo seus áudios `.mp3`. O sistema fará a conversão automática para o formato bruto (`.pcm` | Mono | 16000Hz | 16-bit)")

# Área de upload
uploaded_zip = st.file_uploader("Faça o upload do arquivo ZIP com os MP3", type=["zip"])

if uploaded_zip is not None:
    if st.button("Processar e Converter"):
        with st.spinner("Extraindo e convertendo arquivos. Aguarde..."):
            
            # Cria um diretório temporário para trabalhar de forma segura
            with tempfile.TemporaryDirectory() as temp_dir:
                pasta_entrada = os.path.join(temp_dir, "entrada")
                pasta_saida = os.path.join(temp_dir, "saida")
                os.makedirs(pasta_entrada)
                os.makedirs(pasta_saida)
                
                # 1. Salva o ZIP enviado pelo usuário
                caminho_zip_entrada = os.path.join(temp_dir, "upload.zip")
                with open(caminho_zip_entrada, "wb") as f:
                    f.write(uploaded_zip.getvalue())
                    
                # 2. Extrai os arquivos MP3
                with zipfile.ZipFile(caminho_zip_entrada, 'r') as zip_ref:
                    zip_ref.extractall(pasta_entrada)
                    
                # Procura por arquivos MP3 dentro do ZIP extraído
                arquivos_mp3 = []
                for root, dirs, files in os.walk(pasta_entrada):
                    for file in files:
                        if file.lower().endswith('.mp3'):
                            arquivos_mp3.append(os.path.join(root, file))
                            
                if not arquivos_mp3:
                    st.error("Nenhum arquivo MP3 foi encontrado dentro deste ZIP.")
                else:
                    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                    erros = 0
                    
                    # 3. Converte arquivo por arquivo
                    barra_progresso = st.progress(0)
                    for i, caminho_mp3 in enumerate(arquivos_mp3):
                        nome_arquivo = os.path.basename(caminho_mp3)
                        nome_base = os.path.splitext(nome_arquivo)[0]
                        caminho_pcm = os.path.join(pasta_saida, f"{nome_base}.pcm")
                        
                        cmd = [
                            ffmpeg_exe, "-y", "-i", caminho_mp3, 
                            "-f", "s16le", "-ac", "1", "-ar", "16000", "-acodec", "pcm_s16le", 
                            caminho_pcm
                        ]
                        
                        try:
                            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                        except subprocess.CalledProcessError:
                            erros += 1
                            st.warning(f"Falha ao converter: {nome_arquivo}")
                            
                        # Atualiza a barra de progresso
                        barra_progresso.progress((i + 1) / len(arquivos_mp3))
                    
                    # 4. Compacta os arquivos PCM gerados em um novo ZIP
                    caminho_zip_saida = os.path.join(temp_dir, "convertidos.zip")
                    with zipfile.ZipFile(caminho_zip_saida, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                        for root, dirs, files in os.walk(pasta_saida):
                            for file in files:
                                if file.endswith('.pcm'):
                                    caminho_completo = os.path.join(root, file)
                                    # Grava no zip apenas o nome do arquivo, sem as pastas temporárias
                                    zip_out.write(caminho_completo, arcname=file)
                    
                    # 5. Prepara o ZIP para download
                    with open(caminho_zip_saida, "rb") as f:
                        dados_zip = f.read()
                        
                    if erros == 0:
                        st.success(f"Sucesso! {len(arquivos_mp3)} arquivos convertidos.")
                    else:
                        st.warning(f"Concluído com {erros} erro(s). {len(arquivos_mp3) - erros} arquivos convertidos.")
                    
                    st.download_button(
                        label="⬇️ Baixar ZIP com áudios PCM",
                        data=dados_zip,
                        file_name="Audios_PCM_Prontos.zip",
                        mime="application/zip",
                        type="primary"
                    )