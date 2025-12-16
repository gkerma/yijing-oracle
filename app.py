#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     易經 YI JING ORACLE v2.2                                 ║
║                    Application Streamlit Multilingue                         ║
║         Grilles animées • Textes complets • PDF détaillé • Kasina KBS       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import random
import json
import datetime
import base64
import textwrap
import time
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# Import des traductions
from translations import t, LANGUAGES, get_hex_name, get_trigram_name

# Import du module pour les images de caractères (fallback)
try:
    from char_image import create_character_image, set_font_path
    CHAR_IMAGE_AVAILABLE = True
    # Définir le chemin de la police pour le module char_image
    import os
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _embedded_font = os.path.join(_script_dir, 'fonts', 'ipag.ttf')
    if os.path.exists(_embedded_font):
        set_font_path(_embedded_font)
except ImportError:
    CHAR_IMAGE_AVAILABLE = False
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph

import numpy as np
from scipy.io import wavfile

# ============================================================================
# CONFIGURATION PAGE
# ============================================================================

st.set_page_config(
    page_title="易經 Yi Jing Oracle",
    page_icon="☯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# INITIALISATION POLICE CJK
# ============================================================================
# Initialiser la police CJK au démarrage pour le diagnostic
# (sera appelé plus tard par generate_pdf_report_complete)

# ============================================================================
# DONNÉES STATIQUES
# ============================================================================

BINAIRE_TO_HEX = {
    (1,1,1,1,1,1): 1, (0,0,0,0,0,0): 2, (1,0,0,0,1,0): 3, (0,1,0,0,0,1): 4,
    (1,1,1,0,1,0): 5, (0,1,0,1,1,1): 6, (0,1,0,0,0,0): 7, (0,0,0,0,1,0): 8,
    (1,1,1,0,1,1): 9, (1,1,0,1,1,1): 10, (1,1,1,0,0,0): 11, (0,0,0,1,1,1): 12,
    (1,0,1,1,1,1): 13, (1,1,1,1,0,1): 14, (0,0,1,0,0,0): 15, (0,0,0,1,0,0): 16,
    (1,0,0,1,1,0): 17, (0,1,1,0,0,1): 18, (1,1,0,0,0,0): 19, (0,0,0,0,1,1): 20,
    (1,0,0,1,0,1): 21, (1,0,1,0,0,1): 22, (0,0,0,0,0,1): 23, (1,0,0,0,0,0): 24,
    (1,0,0,1,1,1): 25, (1,1,1,0,0,1): 26, (1,0,0,0,0,1): 27, (0,1,1,1,1,0): 28,
    (0,1,0,0,1,0): 29, (1,0,1,1,0,1): 30, (0,0,1,1,1,0): 31, (0,1,1,1,0,0): 32,
    (0,0,1,1,1,1): 33, (1,1,1,1,0,0): 34, (0,0,0,1,0,1): 35, (1,0,1,0,0,0): 36,
    (1,0,1,0,1,1): 37, (1,1,0,1,0,1): 38, (0,0,1,0,1,0): 39, (0,1,0,1,0,0): 40,
    (1,1,0,0,0,1): 41, (1,0,0,0,1,1): 42, (1,1,1,1,1,0): 43, (0,1,1,1,1,1): 44,
    (0,0,0,1,1,0): 45, (0,1,1,0,0,0): 46, (0,1,0,1,1,0): 47, (0,1,1,0,1,0): 48,
    (1,0,1,1,1,0): 49, (0,1,1,1,0,1): 50, (0,0,1,0,0,1): 51, (1,0,0,1,0,0): 52,
    (0,0,1,0,1,1): 53, (1,1,0,1,0,0): 54, (1,0,1,0,0,1): 55, (0,0,1,1,0,1): 56,
    (0,1,1,0,1,1): 57, (1,1,0,1,1,0): 58, (0,1,0,0,1,1): 59, (1,1,0,0,1,0): 60,
    (1,1,0,0,1,1): 61, (0,0,1,1,0,0): 62, (1,0,1,0,1,0): 63, (0,1,0,1,0,1): 64,
}

TRIGRAMMES = {
    "K'ien": {"symbole": "☰", "element": "Ciel", "freq": 852, "nature": "Fort, créatif"},
    "K'ouen": {"symbole": "☷", "element": "Terre", "freq": 396, "nature": "Réceptif, docile"},
    "Tchen": {"symbole": "☳", "element": "Tonnerre", "freq": 417, "nature": "Éveilleur, mouvement"},
    "K'an": {"symbole": "☵", "element": "Eau", "freq": 528, "nature": "Abyssal, danger"},
    "Ken": {"symbole": "☶", "element": "Montagne", "freq": 639, "nature": "Immobile, repos"},
    "Souen": {"symbole": "☴", "element": "Vent", "freq": 741, "nature": "Doux, pénétrant"},
    "Li": {"symbole": "☲", "element": "Feu", "freq": 963, "nature": "Lumineux, attachant"},
    "Touei": {"symbole": "☱", "element": "Lac", "freq": 432, "nature": "Joyeux, serein"},
}

FREQ_TRAITS = {
    6: {"freq": 216, "note": "LA-1", "nom": "Yin mutant", "couleur": "#E91E63", "symbole": "━━ ✕ ━━"},
    7: {"freq": 256, "note": "DO", "nom": "Yang stable", "couleur": "#4CAF50", "symbole": "━━━━━━━"},
    8: {"freq": 192, "note": "SOL-1", "nom": "Yin stable", "couleur": "#2196F3", "symbole": "━━   ━━"},
    9: {"freq": 288, "note": "RÉ", "nom": "Yang mutant", "couleur": "#FF9800", "symbole": "━━━◯━━━"}
}

FREQ_SOLFEGGIO = {
    396: "Libération de la culpabilité et de la peur",
    417: "Facilite le changement et la transformation",
    432: "Harmonie universelle, fréquence de la Terre",
    528: "Transformation, réparation ADN, miracles",
    639: "Relations harmonieuses, connexion",
    741: "Éveil de l'intuition, expression",
    852: "Retour à l'ordre spirituel",
    963: "Activation pinéale, unité divine"
}

# Couleurs Kasina RGB (0-100%)
KASINA_RGB = {
    "K'ien": (100, 100, 100),
    "K'ouen": (60, 40, 20),
    "Tchen": (100, 80, 0),
    "K'an": (0, 40, 100),
    "Ken": (50, 50, 60),
    "Souen": (30, 100, 50),
    "Li": (100, 30, 0),
    "Touei": (0, 70, 100),
}

# ============================================================================
# CHARGEMENT DES DONNÉES JSON
# ============================================================================

@st.cache_data
def load_yijing_data(json_path, lang='fr'):
    """Charge les données Yi Jing dans la langue appropriée"""
    import os
    
    # Déterminer le fichier à charger selon la langue
    if lang != 'fr':
        # Chercher le fichier traduit
        base_dir = os.path.dirname(os.path.abspath(__file__))
        lang_file = os.path.join(base_dir, f'yijing_{lang}.json')
        if os.path.exists(lang_file):
            json_path = lang_file
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning(f"⚠️ Fichier JSON non trouvé: {json_path}")
        return {"hexagrammes": []}

def get_hex_from_json(yijing_data, numero):
    for h in yijing_data.get('hexagrammes', []):
        if h.get('numero') == numero:
            return h
    return {}

# ============================================================================
# FONCTIONS DE TIRAGE
# ============================================================================

def tirer_trait():
    return sum(random.choice([2, 3]) for _ in range(3))

def get_hexagramme_numero(traits):
    binaire = tuple(1 if t in [7, 9] else 0 for t in traits)
    return BINAIRE_TO_HEX.get(binaire, 1)

def get_mutation_numero(traits):
    if not any(t in [6, 9] for t in traits):
        return None
    binaire_orig = tuple(1 if t in [7, 9] else 0 for t in traits)
    binaire_mute = tuple(
        (0 if t == 9 else 1 if t == 6 else b)
        for t, b in zip(traits, binaire_orig)
    )
    return BINAIRE_TO_HEX.get(binaire_mute, 1)

# ============================================================================
# GÉNÉRATION DE GRILLES
# ============================================================================

def get_image_key(trait_val, position):
    is_yang = trait_val in [7, 9]
    is_mutant = trait_val in [6, 9]
    key = "YANG" if is_yang else "YING"
    if is_mutant:
        key += "-MUT"
    return f"lldh-YY-{key}-{position}.png"

def generer_grille(traits, images_dir, mutation=False):
    composite = None
    for i, trait in enumerate(traits):
        trait_val = trait
        if mutation and trait in [6, 9]:
            trait_val = 7 if trait == 6 else 8
        filename = get_image_key(trait_val, i + 1)
        filepath = Path(images_dir) / filename
        if not filepath.exists():
            continue
        layer = Image.open(filepath).convert('RGBA')
        if composite is None:
            composite = Image.new('RGBA', layer.size, (255, 255, 255, 255))
        layer_with_bg = Image.new('RGBA', layer.size, (255, 255, 255, 255))
        layer_with_bg = Image.alpha_composite(layer_with_bg, layer)
        composite = ImageChops.multiply(composite, layer_with_bg)
    if composite:
        composite = composite.convert('RGB')
    return composite

def image_to_base64(img):
    """Convertit une image PIL en base64 pour affichage HTML"""
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode()

# ============================================================================
# GÉNÉRATION AUDIO
# ============================================================================

def generate_audio_sequence(traits, sample_rate=44100):
    t_intro = np.linspace(0, 2, int(sample_rate * 2), False)
    intro = np.sin(2 * np.pi * 432 * t_intro) * 0.3
    silence = np.zeros(int(sample_rate * 0.3))
    parts = [intro, silence]
    
    for trait in traits:
        freq = FREQ_TRAITS[trait]['freq']
        t = np.linspace(0, 2, int(sample_rate * 2), False)
        tone = np.sin(2 * np.pi * freq * t) * 0.3
        if trait in [6, 9]:
            beat = np.sin(2 * np.pi * (freq + 3) * t) * 0.15
            tone = tone + beat
        fade_len = int(sample_rate * 0.05)
        tone[:fade_len] *= np.linspace(0, 1, fade_len)
        tone[-fade_len:] *= np.linspace(1, 0, fade_len)
        parts.append(tone)
        parts.append(silence)
    
    t_chord = np.linspace(0, 4, int(sample_rate * 4), False)
    chord = np.zeros_like(t_chord)
    intervals = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25]
    for i, trait in enumerate(traits):
        freq = FREQ_TRAITS[trait]['freq'] * intervals[i]
        chord += np.sin(2 * np.pi * freq * t_chord) / (i + 1)
    chord = chord / np.max(np.abs(chord)) * 0.4
    fade_len = int(sample_rate * 0.3)
    chord[:fade_len] *= np.linspace(0, 1, fade_len)
    chord[-fade_len:] *= np.linspace(1, 0, fade_len)
    parts.append(chord)
    
    audio = np.concatenate(parts)
    audio = audio / np.max(np.abs(audio))
    return (audio * 32767).astype(np.int16)

