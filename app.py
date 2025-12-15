#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     易經 YI JING ORACLE v2.2                                 ║
║                    Application Streamlit                                     ║
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
def load_yijing_data(json_path):
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

def init_cjk_font():
    """Initialise une police CJK pour les caractères chinois"""
    # Liste des polices CJK à essayer
    cjk_fonts = [
        'STSong-Light',      # Police chinoise standard ReportLab
        'HeiseiMin-W3',      # Police japonaise
        'HeiseiKakuGo-W5',   # Police japonaise
        'HYSMyeongJo-Medium' # Police coréenne
    ]
    
    for font_name in cjk_fonts:
        try:
            pdfmetrics.registerFont(UnicodeCIDFont(font_name))
            return font_name
        except:
            continue
    
    # Essayer d'enregistrer une police TTF si disponible
    try:
        from reportlab.pdfbase.ttfonts import TTFont
        import os
        
        # Chercher des polices Noto CJK
        font_paths = [
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('NotoCJK', font_path))
                return 'NotoCJK'
    except:
        pass
    
    return None

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

def generate_pdf_report_complete(traits, question, hex_data, hex_mute_data, grille_img, grille_mut_img=None):
    """Génère un rapport PDF complet multi-pages"""
    buffer = BytesIO()
    width, height = A4
    margin = 15 * mm
    c = canvas.Canvas(buffer, pagesize=A4)
    
    cjk_font = init_cjk_font()
    
    # Couleurs
    marron = HexColor('#8B4513')
    or_color = HexColor('#DAA520')
    creme = HexColor('#FFFAF0')
    gris = HexColor('#5D4037')
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
    c.drawCentredString(width/2, height - 22*mm, "Rapport de Consultation Détaillé")
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
        c.drawString(margin + 4*mm, y - 5*mm, "Question posée :")
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
    c.drawCentredString(width/2, y - 10*mm, f"HEXAGRAMME {hex_numero}")
    
    caractere = hex_data.get('caractere', '')
    if caractere:
        if cjk_font:
            c.setFont(cjk_font, 42)
        else:
            # Fallback: utiliser Helvetica (le caractère pourrait ne pas s'afficher correctement)
            c.setFont("Helvetica-Bold", 42)
        c.setFillColor(HexColor('#2F4F4F'))
        c.drawCentredString(width/2, y - 32*mm, caractere)
    
    nom = f"{hex_data.get('nom_pinyin', '')} - {hex_data.get('nom_fr', '')}"
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
    c.drawString(margin + 4*mm, y - 6*mm, f"☰ Trigramme Supérieur")
    c.setFont("Helvetica", 8)
    c.setFillColor(gris)
    c.drawString(margin + 4*mm, y - 12*mm, f"{trig_h_info.get('symbole', '')} {trig_haut} - {trig_h_info.get('element', '')}")
    c.drawString(margin + 4*mm, y - 17*mm, f"{trig_h_info.get('freq', 0)} Hz - {hex_data.get('trigramme_haut_desc', '')[:35]}")
    c.drawString(margin + 4*mm, y - 22*mm, f"Nature: {trig_h_info.get('nature', '')}")
    
    c.setFillColor(bleu)
    c.setFont("Helvetica-Bold", 9)
    tx = margin + (width - 2*margin + 5*mm)/2 + 4*mm
    c.drawString(tx, y - 6*mm, f"☷ Trigramme Inférieur")
    c.setFont("Helvetica", 8)
    c.setFillColor(gris)
    c.drawString(tx, y - 12*mm, f"{trig_b_info.get('symbole', '')} {trig_bas} - {trig_b_info.get('element', '')}")
    c.drawString(tx, y - 17*mm, f"{trig_b_info.get('freq', 0)} Hz - {hex_data.get('trigramme_bas_desc', '')[:35]}")
    c.drawString(tx, y - 22*mm, f"Nature: {trig_b_info.get('nature', '')}")
    y -= 32*mm
    
    # Traits tirés
    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, "Traits tirés et fréquences :")
    y -= 6*mm
    
    for i in range(5, -1, -1):
        t = traits[i]
        info = FREQ_TRAITS[t]
        is_mutant = t in [6, 9]
        
        if is_mutant:
            c.setFillColor(HexColor('#FFEBEE'))
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
        c.drawString(margin, y, "Grille La Livrée d'Hermès :")
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
    c.drawCentredString(width/2, 8*mm, "Yi Jing Oracle v2.2 - CyberMind.FR | Grilles: Anibal Edelbert Amiot | Page 1")
    
    # ==========================================================================
    # PAGE 2 : JUGEMENT ET IMAGE
    # ==========================================================================
    c.showPage()
    y = height - 20*mm
    
    c.setFillColor(marron)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y, f"Hexagramme {hex_numero} - Textes Traditionnels")
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
        c.drawString(margin + 5*mm, y - 8*mm, "⚖️ LE JUGEMENT")
        
        c.setFillColor(gris)
        c.setFont("Helvetica", 8)
        text_y = y - 16*mm
        for line in jug_lines[:15]:
            c.drawString(margin + 5*mm, text_y, line)
            text_y -= 4*mm
        y -= box_height + 8*mm
    
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
        c.drawString(margin + 5*mm, y - 8*mm, "🖼️ L'IMAGE")
        
        c.setFillColor(gris)
        c.setFont("Helvetica", 8)
        text_y = y - 16*mm
        for line in img_lines[:12]:
            c.drawString(margin + 5*mm, text_y, line)
            text_y -= 4*mm
        y -= box_height + 8*mm
    
    # Interprétation générale
    c.setFillColor(HexColor('#F3E5F5'))
    c.setStrokeColor(violet)
    c.setLineWidth(1.5)
    c.roundRect(margin, y - 45*mm, width - 2*margin, 45*mm, 4, fill=1, stroke=1)
    
    c.setFillColor(violet)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin + 5*mm, y - 8*mm, "🔮 INTERPRÉTATION GÉNÉRALE")
    
    c.setFillColor(gris)
    c.setFont("Helvetica", 8)
    
    has_mutation = any(t in [6, 9] for t in traits)
    nb_mutants = sum(1 for t in traits if t in [6, 9])
    
    interp_lines = []
    interp_lines.append(f"Hexagramme obtenu: {hex_numero} - {hex_data.get('nom_fr', '')}")
    interp_lines.append(f"Combinaison: {trig_haut} ({trig_h_info.get('element', '')}) sur {trig_bas} ({trig_b_info.get('element', '')})")
    
    if has_mutation:
        interp_lines.append(f"")
        interp_lines.append(f"⚡ {nb_mutants} trait(s) mutant(s) détecté(s) - Situation en transformation")
        interp_lines.append(f"L'hexagramme évolue vers le n°{hex_mute_numero}: {hex_mute_data.get('nom_fr', '')}")
        interp_lines.append(f"Lisez attentivement les textes des traits mutants ci-après.")
    else:
        interp_lines.append(f"")
        interp_lines.append(f"✓ Aucun trait mutant - Situation stable")
        interp_lines.append(f"Le message de l'hexagramme s'applique tel quel.")
    
    text_y = y - 16*mm
    for line in interp_lines:
        c.drawString(margin + 5*mm, text_y, line)
        text_y -= 4*mm
    
    c.setFillColor(HexColor('#9E9E9E'))
    c.setFont("Helvetica", 6)
    c.drawCentredString(width/2, 8*mm, "Page 2")
    
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
            bg_color = HexColor('#FFEBEE')
            border_color = rouge
        elif trait_val == 7:
            bg_color = HexColor('#E8F5E9')
            border_color = vert
        else:
            bg_color = HexColor('#E3F2FD')
            border_color = bleu
        
        c.setFillColor(bg_color)
        c.setStrokeColor(border_color)
        c.setLineWidth(1.5)
        
        box_height = 38*mm
        if y - box_height < 25*mm:
            c.showPage()
            y = height - 20*mm
        
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
        c.drawCentredString(width/2, y, "⚡ TRAITS MUTANTS - À lire attentivement")
        y -= 8*mm
        
        c.setFillColor(gris)
        c.setFont("Helvetica", 9)
        c.drawCentredString(width/2, y, f"Ces {len(traits_mutants)} trait(s) indiquent les aspects de la situation en transformation")
        y -= 15*mm
        
        for pos, val in traits_mutants:
            trait_data = next((t for t in hex_traits if t.get('position') == pos + 1), None)
            
            c.setFillColor(HexColor('#FFCDD2'))
            c.setStrokeColor(rouge)
            c.setLineWidth(2)
            
            box_height = 50*mm
            if y - box_height < 30*mm:
                c.showPage()
                y = height - 20*mm
            
            c.roundRect(margin, y - box_height, width - 2*margin, box_height, 5, fill=1, stroke=1)
            
            info = FREQ_TRAITS[val]
            c.setFillColor(rouge)
            c.setFont("Helvetica-Bold", 11)
            mutation_dir = "Yin → Yang" if val == 6 else "Yang → Yin"
            c.drawString(margin + 5*mm, y - 9*mm, f"🔄 TRAIT {pos + 1} MUTANT - {info['nom']} ({mutation_dir})")
            
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
        
        car_mut = hex_mute_data.get('caractere', '')
        if car_mut:
            if cjk_font:
                c.setFont(cjk_font, 36)
            else:
                c.setFont("Helvetica-Bold", 36)
            c.setFillColor(HexColor('#4A148C'))
            c.drawCentredString(width/2, y - 28*mm, car_mut)
        
        nom_mut = f"{hex_mute_data.get('nom_pinyin', '')} - {hex_mute_data.get('nom_fr', '')}"
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
            c.drawString(margin + 5*mm, y - 7*mm, "⚖️ Jugement de l'hexagramme de mutation")
            
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

