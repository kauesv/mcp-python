"""
Tool para calcular estatísticas básicas de texto.
"""

import re
from typing import Dict, Any


async def text_stats(text: str) -> Dict[str, Any]:
    """
    Calcula estatísticas básicas de um texto fornecido.

    Argumentos:
        text: O texto para analisar

    Retorna:
        Dicionário com estatísticas do texto (contagem de caracteres, palavras, linhas, etc.)
    """
    if not text or not text.strip():
        return {
            "error": "Texto vazio ou inválido fornecido",
            "characters": 0,
            "words": 0,
            "lines": 0,
            "sentences": 0
        }
    
    # Contagem básica
    characters = len(text)
    characters_no_spaces = len(text.replace(" ", ""))
    words = len(text.split())
    lines = len(text.splitlines())
    
    # Contagem de frases (aproximada)
    sentences = len(re.split(r'[.!?]+', text))
    
    # Palavras únicas
    unique_words = len(set(word.lower().strip('.,!?;:') for word in text.split() if word.strip()))
    
    # Palavra mais longa
    longest_word = max(text.split(), key=len) if text.split() else ""
    
    return {
        "characters": characters,
        "characters_no_spaces": characters_no_spaces,
        "words": words,
        "lines": lines,
        "sentences": sentences,
        "unique_words": unique_words,
        "longest_word": longest_word,
        "average_word_length": round(characters_no_spaces / words, 2) if words > 0 else 0
    }
