# Arco.IA - Versão Online (Streamlit Cloud)
# Foco: prompts + legendas + Motion Control (quando tiver API Key)

import streamlit as st
from pathlib import Path
from datetime import datetime
import os

from config import ESTILOS, MOVIMENTOS, WATERMARK_DEFAULT, SHOPEE_SPECS
from styles import gerar_prompt, gerar_legenda
from motion_control import KlingMotionControl, obter_instrucoes_motion_control

# ==================== CONFIGURAÇÃO DA PÁGINA ====================
st.set_page_config(
    page_title="Arco.IA | Vídeos para Shopee",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS mobile-friendly
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FF6B00;
        margin-bottom: 0;
        text-align: center;
    }
    .subtitle {
        color: #666;
        font-size: 1rem;
        margin-top: 0;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-weight: 600;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #eee;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 🎬 Arco.IA")
    st.caption("Vídeos para Shopee Vídeo")
    st.divider()

    modo = st.radio(
        "O que você quer fazer?",
        [
            "🎨 Gerar Prompt + Legenda",
            "🕹️ Motion Control (Kling)",
            "📋 Como usar o Google Flow"
        ],
        index=0
    )

    st.divider()
    st.markdown("### Sua marca d'água")
    marca_dagua = st.text_input("Texto da marca d'água", value="@seu_perfil", label_visibility="collapsed")

    st.divider()
    st.caption("Versão online • Uso pessoal")

# ==================== CABEÇALHO ====================
st.markdown('<p class="main-title">Arco.IA</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Crie vídeos prontos para Shopee Vídeo</p>', unsafe_allow_html=True)
st.divider()

# ==================== MODO 1: GERAR PROMPT + LEGENDA ====================
if modo == "🎨 Gerar Prompt + Legenda":
    st.subheader("Informações do produto")

    produto_nome = st.text_input("Nome do produto *", placeholder="Ex: Vestido Midi Floral")
    
    col1, col2 = st.columns(2)
    with col1:
        preco = st.text_input("Preço", placeholder="R$ 59,90")
    with col2:
        estilo_key = st.selectbox(
            "Estilo do vídeo *",
            options=list(ESTILOS.keys()),
            format_func=lambda x: ESTILOS[x]["nome"]
        )

    beneficio = st.text_input("Benefício principal", placeholder="Ex: Confortável e elegante")
    descricao = st.text_area("Detalhes do produto", placeholder="Cor, material, tamanho, diferenciais...", height=90)

    st.markdown("---")
    
    if st.button("🚀 Gerar Prompt + Legenda", type="primary"):
        if not produto_nome.strip():
            st.warning("Digite o nome do produto.")
        else:
            prompt = gerar_prompt(estilo_key, produto_nome, descricao)
            legenda = gerar_legenda(produto_nome, estilo_key, preco, beneficio)

            st.success("Pronto! Copie e use:")

            st.markdown("### 📝 Prompt (cole no Google Flow ou Kling)")
            st.code(prompt, language=None)
            
            st.download_button(
                "⬇️ Baixar prompt",
                prompt,
                file_name="prompt_arcoia.txt",
                mime="text/plain"
            )

            st.markdown("### 💬 Legenda pronta para Shopee")
            st.text_area("Legenda", legenda, height=160, label_visibility="collapsed")
            
            st.download_button(
                "⬇️ Baixar legenda",
                legenda,
                file_name="legenda_arcoia.txt",
                mime="text/plain"
            )

            st.info("💡 **Próximo passo:** Abra o Google Flow, cole o prompt e gere o vídeo. Depois baixe e poste na Shopee.")

# ==================== MODO 2: MOTION CONTROL ====================
elif modo == "🕹️ Motion Control (Kling)":
    st.subheader("Motion Control (Kling)")

    kling = KlingMotionControl()
    tem_key = kling.tem_api_key()

    if tem_key:
        st.success("API Key do Kling detectada ✓")
    else:
        st.warning("Você ainda não colocou a API Key do Kling.")
        with st.expander("📌 Como configurar a API Key (passo a passo)"):
            st.markdown("""
1. Crie conta em [kling.ai](https://kling.ai)
2. Gere uma API Key
3. No Streamlit Cloud, vá em **Settings → Secrets**
4. Adicione:
```toml
KLING_API_KEY = "sua_chave_aqui"
```
5. Salve e reinicie o app
            """)

    st.markdown("#### 1. Imagem do produto")
    imagem_mc = st.file_uploader(
        "Foto do produto ou pessoa segurando",
        type=["jpg", "jpeg", "png", "webp"]
    )

    st.markdown("#### 2. Tipo de movimento")
    mov_escolhido = st.selectbox(
        "Escolha o movimento",
        options=list(MOVIMENTOS.keys()),
        format_func=lambda x: MOVIMENTOS[x]["nome"]
    )
    st.caption(MOVIMENTOS[mov_escolhido]["descricao"])

    prompt_extra = st.text_input(
        "Detalhes extras (opcional)",
        placeholder="Ex: luz natural, fundo limpo, cores vibrantes"
    )

    if st.button("🎬 Gerar com Motion Control", type="primary"):
        if not imagem_mc:
            st.warning("Envie a imagem do produto.")
        elif not tem_key:
            st.error("Coloque a API Key do Kling primeiro (veja as instruções acima).")
        else:
            st.info("Quando a API Key estiver configurada, o vídeo será gerado aqui.")
            st.warning("A geração real depende da API do Kling estar ativa e com créditos.")

    with st.expander("ℹ️ O que é Motion Control?"):
        st.markdown("""
O **Motion Control** do Kling permite que você:
- Envie uma **foto** do produto
- Escolha um **movimento** (girar na mão, colocar na cama, close-up...)
- A IA aplica esse movimento na foto

Fica bem mais controlado do que só escrever um prompt.
        """)

# ==================== MODO 3: COMO USAR O FLOW ====================
elif modo == "📋 Como usar o Google Flow":
    st.subheader("Como gerar o vídeo no Google Flow")

    st.markdown("""
### Passo a passo simples:

1. **Abra o Google Flow**  
   Acesse pelo navegador do celular ou computador.

2. **Volte no Arco.IA** e gere o prompt  
   Use o modo **Gerar Prompt + Legenda**.

3. **Copie o prompt** completo.

4. **Cole no Google Flow** e gere o vídeo.

5. **Baixe o vídeo** gerado.

6. **Poste na Shopee Vídeo**  
   Formato ideal: vertical (9:16), entre 15 e 25 segundos.

---

### Dicas para melhores resultados:

- Use o estilo **UGC** ou **Produto na mão** → costuma converter mais
- Sempre mencione no prompt: `9:16 vertical video`
- Se o vídeo sair horizontal, peça no prompt: `vertical smartphone video, 9:16 aspect ratio`
- Gere 2 ou 3 versões e escolha a melhor

---

### Quando tiver Kling:

O modo **Motion Control** fica bem mais poderoso, porque você controla o movimento de verdade (não só o texto).
    """)

    st.success("Comece pelo modo **Gerar Prompt + Legenda** → é o mais rápido.")

# ==================== RODAPÉ ====================
st.divider()
st.caption(f"Arco.IA • Online • {datetime.now().strftime('%d/%m/%Y %H:%M')}")
st.caption("Formato alvo Shopee: 1080×1920 (9:16)")
