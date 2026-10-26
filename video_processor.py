# video_processor.py - Processamento de vídeo para Shopee (FFmpeg + MoviePy)

import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from config import SHOPEE_SPECS, OUTPUTS_DIR, TEMP_DIR, WATERMARK_DEFAULT


def verificar_ffmpeg() -> bool:
    """Verifica se o FFmpeg está instalado."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


def redimensionar_para_shopee(
    video_entrada: str,
    video_saida: Optional[str] = None,
    duracao_max: int = 25
) -> str:
    """
    Redimensiona o vídeo para 9:16 (1080x1920), corta se necessário e limita duração.
    """
    if not video_saida:
        nome = Path(video_entrada).stem
        video_saida = str(OUTPUTS_DIR / f"{nome}_shopee.mp4")

    w = SHOPEE_SPECS["width"]
    h = SHOPEE_SPECS["height"]

    # Filtro: escala mantendo proporção + crop central para 9:16
    filtro = (
        f"scale={w}:{h}:force_original_aspect_ratio=increase,"
        f"crop={w}:{h},setsar=1"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", video_entrada,
        "-t", str(duracao_max),
        "-vf", filtro,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        video_saida
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return video_saida


def adicionar_marca_dagua(
    video_entrada: str,
    texto: str = None,
    posicao: str = "bottom_right",
    opacidade: float = 0.55,
    video_saida: Optional[str] = None
) -> str:
    """
    Adiciona marca d'água de texto no vídeo.
    """
    if not texto:
        texto = WATERMARK_DEFAULT["texto"]

    if not video_saida:
        nome = Path(video_entrada).stem
        video_saida = str(OUTPUTS_DIR / f"{nome}_wm.mp4")

    # Posições aproximadas (em pixels para 1080x1920)
    posicoes = {
        "top_left": "x=30:y=40",
        "top_right": "x=w-tw-30:y=40",
        "bottom_left": "x=30:y=h-th-50",
        "bottom_right": "x=w-tw-30:y=h-th-50",
    }
    pos = posicoes.get(posicao, posicoes["bottom_right"])

    # Escapa caracteres especiais do texto
    texto_escapado = texto.replace(":", "\\:").replace("'", "\\'")

    filtro = (
        f"drawtext=text='{texto_escapado}':"
        f"fontsize=36:fontcolor=white@{opacidade}:"
        f"borderw=2:bordercolor=black@0.4:"
        f"{pos}"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", video_entrada,
        "-vf", filtro,
        "-c:a", "copy",
        video_saida
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return video_saida


def criar_capa_do_video(
    video_path: str,
    segundo: float = 1.0,
    saida: Optional[str] = None
) -> str:
    """
    Extrai um frame do vídeo para usar como capa.
    """
    if not saida:
        nome = Path(video_path).stem
        saida = str(OUTPUTS_DIR / f"{nome}_capa.jpg")

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(segundo),
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        saida
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return saida


def criar_variacoes_simples(
    video_entrada: str,
    quantidade: int = 3
) -> list:
    """
    Cria variações simples (zoom leve, speed, crop diferente) para evitar conteúdo idêntico.
    """
    variacoes = []
    base_nome = Path(video_entrada).stem

    for i in range(quantidade):
        saida = str(OUTPUTS_DIR / f"{base_nome}_var{i+1}.mp4")

        if i == 0:
            # Zoom suave
            filtro = "scale=1.08*iw:1.08*ih,crop=iw/1.08:ih/1.08"
        elif i == 1:
            # Espelhado horizontal
            filtro = "hflip"
        else:
            # Leve aceleração
            filtro = "setpts=0.92*PTS"

        cmd = [
            "ffmpeg", "-y",
            "-i", video_entrada,
            "-vf", filtro,
            "-c:a", "copy",
            saida
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            variacoes.append(saida)
        except Exception:
            continue

    return variacoes


def processar_video_completo(
    video_entrada: str,
    marca_dagua: str = "@seu_perfil",
    criar_variacoes: bool = True,
    extrair_capa: bool = True
) -> dict:
    """
    Pipeline completo: redimensiona → marca d'água → capa → variações.
    """
    resultado = {
        "video_principal": None,
        "capa": None,
        "variacoes": [],
        "erro": None
    }

    try:
        # 1. Redimensiona para Shopee
        video_9x16 = redimensionar_para_shopee(video_entrada)

        # 2. Adiciona marca d'água
        video_final = adicionar_marca_dagua(video_9x16, texto=marca_dagua)
        resultado["video_principal"] = video_final

        # 3. Capa
        if extrair_capa:
            resultado["capa"] = criar_capa_do_video(video_final)

        # 4. Variações
        if criar_variacoes:
            resultado["variacoes"] = criar_variacoes_simples(video_final, quantidade=2)

        return resultado

    except Exception as e:
        resultado["erro"] = str(e)
        return resultado
