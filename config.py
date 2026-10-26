# config.py - Configurações do Arco.IA

import os
from pathlib import Path

# Tenta carregar do Streamlit Secrets (quando online) e do .env (local)
try:
    import streamlit as st
    KLING_API_KEY = st.secrets.get("KLING_API_KEY", "") or os.getenv("KLING_API_KEY", "")
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    KLING_API_KEY = os.getenv("KLING_API_KEY", "")

# Caminhos
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
MOTIONS_DIR = ASSETS_DIR / "motions"
OUTPUTS_DIR = BASE_DIR / "outputs"
TEMP_DIR = BASE_DIR / "temp"

for pasta in [ASSETS_DIR, MOTIONS_DIR, OUTPUTS_DIR, TEMP_DIR]:
    try:
        pasta.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

# Configurações de vídeo para Shopee
SHOPEE_SPECS = {
    "aspect_ratio": "9:16",
    "width": 1080,
    "height": 1920,
    "min_duration": 15,
    "max_duration": 60,
    "ideal_duration": 20,
    "fps": 30,
}

# Estilos disponíveis
ESTILOS = {
    "ugc": {
        "nome": "UGC (User Generated Content)",
        "descricao": "Parece vídeo feito por cliente real, natural e autêntico",
        "prompt_base": "UGC style, authentic customer video, natural lighting, handheld camera, real person showing product"
    },
    "pov": {
        "nome": "POV (Primeira Pessoa)",
        "descricao": "Como se a câmera fosse os olhos do usuário",
        "prompt_base": "POV shot, first person view, hands holding product, immersive perspective"
    },
    "lifestyle": {
        "nome": "Lifestyle",
        "descricao": "Produto em uso no dia a dia, ambiente bonito",
        "prompt_base": "Lifestyle photography, product in use, aesthetic environment, soft natural light"
    },
    "produto_na_mao": {
        "nome": "Produto na Mão",
        "descricao": "Mão segurando e mostrando o produto",
        "prompt_base": "Product held in hand, close up of hands presenting item, clean background"
    },
    "close_up": {
        "nome": "Close-up",
        "descricao": "Detalhes do produto bem de perto",
        "prompt_base": "Extreme close-up, product details, macro shot, sharp focus on texture and features"
    },
    "em_cima_da_cama": {
        "nome": "Em cima da cama",
        "descricao": "Produto disposto na cama, flatlay ou com pessoa",
        "prompt_base": "Product on bed, flat lay or person lying with product, cozy bedroom aesthetic"
    },
    "unboxing": {
        "nome": "Unboxing",
        "descricao": "Abrindo a embalagem e revelando o produto",
        "prompt_base": "Unboxing video, hands opening package, revealing product, excited reaction"
    },
    "demonstracao": {
        "nome": "Demonstração",
        "descricao": "Mostrando como usar o produto",
        "prompt_base": "Product demonstration, how to use, step by step, clear tutorial style"
    }
}

# Movimentos prontos para Motion Control
MOVIMENTOS = {
    "girar_na_mao": {
        "nome": "Girar produto na mão",
        "descricao": "Mão segurando e girando o produto 360°",
        "arquivo": "girar_na_mao.mp4",
        "duracao_sugerida": 8
    },
    "colocar_na_cama": {
        "nome": "Colocar em cima da cama",
        "descricao": "Mão colocando o produto suavemente na cama",
        "arquivo": "colocar_na_cama.mp4",
        "duracao_sugerida": 6
    },
    "close_up_girando": {
        "nome": "Close-up girando",
        "descricao": "Produto girando bem de perto mostrando detalhes",
        "arquivo": "close_up_girando.mp4",
        "duracao_sugerida": 7
    },
    "pov_mao": {
        "nome": "POV - Mão do usuário",
        "descricao": "Como se fosse sua mão segurando e mexendo no produto",
        "arquivo": "pov_mao.mp4",
        "duracao_sugerida": 8
    },
    "unboxing_movimento": {
        "nome": "Unboxing",
        "descricao": "Abrindo caixa e tirando o produto",
        "arquivo": "unboxing.mp4",
        "duracao_sugerida": 12
    },
    "mostrar_detalhes": {
        "nome": "Mostrar detalhes",
        "descricao": "Aproxima e mostra textura, costura, botões etc.",
        "arquivo": "mostrar_detalhes.mp4",
        "duracao_sugerida": 7
    }
}

WATERMARK_DEFAULT = {
    "texto": "@seu_perfil",
    "posicao": "bottom_right",
    "opacidade": 0.6,
    "tamanho_fonte": 36,
}