def audio_to_base64(audio_data, sample_rate=44100):
    buffer = BytesIO()
    wavfile.write(buffer, sample_rate, audio_data)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode()

# ============================================================================
# GÉNÉRATION KASINA KBS
# ============================================================================

def generate_kbs_session(hex_data, duration_minutes=5):
    """Génère une session KBS au format Mindplace"""
    
    trig_bas = hex_data.get('trigramme_bas', 'Touei')
    trig_haut = hex_data.get('trigramme_haut', 'Li')
    
    freq_bas = TRIGRAMMES.get(trig_bas, {}).get('freq', 432)
    freq_haut = TRIGRAMMES.get(trig_haut, {}).get('freq', 528)
    
    rgb_bas = KASINA_RGB.get(trig_bas, (0, 70, 100))
    rgb_haut = KASINA_RGB.get(trig_haut, (100, 30, 0))
    
    hex_num = hex_data.get('numero', 0)
    hex_name = hex_data.get('nom_fr', 'Hexagramme')
    
    kbs = []
    kbs.append(f"; Yi Jing Meditation - Hexagramme {hex_num}: {hex_name}")
    kbs.append(f"; Trigramme Bas: {trig_bas} ({freq_bas} Hz)")
    kbs.append(f"; Trigramme Haut: {trig_haut} ({freq_haut} Hz)")
    kbs.append("; Format: KBS v2 - Mindplace Kasina/Limina")
    kbs.append("")
    kbs.append("[Global]")
    kbs.append("ColorControlMode=3")
    kbs.append("GlobalColorSet=1")
    kbs.append("")
    
    segments = [
        {"name": "Fade In", "Time": 5.00, "Beat": 10.00, "LPtch": 432.00, "RPtch": 442.00,
         "LAMDpth": 50, "SAMDpth": 0, "Bright": 30, "Vol": 30,
         "Red": 40, "Green": 0, "Blue": 80},
        {"name": "Ancrage Alpha", "Time": 55.00, "Beat": 10.00, "LPtch": 432.00, "RPtch": 442.00,
         "LAMDpth": 70, "SAMDpth": 0, "Bright": 60, "Vol": 50,
         "Red": 40, "Green": 0, "Blue": 100},
        {"name": "Transition Theta", "Time": 15.00, "Beat": 8.00, "LPtch": float(freq_bas), "RPtch": float(freq_bas + 7),
         "LAMDpth": 65, "SAMDpth": 0, "Bright": 55, "Vol": 55,
         "Red": rgb_bas[0], "Green": rgb_bas[1], "Blue": rgb_bas[2]},
        {"name": f"Trigramme {trig_bas}", "Time": 75.00, "Beat": 7.00, "LPtch": float(freq_bas), "RPtch": float(freq_bas + 7),
         "LAMDpth": 80, "SAMDpth": 0, "Bright": 55, "Vol": 60,
         "Red": rgb_bas[0], "Green": rgb_bas[1], "Blue": rgb_bas[2]},
        {"name": "Transition", "Time": 15.00, "Beat": 6.00, "LPtch": float((freq_bas + freq_haut) // 2), "RPtch": float((freq_bas + freq_haut) // 2 + 6),
         "LAMDpth": 75, "SAMDpth": 0, "Bright": 50, "Vol": 58,
         "Red": (rgb_bas[0] + rgb_haut[0]) // 2, "Green": (rgb_bas[1] + rgb_haut[1]) // 2, "Blue": (rgb_bas[2] + rgb_haut[2]) // 2},
        {"name": f"Trigramme {trig_haut}", "Time": 75.00, "Beat": 5.00, "LPtch": float(freq_haut), "RPtch": float(freq_haut + 5),
         "LAMDpth": 85, "SAMDpth": 0, "Bright": 50, "Vol": 55,
         "Red": rgb_haut[0], "Green": rgb_haut[1], "Blue": rgb_haut[2]},
        {"name": "Retour Alpha", "Time": 15.00, "Beat": 7.00, "LPtch": 528.00, "RPtch": 535.00,
         "LAMDpth": 70, "SAMDpth": 0, "Bright": 45, "Vol": 50,
         "Red": 0, "Green": 80, "Blue": 50},
        {"name": "Integration", "Time": 35.00, "Beat": 8.00, "LPtch": 528.00, "RPtch": 536.00,
         "LAMDpth": 60, "SAMDpth": 0, "Bright": 40, "Vol": 45,
         "Red": 0, "Green": 100, "Blue": 50},
        {"name": "Fade Out", "Time": 10.00, "Beat": 10.00, "LPtch": 528.00, "RPtch": 538.00,
         "LAMDpth": 20, "SAMDpth": 0, "Bright": 0, "Vol": 0,
         "Red": 0, "Green": 40, "Blue": 30},
    ]
    
    for i, seg in enumerate(segments):
        kbs.append(f"[Segment{i}]")
        kbs.append(f"; {seg['name']}")
        kbs.append(f"Time={seg['Time']:.2f}")
        kbs.append(f"Beat={seg['Beat']:.2f}")
        kbs.append(f"LPtch={seg['LPtch']:.2f}")
        kbs.append(f"RPtch={seg['RPtch']:.2f}")
        kbs.append(f"LPhse=50")
        kbs.append(f"SPhse=50")
        kbs.append(f"LAMDpth={seg['LAMDpth']}")
        kbs.append(f"SAMDpth={seg['SAMDpth']}")
        kbs.append(f"Bright={seg['Bright']}")
        kbs.append(f"Vol={seg['Vol']}")
        kbs.append(f"SndWF=Sine")
        kbs.append(f"SndModWF=Sine")
        kbs.append(f"LgtModWF=Sine")
        kbs.append(f"LgtModPW=50")
        kbs.append(f"SndPW=50")
        kbs.append(f"SndModPW=50")
        kbs.append(f"Red={seg['Red']}")
        kbs.append(f"Green={seg['Green']}")
        kbs.append(f"Blue={seg['Blue']}")
        kbs.append("")
    
    return "\n".join(kbs), segments

def generate_kasina_audio(segments, sample_rate=44100):
    """Génère audio binaural stéréo"""
    audio_parts = []
    for seg in segments:
        duration = seg['Time']
        l_pitch = seg['LPtch']
        r_pitch = seg['RPtch']
        vol = seg['Vol'] / 100.0
        
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        left = np.sin(2 * np.pi * l_pitch * t) * vol
        right = np.sin(2 * np.pi * r_pitch * t) * vol
        stereo = np.column_stack((left, right))
        
        fade_samples = min(int(sample_rate * 0.5), len(stereo) // 4)
        if fade_samples > 0:
            fade_in = np.linspace(0, 1, fade_samples).reshape(-1, 1)
            fade_out = np.linspace(1, 0, fade_samples).reshape(-1, 1)
            stereo[:fade_samples] *= fade_in
            stereo[-fade_samples:] *= fade_out
        audio_parts.append(stereo)
    
    full_audio = np.vstack(audio_parts)
    max_val = np.max(np.abs(full_audio))
    if max_val > 0:
        full_audio = full_audio / max_val * 0.7
    return (full_audio * 32767).astype(np.int16)

# ============================================================================
# GÉNÉRATION PDF COMPLET
# ============================================================================

# Variable globale pour stocker le nom de la police CJK
_CJK_FONT_NAME = None
_CJK_FONT_INITIALIZED = False
_CJK_FONT_ERROR = None

def init_cjk_font():
    """Initialise une police CJK pour les caractères chinois"""
    global _CJK_FONT_NAME, _CJK_FONT_INITIALIZED, _CJK_FONT_ERROR
    
    # Si déjà initialisé, retourner le résultat précédent
    if _CJK_FONT_INITIALIZED:
        return _CJK_FONT_NAME
    
    from reportlab.pdfbase.ttfonts import TTFont
    import os
    import traceback
    
    errors = []
    
    # 1. Police embarquée dans le projet (priorité absolue)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    embedded_font = os.path.join(script_dir, 'fonts', 'ipag.ttf')
    
    if os.path.exists(embedded_font):
        # Essayer avec différents noms au cas où la police serait déjà enregistrée
        for font_name in ['IPAGothic', 'IPAGothic2', 'YiJingCJK']:
            try:
                pdfmetrics.registerFont(TTFont(font_name, embedded_font))
                _CJK_FONT_NAME = font_name
                _CJK_FONT_INITIALIZED = True
                _CJK_FONT_ERROR = None
                return _CJK_FONT_NAME
            except Exception as e:
                errors.append(f"Police embarquée ({font_name}): {str(e)}")
                # Si c'est une erreur "already registered", c'est OK
                if "already registered" in str(e).lower():
                    _CJK_FONT_NAME = font_name
                    _CJK_FONT_INITIALIZED = True
                    _CJK_FONT_ERROR = None
                    return _CJK_FONT_NAME
    
    # 2. Polices système (Linux, macOS, Windows)
    ttf_fonts = [
        # Linux Debian/Ubuntu
        '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf',
        '/usr/share/fonts/truetype/fonts-ipafont-gothic/ipag.ttf',
        '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        # Linux Fedora/Arch
        '/usr/share/fonts/ipa-gothic/ipag.ttf',
        '/usr/share/fonts/OTF/ipag.ttf',
        # macOS
        '/Library/Fonts/IPAPGothic.ttf',
        os.path.expanduser('~/Library/Fonts/IPAPGothic.ttf'),
        '/System/Library/Fonts/PingFang.ttc',
        # Windows
        'C:/Windows/Fonts/ipag.ttf',
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/simsun.ttc',
        'C:/Windows/Fonts/simhei.ttf',
    ]
    
    for font_path in ttf_fonts:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('IPAGothic', font_path))
                _CJK_FONT_NAME = 'IPAGothic'
                _CJK_FONT_INITIALIZED = True
                _CJK_FONT_ERROR = None
                return _CJK_FONT_NAME
            except Exception as e:
                errors.append(f"Système {font_path}: {str(e)}")
                continue
    
    # 3. Fallback CID (dépend du viewer PDF)
    try:
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        _CJK_FONT_NAME = 'STSong-Light'
        _CJK_FONT_INITIALIZED = True
        _CJK_FONT_ERROR = None
        return _CJK_FONT_NAME
    except Exception as e:
        errors.append(f"CID STSong-Light: {str(e)}")
    
    _CJK_FONT_INITIALIZED = True
    _CJK_FONT_ERROR = " | ".join(errors[-3:]) if errors else "Aucune police trouvée"
    return None

def get_cjk_font_status():
    """Retourne le statut de la police CJK pour le diagnostic"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    embedded_font = os.path.join(script_dir, 'fonts', 'ipag.ttf')
    
    status = {
        'font_name': _CJK_FONT_NAME,
        'initialized': _CJK_FONT_INITIALIZED,
        'embedded_path': embedded_font,
        'embedded_exists': os.path.exists(embedded_font),
        'error': _CJK_FONT_ERROR,
        'char_image_available': CHAR_IMAGE_AVAILABLE,
    }
    
    if os.path.exists(embedded_font):
        status['embedded_size'] = os.path.getsize(embedded_font)
    
    return status

def draw_cjk_character(canvas, x, y, char, font_size, color, cjk_font=None, fallback_text=None, hex_numero=None, is_mutation=False):
    """
    Dessine un caractère chinois dans le PDF.
    Priorité: 1) Image pré-générée, 2) Police ReportLab, 3) Image PIL, 4) Texte fallback
    
    Args:
        canvas: ReportLab canvas
        x, y: Position (centrée)
        char: Le caractère chinois
        font_size: Taille de police souhaitée
        color: Couleur (HexColor)
        cjk_font: Nom de la police CJK (ou None)
        fallback_text: Texte à afficher si tout échoue (ex: "#8")
        hex_numero: Numéro de l'hexagramme (pour trouver l'image pré-générée)
        is_mutation: Si True, utilise les images violettes
    
    Returns:
        True si succès, False sinon
    """
    from reportlab.lib.utils import ImageReader
    import os
    
    # Obtenir le chemin du script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Méthode 1: Utiliser l'image pré-générée (la plus fiable)
    if hex_numero:
        # Choisir le dossier selon le contexte
        if is_mutation:
            img_folder = 'char_images_mutation'
        else:
            img_folder = 'char_images'
        
        char_img_path = os.path.join(script_dir, img_folder, f'hex_{hex_numero:02d}.png')
        if os.path.exists(char_img_path):
            try:
                img_reader = ImageReader(char_img_path)
                img_width = font_size * 1.2
                img_height = font_size * 1.2
                canvas.drawImage(img_reader, x - img_width/2, y - img_height/3, 
                               width=img_width, height=img_height, 
                               preserveAspectRatio=True, mask='auto')
                return True
            except Exception as e:
                pass  # Continuer avec les autres méthodes
    
    # Méthode 2: Essayer avec la police CJK ReportLab
    if cjk_font and char:
        try:
            canvas.setFont(cjk_font, font_size)
            canvas.setFillColor(color)
            canvas.drawCentredString(x, y, char)
            return True
        except Exception as e:
            pass  # Continuer avec le fallback
    
    # Méthode 3: Utiliser une image générée avec PIL
    embedded_font_path = os.path.join(script_dir, 'fonts', 'ipag.ttf')
    if CHAR_IMAGE_AVAILABLE and char:
        try:
            if hasattr(color, 'hexval'):
                color_hex = '#' + color.hexval()[2:]
            else:
                color_hex = '#8B4513'
            
            img_buffer = create_character_image(
                char, 
                size=int(font_size * 1.5), 
                color=color_hex,
                font_path=embedded_font_path
            )
            if img_buffer:
                img_reader = ImageReader(img_buffer)
                img_width = font_size * 1.2
                img_height = font_size * 1.2
                canvas.drawImage(img_reader, x - img_width/2, y - img_height/3, 
                               width=img_width, height=img_height, 
                               preserveAspectRatio=True, mask='auto')
                return True
        except Exception as e:
            pass  # Continuer avec le fallback
    
    # Méthode 4: Afficher le texte de fallback
    if fallback_text:
        canvas.setFont("Helvetica-Bold", font_size * 0.8)
        canvas.setFillColor(color)
        canvas.drawCentredString(x, y, fallback_text)
        return True
    
    return False

def draw_text_box(c, x, y, width, height, title, content, title_color, bg_color, text_color):
    """Dessine une boîte de texte avec titre"""
    from reportlab.lib.colors import HexColor
    
    c.setFillColor(bg_color)
    c.setStrokeColor(title_color)
    c.setLineWidth(1.5)
    c.roundRect(x, y, width, height, 4, fill=1, stroke=1)
    
    c.setFillColor(title_color)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 4*mm, y + height - 6*mm, title)
    
    c.setFillColor(text_color)
    c.setFont("Helvetica", 7)
    
    lines = textwrap.wrap(content, int(width / 2))
    text_y = y + height - 12*mm
    for line in lines:
        if text_y < y + 4*mm:
            break
        c.drawString(x + 4*mm, text_y, line)
        text_y -= 3.5*mm

def generate_pdf_report_complete(traits, question, hex_data, hex_mute_data, grille_img, grille_mut_img=None, lang='fr'):
    """Génère un rapport PDF complet multi-pages avec support multilingue"""
    buffer = BytesIO()
    width, height = A4
    margin = 15 * mm
    c = canvas.Canvas(buffer, pagesize=A4)
    
    cjk_font = init_cjk_font()
    
    # Couleurs
    marron = HexColor('#8B4513')
    or_color = HexColor('#DAA520')
    creme = HexColor('#FFFAF0')
    gris = HexColor('#4A4A4A')  # Gris neutre pour meilleure lisibilité
    rouge = HexColor('#C62828')
    bleu = HexColor('#1565C0')
    vert = HexColor('#2E7D32')
    orange = HexColor('#E65100')
    violet = HexColor('#7B1FA2')
    
    hex_numero = get_hexagramme_numero(traits)
    hex_mute_numero = get_mutation_numero(traits)
    
    # ==========================================================================
    # PAGE 1 : HEXAGRAMME PRINCIPAL
    # ==========================================================================
    
    # En-tête
    c.setFillColor(marron)
    c.rect(0, height - 35*mm, width, 35*mm, fill=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 14*mm, "易經 Yi Jing Oracle")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 22*mm, t('pdf_title', lang))
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, height - 30*mm, datetime.datetime.now().strftime("%d/%m/%Y à %H:%M"))
    
    y = height - 45*mm
    
    # Question
    if question:
        c.setFillColor(HexColor('#FFF8E1'))
        c.setStrokeColor(or_color)
        c.roundRect(margin, y - 15*mm, width - 2*margin, 15*mm, 3, fill=1, stroke=1)
        c.setFillColor(gris)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin + 4*mm, y - 5*mm, t('your_question', lang) + " :")
        c.setFont("Helvetica", 8)
        question_text = (question[:100] + "...") if len(question) > 100 else question
        c.drawString(margin + 4*mm, y - 11*mm, question_text)
        y -= 22*mm
    
    # Carte hexagramme
    c.setFillColor(creme)
    c.setStrokeColor(or_color)
    c.setLineWidth(3)
    c.roundRect(margin, y - 55*mm, width - 2*margin, 55*mm, 8, fill=1, stroke=1)
    
    c.setFillColor(marron)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y - 10*mm, f"{t('hexagram', lang).upper()} {hex_numero}")
    
    # Afficher le caractère chinois (avec fallback automatique)
    caractere = hex_data.get('caractere', '')
    draw_cjk_character(
        canvas=c,
        x=width/2,
        y=y - 32*mm,
        char=caractere,
        font_size=42,
        color=marron,  # Marron pour cohérence avec le thème
        cjk_font=cjk_font,
        fallback_text=f"#{hex_numero}",
        hex_numero=hex_numero
    )
    
    nom = f"{hex_data.get('nom_pinyin', '')} - {get_hex_name(hex_numero, lang)}"
    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, y - 48*mm, nom)
    y -= 65*mm
    
    # Trigrammes
    trig_haut = hex_data.get('trigramme_haut', '')
    trig_bas = hex_data.get('trigramme_bas', '')
    trig_h_info = TRIGRAMMES.get(trig_haut, {})
    trig_b_info = TRIGRAMMES.get(trig_bas, {})
    
    c.setFillColor(HexColor('#E3F2FD'))
    c.setStrokeColor(bleu)
    c.setLineWidth(1)
    c.roundRect(margin, y - 25*mm, (width - 2*margin - 5*mm)/2, 25*mm, 3, fill=1, stroke=1)
    c.roundRect(margin + (width - 2*margin + 5*mm)/2, y - 25*mm, (width - 2*margin - 5*mm)/2, 25*mm, 3, fill=1, stroke=1)
    
    c.setFillColor(bleu)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin + 4*mm, y - 6*mm, f"☰ {t('upper_trigram', lang)}")
    c.setFont("Helvetica", 8)
    c.setFillColor(gris)
    c.drawString(margin + 4*mm, y - 12*mm, f"{trig_h_info.get('symbole', '')} {trig_haut} - {trig_h_info.get('element', '')}")
    c.drawString(margin + 4*mm, y - 17*mm, f"{trig_h_info.get('freq', 0)} Hz - {hex_data.get('trigramme_haut_desc', '')[:35]}")
    c.drawString(margin + 4*mm, y - 22*mm, f"{t('nature', lang)}: {trig_h_info.get('nature', '')}")
    
    c.setFillColor(bleu)
    c.setFont("Helvetica-Bold", 9)
    tx = margin + (width - 2*margin + 5*mm)/2 + 4*mm
    c.drawString(tx, y - 6*mm, f"☷ {t('lower_trigram', lang)}")
    c.setFont("Helvetica", 8)
    c.setFillColor(gris)
    c.drawString(tx, y - 12*mm, f"{trig_b_info.get('symbole', '')} {trig_bas} - {trig_b_info.get('element', '')}")
    c.drawString(tx, y - 17*mm, f"{trig_b_info.get('freq', 0)} Hz - {hex_data.get('trigramme_bas_desc', '')[:35]}")
    c.drawString(tx, y - 22*mm, f"{t('nature', lang)}: {trig_b_info.get('nature', '')}")
    y -= 32*mm
    
    # Traits tirés
    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, t('traits_frequencies', lang) + " :")
    y -= 6*mm
    
    for i in range(5, -1, -1):
        trait_val = traits[i]
        info = FREQ_TRAITS[trait_val]
        is_mutant = trait_val in [6, 9]
        
        if is_mutant:
            c.setFillColor(HexColor('#E0E0E0'))  # Gris clair pour meilleur contraste
            c.setStrokeColor(rouge)
        else:
            c.setFillColor(white)
            c.setStrokeColor(HexColor('#BDBDBD'))
        c.setLineWidth(0.5)
        c.roundRect(margin, y - 7*mm, width - 2*margin, 7*mm, 2, fill=1, stroke=1)
        
        c.setFillColor(rouge if is_mutant else gris)
        c.setFont("Helvetica-Bold" if is_mutant else "Helvetica", 8)
        symbole = info['symbole']
        mut = " ← MUTANT" if is_mutant else ""
        c.drawString(margin + 3*mm, y - 5*mm, f"Trait {i+1}: {symbole}  |  {info['nom']}  |  {info['freq']} Hz ({info['note']}){mut}")
        y -= 8*mm
    
    y -= 5*mm
    
    # Grille
    if grille_img:
        c.setFillColor(violet)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, y, f"{t('hermes_grid', lang)} :")
        y -= 3*mm
        
        img_buffer = BytesIO()
        grille_img.save(img_buffer, 'PNG')
        img_buffer.seek(0)
        from reportlab.lib.utils import ImageReader
        img_reader = ImageReader(img_buffer)
        
        grille_width = 50*mm
        grille_height = 65*mm
        c.drawImage(img_reader, margin, y - grille_height, width=grille_width, height=grille_height, preserveAspectRatio=True)
        
        # Description à côté
        text_x = margin + grille_width + 8*mm
        text_y = y - 5*mm
        c.setFillColor(gris)
        c.setFont("Helvetica", 7)
        desc = hex_data.get('description', '')
        if desc:
            lines = textwrap.wrap(desc, 55)
            for line in lines[:16]:
                c.drawString(text_x, text_y, line)
                text_y -= 3.5*mm
    
    # Footer
    c.setFillColor(HexColor('#9E9E9E'))
    c.setFont("Helvetica", 6)
    c.drawCentredString(width/2, 8*mm, f"Yi Jing Oracle v2.2 - {t('footer_credit', lang)} | {t('grids_credit', lang)} | {t('page', lang)} 1")
    
    # ==========================================================================
    # PAGE 2 : JUGEMENT ET IMAGE
    # ==========================================================================
    c.showPage()
    y = height - 20*mm
    
    c.setFillColor(marron)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y, f"{t('hexagram', lang)} {hex_numero} - {t('traditional_texts', lang)}")
    y -= 15*mm
    
    # Le Jugement
    jugement = hex_data.get('jugement_texte', '')
    if jugement:
        c.setFillColor(HexColor('#FFF3E0'))
        c.setStrokeColor(orange)
        c.setLineWidth(2)
        jug_lines = textwrap.wrap(jugement, 90)
        box_height = min(len(jug_lines) * 4 + 15, 80) * mm
        c.roundRect(margin, y - box_height, width - 2*margin, box_height, 5, fill=1, stroke=1)
        
        c.setFillColor(orange)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin + 5*mm, y - 8*mm, t('judgment', lang).upper())
        
        c.setFillColor(gris)
        c.setFont("Helvetica", 8)
        text_y = y - 16*mm
        for line in jug_lines[:15]:
            c.drawString(margin + 5*mm, text_y, line)
            text_y -= 4*mm
        y -= box_height + 8*mm
    else:
        # Message quand le texte est manquant
        c.setFillColor(HexColor('#FFF3E0'))
        c.setStrokeColor(orange)
        c.setLineWidth(1)
        c.roundRect(margin, y - 25*mm, width - 2*margin, 25*mm, 5, fill=1, stroke=1)
        c.setFillColor(orange)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin + 5*mm, y - 8*mm, t('judgment', lang).upper())
        c.setFillColor(gris)
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(margin + 5*mm, y - 18*mm, t('judgment_not_available', lang))
        c.drawString(margin + 5*mm, y - 23*mm, t('consult_complete', lang))
        y -= 33*mm
    
    # L'Image
    image_texte = hex_data.get('image_texte', '')
    if image_texte:
        c.setFillColor(HexColor('#E3F2FD'))
        c.setStrokeColor(bleu)
        c.setLineWidth(2)
        img_lines = textwrap.wrap(image_texte, 90)
        box_height = min(len(img_lines) * 4 + 15, 60) * mm
        c.roundRect(margin, y - box_height, width - 2*margin, box_height, 5, fill=1, stroke=1)
        
        c.setFillColor(bleu)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin + 5*mm, y - 8*mm, t('image', lang).upper())
        
        c.setFillColor(gris)
        c.setFont("Helvetica", 8)
        text_y = y - 16*mm
        for line in img_lines[:12]:
            c.drawString(margin + 5*mm, text_y, line)
            text_y -= 4*mm
        y -= box_height + 8*mm
    else:
        # Message quand le texte est manquant
        c.setFillColor(HexColor('#E3F2FD'))
        c.setStrokeColor(bleu)
        c.setLineWidth(1)
        c.roundRect(margin, y - 25*mm, width - 2*margin, 25*mm, 5, fill=1, stroke=1)
        c.setFillColor(bleu)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin + 5*mm, y - 8*mm, t('image', lang).upper())
        c.setFillColor(gris)
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(margin + 5*mm, y - 18*mm, t('image_not_available', lang))
        c.drawString(margin + 5*mm, y - 23*mm, t('consult_complete', lang))
        y -= 33*mm
    
    # Interprétation générale
    c.setFillColor(HexColor('#F3E5F5'))
    c.setStrokeColor(violet)
    c.setLineWidth(1.5)
    c.roundRect(margin, y - 45*mm, width - 2*margin, 45*mm, 4, fill=1, stroke=1)
    
    c.setFillColor(violet)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin + 5*mm, y - 8*mm, t('general_interpretation', lang))
    
    c.setFillColor(gris)
    c.setFont("Helvetica", 8)
    
    has_mutation = any(tv in [6, 9] for tv in traits)
    nb_mutants = sum(1 for tv in traits if tv in [6, 9])
    
    interp_lines = []
    interp_lines.append(f"{t('hexagram_obtained', lang)}: {hex_numero} - {get_hex_name(hex_numero, lang)}")
    interp_lines.append(f"{t('combination', lang)}: {trig_haut} ({trig_h_info.get('element', '')}) {t('on', lang)} {trig_bas} ({trig_b_info.get('element', '')})")
    
    if has_mutation:
        interp_lines.append(f"")
        interp_lines.append(f"*** {nb_mutants} {t('mutant_traits_detected', lang)}")
        interp_lines.append(f"{t('evolves_to', lang)}{hex_mute_numero}: {get_hex_name(hex_mute_numero, lang)}")
        interp_lines.append(t('read_mutant_traits', lang))
    else:
        interp_lines.append(f"")
        interp_lines.append(f"✓ {t('no_mutant_stable', lang)}")
        interp_lines.append(t('message_applies', lang))
    
    text_y = y - 16*mm
    for line in interp_lines:
        c.drawString(margin + 5*mm, text_y, line)
        text_y -= 4*mm
    
    c.setFillColor(HexColor('#9E9E9E'))
    c.setFont("Helvetica", 6)
    c.drawCentredString(width/2, 8*mm, f"{t('page', lang)} 2")
    
    # ==========================================================================
    # PAGE 3 : TOUS LES TRAITS
    # ==========================================================================
    c.showPage()
    y = height - 20*mm
    
    c.setFillColor(marron)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y, f"Les Six Traits de l'Hexagramme {hex_numero}")
    y -= 12*mm
    
    hex_traits = hex_data.get('traits', [])
    
    for i in range(6):
        trait_val = traits[i]
        is_mutant = trait_val in [6, 9]
        trait_data = next((t for t in hex_traits if t.get('position') == i + 1), None)
        
        # Couleur de la boîte selon le type
        if is_mutant:
            bg_color = HexColor('#E0E0E0')  # Gris clair pour meilleur contraste
            border_color = rouge
        elif trait_val == 7:
            bg_color = HexColor('#E8F5E9')
            border_color = vert
        else:
            bg_color = HexColor('#E3F2FD')
            border_color = bleu
        
        box_height = 38*mm
        if y - box_height < 25*mm:
            c.showPage()
            y = height - 20*mm
        
        # Définir les couleurs APRÈS le potentiel showPage()
        c.setFillColor(bg_color)
        c.setStrokeColor(border_color)
        c.setLineWidth(1.5)
        
        c.roundRect(margin, y - box_height, width - 2*margin, box_height, 4, fill=1, stroke=1)
        
        # Titre du trait
        c.setFillColor(border_color)
        c.setFont("Helvetica-Bold", 9)
        info = FREQ_TRAITS[trait_val]
        trait_title = f"TRAIT {i+1} - {info['symbole']} - {info['nom'].upper()}"
        if is_mutant:
            trait_title += " 🔄"
        c.drawString(margin + 5*mm, y - 7*mm, trait_title)
        
        # Fréquence
        c.setFont("Helvetica", 7)
        c.drawString(width - margin - 40*mm, y - 7*mm, f"{info['freq']} Hz ({info['note']})")
        
        if trait_data:
            c.setFillColor(gris)
            c.setFont("Helvetica-Bold", 8)
            titre = trait_data.get('titre', f'Trait {i+1}')
            c.drawString(margin + 5*mm, y - 14*mm, titre)
            
            c.setFont("Helvetica", 7)
            texte = trait_data.get('texte', '')
            lines = textwrap.wrap(texte, 100)
            text_y = y - 20*mm
            for line in lines[:5]:
                c.drawString(margin + 5*mm, text_y, line)
                text_y -= 3.5*mm
        
        y -= box_height + 3*mm
    
    c.setFillColor(HexColor('#9E9E9E'))
    c.setFont("Helvetica", 6)
    c.drawCentredString(width/2, 8*mm, "Page 3")
    
    # ==========================================================================
    # PAGE 4 : TRAITS MUTANTS (si présents)
    # ==========================================================================
    traits_mutants = [(i, traits[i]) for i in range(6) if traits[i] in [6, 9]]
    
    if traits_mutants:
        c.showPage()
        y = height - 20*mm
        
        c.setFillColor(rouge)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width/2, y, "*** TRAITS MUTANTS - À lire attentivement")
        y -= 8*mm
        
        c.setFillColor(gris)
        c.setFont("Helvetica", 9)
        c.drawCentredString(width/2, y, f"Ces {len(traits_mutants)} trait(s) indiquent les aspects de la situation en transformation")
        y -= 15*mm
        
        for pos, val in traits_mutants:
            trait_data = next((t for t in hex_traits if t.get('position') == pos + 1), None)
            
            box_height = 50*mm
            if y - box_height < 30*mm:
                c.showPage()
                y = height - 20*mm
            
            # Définir les couleurs APRÈS le potentiel showPage()
            c.setFillColor(HexColor('#F5F5F5'))  # Gris très clair pour le fond
            c.setStrokeColor(rouge)
            c.setLineWidth(2)
            
            c.roundRect(margin, y - box_height, width - 2*margin, box_height, 5, fill=1, stroke=1)
            
            info = FREQ_TRAITS[val]
            c.setFillColor(rouge)
            c.setFont("Helvetica-Bold", 11)
            mutation_dir = "Yin → Yang" if val == 6 else "Yang → Yin"
            c.drawString(margin + 5*mm, y - 9*mm, f"TRAIT {pos + 1} MUTANT - {info['nom']} ({mutation_dir})")
            
            if trait_data:
                c.setFillColor(HexColor('#B71C1C'))
                c.setFont("Helvetica-Bold", 9)
                titre = trait_data.get('titre', '')
                c.drawString(margin + 5*mm, y - 18*mm, titre)
                
                c.setFillColor(gris)
                c.setFont("Helvetica", 8)
                texte = trait_data.get('texte', '')
                lines = textwrap.wrap(texte, 95)
                text_y = y - 26*mm
                for line in lines[:6]:
                    c.drawString(margin + 5*mm, text_y, line)
                    text_y -= 4*mm
            
            y -= box_height + 5*mm
        
        c.setFillColor(HexColor('#9E9E9E'))
        c.setFont("Helvetica", 6)
        c.drawCentredString(width/2, 8*mm, "Page 4")
    
    # ==========================================================================
    # PAGE 5 : HEXAGRAMME DE MUTATION (si présent)
    # ==========================================================================
    if hex_mute_numero and hex_mute_data:
        c.showPage()
        y = height - 20*mm
        
        c.setFillColor(violet)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width/2, y, f"🔄 MUTATION VERS HEXAGRAMME {hex_mute_numero}")
        y -= 15*mm
        
        # Carte mutation
        c.setFillColor(HexColor('#F3E5F5'))
        c.setStrokeColor(violet)
        c.setLineWidth(3)
        c.roundRect(margin, y - 50*mm, width - 2*margin, 50*mm, 8, fill=1, stroke=1)
        
        c.setFillColor(violet)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width/2, y - 10*mm, f"HEXAGRAMME {hex_mute_numero}")
        
        # Afficher le caractère chinois de mutation (avec fallback automatique)
        car_mut = hex_mute_data.get('caractere', '')
        draw_cjk_character(
            canvas=c,
            x=width/2,
            y=y - 28*mm,
            char=car_mut,
            font_size=36,
            color=HexColor('#4A148C'),
            cjk_font=cjk_font,
            fallback_text=f"#{hex_mute_numero}",
            hex_numero=hex_mute_numero,
            is_mutation=True
        )
        
        nom_mut = f"{hex_mute_data.get('nom_pinyin', '')} - {get_hex_name(hex_mute_numero, lang)}"
        c.setFillColor(gris)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(width/2, y - 43*mm, nom_mut)
        y -= 60*mm
        
        # Grille mutation
        if grille_mut_img:
            c.setFillColor(violet)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(margin, y, "Grille après mutation :")
            y -= 3*mm
            
            img_buffer = BytesIO()
            grille_mut_img.save(img_buffer, 'PNG')
            img_buffer.seek(0)
            from reportlab.lib.utils import ImageReader
            img_reader = ImageReader(img_buffer)
            c.drawImage(img_reader, margin, y - 65*mm, width=50*mm, height=65*mm, preserveAspectRatio=True)
            
            # Description mutation
            text_x = margin + 55*mm
            text_y = y - 5*mm
            c.setFillColor(gris)
            c.setFont("Helvetica", 7)
            desc_mut = hex_mute_data.get('description', '')
            if desc_mut:
                lines = textwrap.wrap(desc_mut, 55)
                for line in lines[:16]:
                    c.drawString(text_x, text_y, line)
                    text_y -= 3.5*mm
            y -= 70*mm
        
        # Jugement mutation
        jug_mut = hex_mute_data.get('jugement_texte', '')
        if jug_mut and y > 50*mm:
            c.setFillColor(HexColor('#EDE7F6'))
            c.setStrokeColor(violet)
            c.setLineWidth(1.5)
            jug_lines = textwrap.wrap(jug_mut, 90)
            box_height = min(len(jug_lines) * 4 + 12, 50) * mm
            c.roundRect(margin, y - box_height, width - 2*margin, box_height, 4, fill=1, stroke=1)
            
            c.setFillColor(violet)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(margin + 5*mm, y - 7*mm, "Jugement de l'hexagramme de mutation")
            
            c.setFillColor(gris)
            c.setFont("Helvetica", 7)
            text_y = y - 14*mm
            for line in jug_lines[:10]:
                c.drawString(margin + 5*mm, text_y, line)
                text_y -= 3.5*mm
        
        c.setFillColor(HexColor('#9E9E9E'))
        c.setFont("Helvetica", 6)
        c.drawCentredString(width/2, 8*mm, "Page 5")
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# ============================================================================
# CSS AVEC ANIMATIONS
# ============================================================================

st.markdown("""
<style>
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.3);
    }
    
    /* Carte hexagramme */
    .hex-card {
        background: linear-gradient(135deg, #FFFAF0 0%, #FFF8DC 100%);
        border: 3px solid #DAA520;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(218, 165, 32, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .hex-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(218, 165, 32, 0.3);
    }
    .hex-caractere { font-size: 4rem; color: #2F4F4F; }
    .hex-nom { font-size: 1.3rem; color: #8B4513; font-weight: bold; }
    
    /* Traits */
    .trait-box {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.2rem;
        border-radius: 10px;
        font-family: monospace;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    .trait-box:hover {
        transform: scale(1.02);
    }
    .trait-yang { background: #E8F5E9; border: 2px solid #4CAF50; }
    .trait-yin { background: #E3F2FD; border: 2px solid #2196F3; }
    .trait-yang-mut { background: #FFF3E0; border: 2px solid #FF9800; animation: pulse-orange 2s infinite; }
    .trait-yin-mut { background: #FCE4EC; border: 2px solid #E91E63; animation: pulse-pink 2s infinite; }
    
    @keyframes pulse-orange {
        0%, 100% { box-shadow: 0 0 0 0 rgba(255, 152, 0, 0.4); }
        50% { box-shadow: 0 0 0 8px rgba(255, 152, 0, 0); }
    }
    @keyframes pulse-pink {
        0%, 100% { box-shadow: 0 0 0 0 rgba(233, 30, 99, 0.4); }
        50% { box-shadow: 0 0 0 8px rgba(233, 30, 99, 0); }
    }
    
    /* Carte mutation */
    .mutation-card {
        background: linear-gradient(135deg, #FCE4EC 0%, #F8BBD9 100%);
        border: 3px solid #E91E63;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        animation: glow-mutation 3s ease-in-out infinite;
    }
    @keyframes glow-mutation {
        0%, 100% { box-shadow: 0 0 5px rgba(233, 30, 99, 0.3); }
        50% { box-shadow: 0 0 20px rgba(233, 30, 99, 0.5); }
    }
    
    /* Container animation grilles */
    .grille-container {
        position: relative;
        width: 100%;
        height: 400px;
        overflow: hidden;
        border-radius: 15px;
        background: #f5f5f5;
    }
    
    .grille-slide {
        position: absolute;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: all 0.8s ease-in-out;
    }
    
    .grille-slide img {
        max-height: 380px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .grille-active {
        opacity: 1;
        transform: translateX(0);
    }
    
    .grille-inactive-left {
        opacity: 0;
        transform: translateX(-100%);
    }
    
    .grille-inactive-right {
        opacity: 0;
        transform: translateX(100%);
    }
    
    /* Animation crossfade */
    .crossfade-container {
        position: relative;
        width: 100%;
        min-height: 350px;
    }
    
    .crossfade-img {
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        transition: opacity 1.5s ease-in-out;
    }
    
    .crossfade-visible { opacity: 1; z-index: 2; }
    .crossfade-hidden { opacity: 0; z-index: 1; }
    
    /* Boutons navigation grilles */
    .grille-nav {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .grille-nav-btn {
        padding: 0.5rem 1.5rem;
        border: none;
        border-radius: 25px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .grille-nav-btn-active {
        background: #8B4513;
        color: white;
    }
    
    .grille-nav-btn-inactive {
        background: #e0e0e0;
        color: #666;
    }
    
    /* Boîtes de texte */
    .text-box {
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        transition: all 0.3s ease;
    }
    .text-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    }
    
    .jugement-box {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        border-left: 5px solid #FF9800;
    }
    
    .image-box {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border-left: 5px solid #2196F3;
    }
    
    .trait-text-box {
        background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%);
        border-left: 5px solid #9C27B0;
    }
    
    .trait-mutant-box {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        border-left: 5px solid #E91E63;
        animation: pulse-border 2s infinite;
    }
    
    @keyframes pulse-border {
        0%, 100% { border-left-color: #E91E63; }
        50% { border-left-color: #F48FB1; }
    }
    
    /* Kasina box */
    .kasina-box {
        background: linear-gradient(135deg, #E8EAF6 0%, #C5CAE9 100%);
        border: 2px solid #3F51B5;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Phase items */
    .phase-item {
        display: flex;
        align-items: center;
        margin: 6px 0;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #3F51B5;
        transition: all 0.3s ease;
    }
    .phase-item:hover {
        background: #e8eaf6;
        transform: translateX(5px);
    }
    
    .phase-color {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        margin-right: 15px;
        border: 2px solid white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* Fleche mutation */
    .mutation-arrow {
        font-size: 3rem;
        color: #E91E63;
        animation: arrow-pulse 1.5s ease-in-out infinite;
        text-align: center;
        margin: 1rem 0;
    }
    @keyframes arrow-pulse {
        0%, 100% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.2); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# APPLICATION PRINCIPALE
# ============================================================================

if 'traits' not in st.session_state:
    st.session_state.traits = None
if 'question' not in st.session_state:
    st.session_state.question = ""
if 'grille_view' not in st.session_state:
    st.session_state.grille_view = 'principal'
if 'lang' not in st.session_state:
    st.session_state.lang = 'fr'

# Fonction pour obtenir la langue courante
def get_lang():
    return st.session_state.get('lang', 'fr')

# Header
st.markdown(f"""
<div class="main-header">
    <h1>{t('app_title', get_lang())} v2.2</h1>
    <p>{t('app_subtitle', get_lang())}</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Sélecteur de langue en haut
    lang_options = list(LANGUAGES.keys())
    lang_labels = list(LANGUAGES.values())
    current_idx = lang_options.index(get_lang()) if get_lang() in lang_options else 0
    
    selected_lang = st.selectbox(
        t('language', get_lang()),
        options=lang_options,
        format_func=lambda x: LANGUAGES[x],
        index=current_idx,
        key="lang_selector"
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()
    
    lang = get_lang()
    
    st.divider()
    st.header(t('sidebar_title', lang))
    question = st.text_area(
        t('your_question', lang), 
        placeholder=t('question_placeholder', lang), 
        height=100
    )
    st.divider()
    
    mode_random = "🎲 " + ("Tirage aléatoire" if lang == "fr" else "Random" if lang == "en" else "Zufall" if lang == "de" else "Aleatorio" if lang == "es" else "随机")
    mode_manual = "✏️ " + ("Saisie manuelle" if lang == "fr" else "Manual" if lang == "en" else "Manuell" if lang == "de" else "Manual" if lang == "es" else "手动")
    mode = st.radio("Mode :", [mode_random, mode_manual])
    
    if mode == mode_manual:
        st.caption("Traits (6=Yin mut, 7=Yang, 8=Yin, 9=Yang mut)")
        cols = st.columns(6)
        manual_traits = []
        for i, col in enumerate(cols):
            with col:
                tr = st.selectbox(f"{i+1}", [6, 7, 8, 9], index=1, key=f"t{i}")
                manual_traits.append(tr)
    
    st.divider()
    
    if st.button(t('throw_coins', lang), type="primary", use_container_width=True):
        st.session_state.question = question
        if mode == mode_random:
            st.session_state.traits = [tirer_trait() for _ in range(6)]
        else:
            st.session_state.traits = manual_traits
        st.session_state.grille_view = 'principal'
    
    st.divider()
    json_path = st.text_input("📄 JSON :", value="yijing_complet.json")
    images_dir = st.text_input("📁 Images :", value="images")
    
    # Diagnostic police CJK
    with st.expander(t('diagnostic_title', lang)):
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Vérifier les images pré-générées (marron)
        char_images_dir = os.path.join(script_dir, 'char_images')
        if os.path.exists(char_images_dir):
            num_images = len([f for f in os.listdir(char_images_dir) if f.endswith('.png')])
            if num_images >= 64:
                st.success(f"✓ {t('images_brown', lang)}: {num_images}/64")
            else:
                st.warning(f"⚠ {t('images_brown', lang)}: {num_images}/64")
        else:
            st.error(f"✗ {t('folder_missing', lang)}: char_images")
        
        # Vérifier les images mutation (violet)
        char_mut_dir = os.path.join(script_dir, 'char_images_mutation')
        if os.path.exists(char_mut_dir):
            num_mut = len([f for f in os.listdir(char_mut_dir) if f.endswith('.png')])
            if num_mut >= 64:
                st.success(f"✓ {t('images_purple', lang)}: {num_mut}/64")
            else:
                st.warning(f"⚠ {t('images_purple', lang)}: {num_mut}/64")
        else:
            st.warning(f"⚠ {t('folder_missing', lang)}: char_images_mutation")
        
        # Forcer l'initialisation pour avoir le diagnostic
        init_cjk_font()
        cjk_status = get_cjk_font_status()
        
        if cjk_status['font_name']:
            st.info(f"{t('reportlab_font', lang)}: {cjk_status['font_name']}")
        else:
            st.caption(f"{t('reportlab_font', lang)}: {t('not_available', lang)}")
        
        st.caption(f"{t('embedded_font', lang)}: {cjk_status['embedded_exists']}")
        if cjk_status.get('embedded_size'):
            st.caption(f"{t('size', lang)}: {cjk_status['embedded_size'] / 1024 / 1024:.1f} MB")

# Charger données dans la langue courante
lang = get_lang()
yijing_data = load_yijing_data(json_path, lang)

# Contenu principal
if st.session_state.traits is not None:
    traits = st.session_state.traits
    hex_numero = get_hexagramme_numero(traits)
    hex_mute_numero = get_mutation_numero(traits)
    hex_data = get_hex_from_json(yijing_data, hex_numero)
    hex_mute_data = get_hex_from_json(yijing_data, hex_mute_numero) if hex_mute_numero else {}
    
    # =========================================================================
    # SECTION 1 : HEXAGRAMME ET TRAITS
    # =========================================================================
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        caractere = hex_data.get('caractere', '')
        nom_pinyin = hex_data.get('nom_pinyin', '')
        nom_traduit = get_hex_name(hex_numero, lang)
        
        st.markdown(f"""
        <div class="hex-card">
            <div style="font-size: 0.9rem; color: #8B4513; letter-spacing: 2px;">{t('hexagram', lang).upper()} {hex_numero}</div>
            <div class="hex-caractere">{caractere}</div>
            <div class="hex-nom">{nom_pinyin}</div>
            <div style="font-size: 1.1rem; color: #5D4037; font-style: italic;">{nom_traduit}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Trigrammes
        trig_haut = hex_data.get('trigramme_haut', '')
        trig_bas = hex_data.get('trigramme_bas', '')
        trig_h_info = TRIGRAMMES.get(trig_haut, {})
        trig_b_info = TRIGRAMMES.get(trig_bas, {})
        
        st.markdown(f"#### ☯ {t('upper_trigram', lang)} / {t('lower_trigram', lang)}")
        tcol1, tcol2 = st.columns(2)
        with tcol1:
            st.markdown(f"""
            **{trig_h_info.get('symbole', '')} {t('upper_trigram', lang)}**  
            {trig_haut} ({trig_h_info.get('element', '')})  
            *{trig_h_info.get('freq', 0)} Hz*  
            {hex_data.get('trigramme_haut_desc', '')[:40]}...
            """)
        with tcol2:
            st.markdown(f"""
            **{trig_b_info.get('symbole', '')} {t('lower_trigram', lang)}**  
            {trig_bas} ({trig_b_info.get('element', '')})  
            *{trig_b_info.get('freq', 0)} Hz*  
            {hex_data.get('trigramme_bas_desc', '')[:40]}...
            """)
    
    with col2:
        st.markdown(f"#### 📊 {t('traits_frequencies', lang)}")
        
        nb_mutants = sum(1 for tv in traits if tv in [6, 9])
        if nb_mutants > 0:
            st.warning(f"*** {nb_mutants} {t('mutant_traits_detected', lang)}")
        
        for i in range(5, -1, -1):
            trait_val = traits[i]
            info = FREQ_TRAITS[trait_val]
            is_yang = trait_val in [7, 9]
            is_mut = trait_val in [6, 9]
            
            if is_yang and is_mut:
                classe = "trait-yang-mut"
            elif is_yang:
                classe = "trait-yang"
            elif is_mut:
                classe = "trait-yin-mut"
            else:
                classe = "trait-yin"
            
            mut_icon = " 🔄" if is_mut else ""
            st.markdown(f"""
            <div class="trait-box {classe}">
                <strong>{i+1}</strong> {info['symbole']} | {info['nom']} | {info['freq']} Hz{mut_icon}
            </div>
            """, unsafe_allow_html=True)
        
        # Carte mutation
        if hex_mute_numero:
            st.markdown('<div class="mutation-arrow">⬇️</div>', unsafe_allow_html=True)
            car_mut = hex_mute_data.get('caractere', '')
            nom_mut_traduit = get_hex_name(hex_mute_numero, lang)
            st.markdown(f"""
            <div class="mutation-card">
                <div style="font-size: 0.85rem; letter-spacing: 1px;">🔄 {t('mutation_to', lang)}</div>
                <div style="font-size: 2.8rem;">{car_mut}</div>
                <div style="font-weight: bold; font-size: 1.1rem;">{hex_mute_numero}. {hex_mute_data.get('nom_pinyin', '')}</div>
                <div style="font-style: italic;">{nom_mut_traduit}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # =========================================================================
    # SECTION 2 : GRILLES AVEC ANIMATION
    # =========================================================================
    
    st.markdown("### 🎮 Grilles La Livrée d'Hermès")
    
    images_path = Path(images_dir)
    
    if images_path.exists():
        grille = generer_grille(traits, images_path, mutation=False)
        grille_mut = generer_grille(traits, images_path, mutation=True) if hex_mute_numero else None
        
        if grille:
            # Boutons de navigation
            if hex_mute_numero and grille_mut:
                nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
                with nav_col2:
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button(f"☯ Hex {hex_numero} Principal", 
                                    type="primary" if st.session_state.grille_view == 'principal' else "secondary",
                                    use_container_width=True):
                            st.session_state.grille_view = 'principal'
                    with btn_col2:
                        if st.button(f"🔄 Hex {hex_mute_numero} Mutation",
                                    type="primary" if st.session_state.grille_view == 'mutation' else "secondary",
                                    use_container_width=True):
                            st.session_state.grille_view = 'mutation'
                
                # Affichage avec animation CSS
                grille_b64 = image_to_base64(grille)
                grille_mut_b64 = image_to_base64(grille_mut)
                
                if st.session_state.grille_view == 'principal':
                    current_img = grille_b64
                    current_title = f"{t('hexagram', lang)} {hex_numero} - {get_hex_name(hex_numero, lang)}"
                else:
                    current_img = grille_mut_b64
                    current_title = f"{t('mutation_to', lang)} {hex_mute_numero} - {get_hex_name(hex_mute_numero, lang)}"
                
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <p style="font-weight: bold; color: #8B4513; margin-bottom: 1rem;">{current_title}</p>
                    <img src="data:image/png;base64,{current_img}" 
                         style="max-height: 400px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); 
                                transition: all 0.5s ease-in-out;"
                         alt="Grille Yi Jing">
                </div>
                """, unsafe_allow_html=True)
                
                # Auto-animation toggle
                auto_label = "🔄 Auto (2s)" if lang != "zh" else "🔄 自动 (2s)"
                if st.checkbox(auto_label, value=False):
                    time.sleep(2)
                    st.session_state.grille_view = 'mutation' if st.session_state.grille_view == 'principal' else 'principal'
                    st.rerun()
            else:
                # Pas de mutation, afficher seulement la grille principale
                grille_b64 = image_to_base64(grille)
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <p style="font-weight: bold; color: #8B4513; margin-bottom: 1rem;">{t('hexagram', lang)} {hex_numero} - {get_hex_name(hex_numero, lang)}</p>
                    <img src="data:image/png;base64,{grille_b64}" 
                         style="max-height: 400px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15);"
                         alt="Grille Yi Jing">
                </div>
                """, unsafe_allow_html=True)
            
            # Téléchargements grilles
            dl_col1, dl_col2 = st.columns(2)
            with dl_col1:
                buf = BytesIO()
                grille.save(buf, format='PNG')
                st.download_button(f"📥 {t('hermes_grid', lang)}", buf.getvalue(), 
                                   f"grille-hex{hex_numero}.png", "image/png")
            with dl_col2:
                if grille_mut:
                    buf = BytesIO()
                    grille_mut.save(buf, format='PNG')
                    st.download_button("📥 Télécharger grille mutation", buf.getvalue(),
                                       f"grille-hex{hex_mute_numero}-mutation.png", "image/png")
    
    st.divider()
    
    # =========================================================================
    # SECTION 3 : TEXTES COMPLETS
    # =========================================================================
    
    st.markdown("### 📜 Textes Traditionnels")
    
    # Description
    desc = hex_data.get('description', '')
    if desc:
        with st.expander("📖 Description de l'hexagramme", expanded=True):
            st.write(desc)
    
    # Jugement
    jugement = hex_data.get('jugement_texte', '')
    if jugement:
        st.markdown(f"""
        <div class="text-box jugement-box">
            <h4 style="color: #E65100; margin-bottom: 0.8rem;">⚖️ LE JUGEMENT</h4>
            <p style="color: #5D4037; line-height: 1.6;">{jugement}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Image
    image_texte = hex_data.get('image_texte', '')
    if image_texte:
        st.markdown(f"""
        <div class="text-box image-box">
            <h4 style="color: #1565C0; margin-bottom: 0.8rem;">🖼️ L'IMAGE</h4>
            <p style="color: #5D4037; line-height: 1.6;">{image_texte}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # =========================================================================
    # SECTION 4 : TOUS LES TRAITS
    # =========================================================================
    
    st.markdown("### 📋 Les Six Traits")
    
    hex_traits = hex_data.get('traits', [])
    
    # Onglets pour les traits
    trait_tabs = st.tabs([f"Trait {i+1}" for i in range(6)])
    
    for i, tab in enumerate(trait_tabs):
        with tab:
            trait_val = traits[i]
            info = FREQ_TRAITS[trait_val]
            is_mutant = trait_val in [6, 9]
            trait_data = next((tr for tr in hex_traits if tr.get('position') == i + 1), None)
            
            box_class = "trait-mutant-box" if is_mutant else "trait-text-box"
            
            if trait_data:
                titre = trait_data.get('titre', f'Trait {i+1}')
                texte = trait_data.get('texte', 'Texte non disponible')
                
                mut_badge = "🔄 MUTANT" if is_mutant else ""
                st.markdown(f"""
                <div class="text-box {box_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-weight: bold; color: {'#C62828' if is_mutant else '#7B1FA2'};">
                            {info['symbole']} {info['nom']} {mut_badge}
                        </span>
                        <span style="color: #666; font-size: 0.9rem;">
                            {info['freq']} Hz ({info['note']})
                        </span>
                    </div>
                    <h4 style="color: #333; margin: 0.5rem 0;">{titre}</h4>
                    <p style="color: #5D4037; line-height: 1.6;">{texte}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info(f"Trait {i+1}: {info['nom']} - {info['freq']} Hz")
    
    # Section traits mutants mis en évidence
    traits_mutants = [(i, traits[i]) for i in range(6) if traits[i] in [6, 9]]
    
    if traits_mutants:
        st.divider()
        st.markdown("### *** Traits Mutants - Attention particulière")
        st.warning("Ces traits indiquent les aspects de votre situation qui sont en transformation. Portez-leur une attention particulière.")
        
        for pos, val in traits_mutants:
            trait_data = next((tr for tr in hex_traits if tr.get('position') == pos + 1), None)
            info = FREQ_TRAITS[val]
            mutation_dir = "Yin → Yang" if val == 6 else "Yang → Yin"
            
            if trait_data:
                with st.container():
                    st.markdown(f"""
                    <div class="text-box trait-mutant-box">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: bold; color: #C62828; font-size: 1.1rem;">
                                TRAIT {pos + 1} - {mutation_dir}
                            </span>
                            <span style="background: #FFCDD2; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.85rem;">
                                {info['freq']} Hz
                            </span>
                        </div>
                        <h4 style="color: #B71C1C; margin: 0.8rem 0;">{trait_data.get('titre', '')}</h4>
                        <p style="color: #5D4037; line-height: 1.7; font-size: 1rem;">{trait_data.get('texte', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # =========================================================================
    # SECTION 5 : HEXAGRAMME DE MUTATION
    # =========================================================================
    
    if hex_mute_numero and hex_mute_data:
        st.divider()
        st.markdown(f"### 🔄 {t('mutation_to', lang)} {hex_mute_numero} - {get_hex_name(hex_mute_numero, lang)}")
        
        desc_label = {"fr": "📖 Description de l'hexagramme de mutation", "en": "📖 Mutation hexagram description", 
                     "de": "📖 Beschreibung des Wandlungshexagramms", "es": "📖 Descripción del hexagrama de mutación",
                     "zh": "📖 变卦描述"}.get(lang, "📖 Description")
        with st.expander(desc_label, expanded=True):
            st.write(hex_mute_data.get('description', ''))
        
        jug_mut = hex_mute_data.get('jugement_texte', '')
        if jug_mut:
            jug_label = t('judgment', lang)
            st.markdown(f"""
            <div class="text-box" style="background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%); border-left: 5px solid #7B1FA2;">
                <h4 style="color: #7B1FA2; margin-bottom: 0.8rem;">⚖️ {jug_label} ({t('mutation_to', lang)})</h4>
                <p style="color: #5D4037; line-height: 1.6;">{jug_mut}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # =========================================================================
    # SECTION 6 : EXPORTS
    # =========================================================================
    
    exports_label = {"fr": "Exports", "en": "Exports", "de": "Exporte", "es": "Exportaciones", "zh": "导出"}.get(lang, "Exports")
    st.markdown(f"### 📦 {exports_label}")
    
    exp_col1, exp_col2, exp_col3 = st.columns(3)
    
    with exp_col1:
        audio_label = {"fr": "Audio Tirage", "en": "Audio Reading", "de": "Audio Lesung", "es": "Audio de la Lectura", "zh": "音频"}.get(lang, "Audio")
        st.markdown(f"#### 🎵 {audio_label}")
        gen_label = {"fr": "Générer audio", "en": "Generate audio", "de": "Audio generieren", "es": "Generar audio", "zh": "生成音频"}.get(lang, "Generate")
        if st.button(f"🔊 {gen_label}", use_container_width=True):
            with st.spinner(t('throwing', lang)):
                audio_data = generate_audio_sequence(traits)
                audio_b64 = audio_to_base64(audio_data)
                st.audio(f"data:audio/wav;base64,{audio_b64}", format="audio/wav")
                audio_buffer = BytesIO()
                wavfile.write(audio_buffer, 44100, audio_data)
                st.download_button("📥 Télécharger WAV", audio_buffer.getvalue(), 
                                   f"yijing-audio-hex{hex_numero}.wav", "audio/wav")
    
    with exp_col2:
        st.markdown(f"#### 📄 {t('download_pdf', lang).replace('📥 ', '')}")
        if st.button("📄 PDF", use_container_width=True):
            with st.spinner(t('throwing', lang)):
                grille = generer_grille(traits, images_path, mutation=False) if images_path.exists() else None
                grille_mut = generer_grille(traits, images_path, mutation=True) if (images_path.exists() and hex_mute_numero) else None
                pdf_data = generate_pdf_report_complete(traits, st.session_state.question, 
                                                        hex_data, hex_mute_data, grille, grille_mut, lang=lang)
                st.download_button(t('download_pdf', lang), pdf_data, 
                                   f"{t('pdf_filename', lang)}-hex{hex_numero}.pdf", "application/pdf")
                st.success("✅ PDF OK")
    
    with exp_col3:
        st.markdown(f"#### 🧘 {t('kasina_title', lang).replace('🧘 ', '')}")
        if st.button("🧘 Kasina", use_container_width=True):
            with st.spinner(t('throwing', lang)):
                kbs_content, segments = generate_kbs_session(hex_data)
                kasina_audio = generate_kasina_audio(segments)
                
                st.success("✅ Kasina OK")
                
                kcol1, kcol2 = st.columns(2)
                with kcol1:
                    st.download_button(t('download_kasina', lang), kbs_content,
                                       f"{t('kasina_filename', lang)}-hex{hex_numero}.kbs", "text/plain")
                with kcol2:
                    audio_buffer = BytesIO()
                    wavfile.write(audio_buffer, 44100, kasina_audio)
                    st.download_button(t('download_audio', lang), audio_buffer.getvalue(),
                                       f"{t('audio_filename', lang)}-hex{hex_numero}.wav", "audio/wav")

else:
    # Page d'accueil
    st.markdown("""
    ### 🌟 Bienvenue dans l'Oracle du Yi Jing v2.2
    
    Le **Yi Jing** (易經), ou *Livre des Mutations*, est l'un des plus anciens textes 
    de sagesse chinoise. Cette version propose une expérience complète avec :
    
    #### ✨ Fonctionnalités
    
    - 🎲 **Tirage** aléatoire ou manuel des 6 traits
    - 📜 **Textes complets** : Description, Jugement, Image, et les 6 traits
    - 🎮 **Grilles animées** avec transition vers la mutation
    - 📄 **PDF détaillé** de 3 à 5 pages avec toute l'interprétation
    - 🎵 **Audio** aux fréquences sacrées (432 Hz)
    - 🧘 **Méditation Kasina** au format KBS Mindplace
    """)
    
    with st.expander("📖 Comment consulter l'Oracle ?"):
        st.markdown("""
        1. **Formulez votre question** avec clarté et intention
        2. **Effectuez le tirage** (aléatoire ou manuel)
        3. **Lisez les textes** dans l'ordre : Jugement → Image → Traits mutants
        4. **Méditez** sur la grille générée
        5. **Exportez** le rapport PDF pour référence future
        """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #9E9E9E; font-size: 0.85rem; padding: 1rem;">
    易經 Yi Jing Oracle v2.2 | Grilles : Anibal Edelbert Amiot | CyberMind.FR<br>
    <em>Le changement est la seule constante de l'univers - 變化是宇宙唯一的常數</em>
</div>
""", unsafe_allow_html=True)
