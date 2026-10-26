# motion_control.py - Integração com Kling Motion Control

import os
import time
from pathlib import Path
from typing import Optional, Dict, Any
from config import KLING_API_KEY, MOTIONS_DIR, MOVIMENTOS, TEMP_DIR


class KlingMotionControl:
    """
    Classe para interagir com a API do Kling Motion Control.
    Preparada para quando você tiver a API Key.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or KLING_API_KEY
        self.base_url = "https://api.klingai.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def tem_api_key(self) -> bool:
        return bool(self.api_key and len(str(self.api_key)) > 10)

    def listar_movimentos_disponiveis(self) -> Dict:
        resultado = {}
        for key, info in MOVIMENTOS.items():
            arquivo_path = MOTIONS_DIR / info["arquivo"]
            resultado[key] = {
                **info,
                "existe": arquivo_path.exists() if MOTIONS_DIR.exists() else False,
                "caminho": str(arquivo_path) if arquivo_path.exists() else None
            }
        return resultado

    def gerar_com_motion_control(
        self,
        imagem_path: str,
        video_movimento_path: str,
        prompt: str = "",
        character_orientation: str = "video",
        mode: str = "pro",
        keep_sound: bool = False
    ) -> Dict[str, Any]:
        if not self.tem_api_key():
            return {
                "sucesso": False,
                "erro": "API Key do Kling não configurada.",
                "modo": "simulacao"
            }

        # Esqueleto pronto. Ajuste o endpoint conforme a documentação oficial do Kling.
        return {
            "sucesso": False,
            "erro": "Integração da API pronta para ser conectada. Configure a chave e ajuste o endpoint se necessário.",
            "modo": "preparado"
        }


def obter_instrucoes_motion_control() -> str:
    return """
### Como usar o Motion Control (Kling)

1. Tenha uma conta no Kling e gere uma API Key.
2. No Streamlit Cloud: Settings → Secrets → adicione:
   KLING_API_KEY = "sua_chave"
3. No Arco.IA escolha o modo Motion Control.
"""