# Header
st.markdown("""
<div class="main-header">
    <h1>☯ 易經 Yi Jing Oracle v2.2</h1>
    <p>Grilles animées • Textes complets • PDF détaillé • Méditation Kasina KBS</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎴 Consultation")
    question = st.text_area("Votre question :", placeholder="Formulez votre question avec intention...", height=100)
    st.divider()
    
    mode = st.radio("Mode de tirage :", ["🎲 Tirage aléatoire", "✏️ Saisie manuelle"])
    
    if mode == "✏️ Saisie manuelle":
        st.caption("Traits (6=Yin mut, 7=Yang, 8=Yin, 9=Yang mut)")
        cols = st.columns(6)
        manual_traits = []
        for i, col in enumerate(cols):
            with col:
                t = st.selectbox(f"{i+1}", [6, 7, 8, 9], index=1, key=f"t{i}")
                manual_traits.append(t)
    
    st.divider()
    
    if st.button("🎴 Consulter l'Oracle", type="primary", use_container_width=True):
        st.session_state.question = question
        if mode == "🎲 Tirage aléatoire":
            st.session_state.traits = [tirer_trait() for _ in range(6)]
        else:
            st.session_state.traits = manual_traits
        st.session_state.grille_view = 'principal'
    
    st.divider()
    json_path = st.text_input("📄 Fichier JSON :", value="yijing_complet.json")
    images_dir = st.text_input("📁 Dossier images :", value="images")

# Charger données
yijing_data = load_yijing_data(json_path)

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
        nom_fr = hex_data.get('nom_fr', '')
        
        st.markdown(f"""
        <div class="hex-card">
            <div style="font-size: 0.9rem; color: #8B4513; letter-spacing: 2px;">HEXAGRAMME {hex_numero}</div>
            <div class="hex-caractere">{caractere}</div>
            <div class="hex-nom">{nom_pinyin}</div>
            <div style="font-size: 1.1rem; color: #5D4037; font-style: italic;">{nom_fr}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Trigrammes
        trig_haut = hex_data.get('trigramme_haut', '')
        trig_bas = hex_data.get('trigramme_bas', '')
        trig_h_info = TRIGRAMMES.get(trig_haut, {})
        trig_b_info = TRIGRAMMES.get(trig_bas, {})
        
        st.markdown("#### ☯ Trigrammes composants")
        tcol1, tcol2 = st.columns(2)
        with tcol1:
            st.markdown(f"""
            **{trig_h_info.get('symbole', '')} Supérieur**  
            {trig_haut} ({trig_h_info.get('element', '')})  
            *{trig_h_info.get('freq', 0)} Hz*  
            {hex_data.get('trigramme_haut_desc', '')[:40]}...
            """)
        with tcol2:
            st.markdown(f"""
            **{trig_b_info.get('symbole', '')} Inférieur**  
            {trig_bas} ({trig_b_info.get('element', '')})  
            *{trig_b_info.get('freq', 0)} Hz*  
            {hex_data.get('trigramme_bas_desc', '')[:40]}...
            """)
    
    with col2:
        st.markdown("#### 📊 Traits tirés")
        
        nb_mutants = sum(1 for t in traits if t in [6, 9])
        if nb_mutants > 0:
            st.warning(f"⚡ {nb_mutants} trait(s) mutant(s) - Situation en transformation")
        
        for i in range(5, -1, -1):
            t = traits[i]
            info = FREQ_TRAITS[t]
            is_yang = t in [7, 9]
            is_mut = t in [6, 9]
            
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
            st.markdown(f"""
            <div class="mutation-card">
                <div style="font-size: 0.85rem; letter-spacing: 1px;">🔄 MUTATION VERS</div>
                <div style="font-size: 2.8rem;">{car_mut}</div>
                <div style="font-weight: bold; font-size: 1.1rem;">{hex_mute_numero}. {hex_mute_data.get('nom_pinyin', '')}</div>
                <div style="font-style: italic;">{hex_mute_data.get('nom_fr', '')}</div>
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
                    current_title = f"Hexagramme {hex_numero} - {hex_data.get('nom_fr', '')}"
                else:
                    current_img = grille_mut_b64
                    current_title = f"Mutation → Hexagramme {hex_mute_numero} - {hex_mute_data.get('nom_fr', '')}"
                
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
                if st.checkbox("🔄 Animation automatique (2s)", value=False):
                    time.sleep(2)
                    st.session_state.grille_view = 'mutation' if st.session_state.grille_view == 'principal' else 'principal'
                    st.rerun()
            else:
                # Pas de mutation, afficher seulement la grille principale
                grille_b64 = image_to_base64(grille)
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <p style="font-weight: bold; color: #8B4513; margin-bottom: 1rem;">Hexagramme {hex_numero} - {hex_data.get('nom_fr', '')}</p>
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
                st.download_button("📥 Télécharger grille principale", buf.getvalue(), 
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
            t = traits[i]
            info = FREQ_TRAITS[t]
            is_mutant = t in [6, 9]
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
        st.markdown("### ⚡ Traits Mutants - Attention particulière")
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
                                🔄 TRAIT {pos + 1} - {mutation_dir}
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
        st.markdown(f"### 🔄 Hexagramme de Mutation : {hex_mute_numero} - {hex_mute_data.get('nom_fr', '')}")
        
        with st.expander("📖 Description de l'hexagramme de mutation", expanded=True):
            st.write(hex_mute_data.get('description', ''))
        
        jug_mut = hex_mute_data.get('jugement_texte', '')
        if jug_mut:
            st.markdown(f"""
            <div class="text-box" style="background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%); border-left: 5px solid #7B1FA2;">
                <h4 style="color: #7B1FA2; margin-bottom: 0.8rem;">⚖️ JUGEMENT (Mutation)</h4>
                <p style="color: #5D4037; line-height: 1.6;">{jug_mut}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # =========================================================================
    # SECTION 6 : EXPORTS
    # =========================================================================
    
    st.markdown("### 📦 Exports")
    
    exp_col1, exp_col2, exp_col3 = st.columns(3)
    
    with exp_col1:
        st.markdown("#### 🎵 Audio Tirage")
        if st.button("🔊 Générer audio", use_container_width=True):
            with st.spinner("Génération..."):
                audio_data = generate_audio_sequence(traits)
                audio_b64 = audio_to_base64(audio_data)
                st.audio(f"data:audio/wav;base64,{audio_b64}", format="audio/wav")
                audio_buffer = BytesIO()
                wavfile.write(audio_buffer, 44100, audio_data)
                st.download_button("📥 Télécharger WAV", audio_buffer.getvalue(), 
                                   f"yijing-audio-hex{hex_numero}.wav", "audio/wav")
    
    with exp_col2:
        st.markdown("#### 📄 Rapport PDF Complet")
        if st.button("📄 Générer PDF", use_container_width=True):
            with st.spinner("Génération du rapport détaillé..."):
                grille = generer_grille(traits, images_path, mutation=False) if images_path.exists() else None
                grille_mut = generer_grille(traits, images_path, mutation=True) if (images_path.exists() and hex_mute_numero) else None
                pdf_data = generate_pdf_report_complete(traits, st.session_state.question, 
                                                        hex_data, hex_mute_data, grille, grille_mut)
                st.download_button("📥 Télécharger PDF", pdf_data, 
                                   f"yijing-rapport-complet-hex{hex_numero}.pdf", "application/pdf")
                st.success("✅ Rapport PDF complet généré (3-5 pages)")
    
    with exp_col3:
        st.markdown("#### 🧘 Méditation Kasina")
        if st.button("🧘 Générer Kasina", use_container_width=True):
            with st.spinner("Génération session Kasina..."):
                kbs_content, segments = generate_kbs_session(hex_data)
                kasina_audio = generate_kasina_audio(segments)
                
                st.success("✅ Session Kasina générée!")
                
                kcol1, kcol2 = st.columns(2)
                with kcol1:
                    st.download_button("📋 Fichier KBS", kbs_content,
                                       f"yijing-hex{hex_numero}.kbs", "text/plain")
                with kcol2:
                    audio_buffer = BytesIO()
                    wavfile.write(audio_buffer, 44100, kasina_audio)
                    st.download_button("🎧 Audio Binaural", audio_buffer.getvalue(),
                                       f"yijing-kasina-hex{hex_numero}.wav", "audio/wav")

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
