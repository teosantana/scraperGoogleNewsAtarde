
import unicodedata
import re

from auxiliar.municipios import get_municipios_metadata
from auxiliar.spacy_extract import extrair_municipios

# Lista de palavras ambíguas que podem causar confusão na detecção de municípios
PALAVRAS_AMBIGUAS = {
    "saude", "gloria", "vitoria", "esperanca", "nazaré", "america",
    "campo", "alegre", "formosa", "nova", "belo", "bonito", "feira", "central",
    "santana", "wagner", "Wagner"
}

def normalize_text(text):
    """Normaliza o texto removendo acentos e convertendo para minúsculas."""
    if not isinstance(text, str):
        return ""
    try:
        nfkd_form = unicodedata.normalize('NFKD', text.lower())
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    except Exception:
        return text.lower()

ALL_BAHIA_MUNICIPIOS_DATA = get_municipios_metadata()
MUNICIPIO_LOOKUP = {
    normalize_text(nome_original): f"{nome_original}-{codigo}"
    for nome_original, codigo in ALL_BAHIA_MUNICIPIOS_DATA.items()
}
NORMALIZED_MUNICIPIO_NAMES = set(MUNICIPIO_LOOKUP.keys())

# Dicionário para municípios compostos (mais de uma palavra)
MULTI_WORD_MUNICIPIOS = {}
for name_original in ALL_BAHIA_MUNICIPIOS_DATA.keys():
    if ' ' in name_original:
        normalized_name = normalize_text(name_original)
        components = normalized_name.split()
        for comp in components:
            if comp in NORMALIZED_MUNICIPIO_NAMES:
                if normalized_name not in MULTI_WORD_MUNICIPIOS:
                    MULTI_WORD_MUNICIPIOS[normalized_name] = []
                if comp not in MULTI_WORD_MUNICIPIOS[normalized_name]:
                    MULTI_WORD_MUNICIPIOS[normalized_name].append(comp)

def pre_process_text_for_municipality_detection(text):
    """Remove sufixos comuns como (BA), - BA, etc., do texto."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'\s*\(BA\)\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*-\s*BA\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r',\s*BA\b', '', text, flags=re.IGNORECASE)
    return text.strip()

def is_geographical_context(name, text):
    """
    Verifica se um nome aparece em um contexto que sugere ser um nome geográfico.
    Aplica pre-processamento no texto antes de verificar.
    """
    if not isinstance(name, str) or not isinstance(text, str):
        return False

    processed_text = pre_process_text_for_municipality_detection(text)
    normalized_name_escaped = re.escape(normalize_text(name))

    padroes_geograficos = [
        rf"\b(prefeitura|município|cidade|câmara)\s+(?:de|do|da|d[oa]s?)\s+{normalized_name_escaped}\b",
        rf"\b(?:em|na|no|de|do|da|para|às?)\s+{normalized_name_escaped}\b",
        rf"\b{normalized_name_escaped}\s+(?:prefeitura|município|cidade)\b"
    ]

    for pattern in padroes_geograficos:
        if re.search(pattern, processed_text, re.IGNORECASE):
            return True
    return False

def should_ignore_municipality(name, text):
    """
    Determina se um nome deve ser ignorado com lógica extra para verificação de palavras ambíguas.
    """
    if not isinstance(name, str):
        return True
    normalized_name = normalize_text(name)
    if normalized_name == 'bahia':
        return True
    if normalized_name in PALAVRAS_AMBIGUAS:
        return not is_geographical_context(name, text)
    return False

def get_municipios_from_title(title, text_content):
    """
    Extrai e filtra municípios usando o modelo do spacy e o contexto.
    Aplica pre-processamento no texto antes de extrair e filtrar.
    Aplica pós-processamento para tratar municípios com mais de uma palavra.
    Prioriza o contexto ao máximo.
    """
    if not title and not text_content:
        return []

    processed_title = pre_process_text_for_municipality_detection(title)
    processed_text_content = pre_process_text_for_municipality_detection(text_content)
    context_text = processed_text_content if processed_text_content and processed_text_content.strip() else processed_title

    potential_municipios_raw = extrair_municipios(processed_title)
    potential_normalized_set = {normalize_text(name) for name in potential_municipios_raw if isinstance(name, str)}
    filtered_municipios_normalized = set()

    for nome_raw in potential_municipios_raw:
        if not isinstance(nome_raw, str) or not nome_raw.strip():
            continue
        normalized_name = normalize_text(nome_raw)
        if normalized_name in NORMALIZED_MUNICIPIO_NAMES and normalized_name != 'bahia':
            if not should_ignore_municipality(nome_raw, context_text):
                is_component_of_detected_multi_word = False
                for multi_word_normalized, components_normalized in MULTI_WORD_MUNICIPIOS.items():
                    if normalized_name in components_normalized:
                        if multi_word_normalized in potential_normalized_set:
                            is_component_of_detected_multi_word = True
                            break
                if not is_component_of_detected_multi_word:
                    filtered_municipios_normalized.add(normalized_name)

    mapped_list = []
    for normalized_filtered_name in filtered_municipios_normalized:
        if normalized_filtered_name in MUNICIPIO_LOOKUP:
            mapped_list.append(MUNICIPIO_LOOKUP[normalized_filtered_name])
    return list(dict.fromkeys(mapped_list))