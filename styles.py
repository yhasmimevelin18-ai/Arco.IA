# styles.py - Geração de prompts e configurações de estilo

from config import ESTILOS

def gerar_prompt(estilo_key: str, produto_nome: str, descricao: str = "", detalhes_extras: str = "") -> str:
    """
    Gera um prompt otimizado para geração de vídeo com base no estilo escolhido.
    """
    if estilo_key not in ESTILOS:
        estilo_key = "ugc"

    estilo = ESTILOS[estilo_key]
    base = estilo["prompt_base"]

    prompt = f"""{base}.

Product: {produto_nome}.
{descricao if descricao else ""}

High quality, sharp details, natural colors, 9:16 vertical video, cinematic lighting, realistic textures.
{detalhes_extras}

Style: authentic Brazilian affiliate video for Shopee, engaging, clean background when possible, product is the hero.
"""
    return prompt.strip()


def gerar_legenda(produto_nome: str, estilo: str, preco: str = "", beneficio: str = "") -> str:
    """
    Gera legenda + hashtags prontas para Shopee Vídeo.
    """
    hashtags = "#shopee #achadinhos #promoção #viral #recomendado #oferta"

    if estilo == "ugc":
        inicio = f"Gente, olha esse {produto_nome} que eu comprei 😍"
    elif estilo == "pov":
        inicio = f"POV: você acabou de achar o {produto_nome} perfeito"
    elif estilo == "lifestyle":
        inicio = f"Usando meu {produto_nome} no dia a dia ✨"
    elif estilo == "close_up":
        inicio = f"Olha os detalhes desse {produto_nome} 🔥"
    else:
        inicio = f"Achadinho: {produto_nome}"

    corpo = ""
    if beneficio:
        corpo += f"\n{beneficio}"
    if preco:
        corpo += f"\nPor apenas {preco} 💸"

    legenda = f"""{inicio}
{corpo}

Link na bio / comentários 👇
{hashtags}"""
    return legenda.strip()


def listar_estilos():
    """Retorna lista formatada dos estilos para a interface."""
    return {k: v["nome"] for k, v in ESTILOS.items()}
