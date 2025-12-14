#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     易經 YI JING ORACLE                                      ║
║              Application Streamlit                                           ║
║         avec Grilles "La Livrée d'Hermès"                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import random
import datetime
import base64
from io import BytesIO
from pathlib import Path

# Imports pour images
from PIL import Image, ImageChops

# Imports pour PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

# Imports pour audio
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
# DONNÉES YI JING
# ============================================================================

HEXAGRAMMES = {
    1: {"caractere": "乾", "pinyin": "Qián", "nom": "Le Créateur", "haut": "Ciel", "bas": "Ciel"},
    2: {"caractere": "坤", "pinyin": "Kūn", "nom": "Le Réceptif", "haut": "Terre", "bas": "Terre"},
    3: {"caractere": "屯", "pinyin": "Zhūn", "nom": "La Difficulté Initiale", "haut": "Eau", "bas": "Tonnerre"},
    4: {"caractere": "蒙", "pinyin": "Méng", "nom": "La Folie Juvénile", "haut": "Montagne", "bas": "Eau"},
    5: {"caractere": "需", "pinyin": "Xū", "nom": "L'Attente", "haut": "Eau", "bas": "Ciel"},
    6: {"caractere": "訟", "pinyin": "Sòng", "nom": "Le Conflit", "haut": "Ciel", "bas": "Eau"},
    7: {"caractere": "師", "pinyin": "Shī", "nom": "L'Armée", "haut": "Terre", "bas": "Eau"},
    8: {"caractere": "比", "pinyin": "Bǐ", "nom": "La Solidarité", "haut": "Eau", "bas": "Terre"},
    9: {"caractere": "小畜", "pinyin": "Xiǎo Xù", "nom": "Le Petit Apprivoisement", "haut": "Vent", "bas": "Ciel"},
    10: {"caractere": "履", "pinyin": "Lǚ", "nom": "La Marche", "haut": "Ciel", "bas": "Lac"},
    11: {"caractere": "泰", "pinyin": "Tài", "nom": "La Paix", "haut": "Terre", "bas": "Ciel"},
    12: {"caractere": "否", "pinyin": "Pǐ", "nom": "La Stagnation", "haut": "Ciel", "bas": "Terre"},
    13: {"caractere": "同人", "pinyin": "Tóng Rén", "nom": "La Communauté", "haut": "Ciel", "bas": "Feu"},
    14: {"caractere": "大有", "pinyin": "Dà Yǒu", "nom": "Le Grand Avoir", "haut": "Feu", "bas": "Ciel"},
    15: {"caractere": "謙", "pinyin": "Qiān", "nom": "L'Humilité", "haut": "Terre", "bas": "Montagne"},
    16: {"caractere": "豫", "pinyin": "Yù", "nom": "L'Enthousiasme", "haut": "Tonnerre", "bas": "Terre"},
    17: {"caractere": "隨", "pinyin": "Suí", "nom": "La Suite", "haut": "Lac", "bas": "Tonnerre"},
    18: {"caractere": "蠱", "pinyin": "Gǔ", "nom": "Le Travail sur le Corrompu", "haut": "Montagne", "bas": "Vent"},
    19: {"caractere": "臨", "pinyin": "Lín", "nom": "L'Approche", "haut": "Terre", "bas": "Lac"},
    20: {"caractere": "觀", "pinyin": "Guān", "nom": "La Contemplation", "haut": "Vent", "bas": "Terre"},
    21: {"caractere": "噬嗑", "pinyin": "Shì Kè", "nom": "Mordre au Travers", "haut": "Feu", "bas": "Tonnerre"},
    22: {"caractere": "賁", "pinyin": "Bì", "nom": "La Grâce", "haut": "Montagne", "bas": "Feu"},
    23: {"caractere": "剝", "pinyin": "Bō", "nom": "L'Éclatement", "haut": "Montagne", "bas": "Terre"},
    24: {"caractere": "復", "pinyin": "Fù", "nom": "Le Retour", "haut": "Terre", "bas": "Tonnerre"},
    25: {"caractere": "無妄", "pinyin": "Wú Wàng", "nom": "L'Innocence", "haut": "Ciel", "bas": "Tonnerre"},
    26: {"caractere": "大畜", "pinyin": "Dà Xù", "nom": "Le Grand Apprivoisement", "haut": "Montagne", "bas": "Ciel"},
    27: {"caractere": "頤", "pinyin": "Yí", "nom": "Les Commissures des Lèvres", "haut": "Montagne", "bas": "Tonnerre"},
    28: {"caractere": "大過", "pinyin": "Dà Guò", "nom": "La Prépondérance du Grand", "haut": "Lac", "bas": "Vent"},
    29: {"caractere": "坎", "pinyin": "Kǎn", "nom": "L'Insondable (Eau)", "haut": "Eau", "bas": "Eau"},
    30: {"caractere": "離", "pinyin": "Lí", "nom": "Ce qui s'Attache (Feu)", "haut": "Feu", "bas": "Feu"},
    31: {"caractere": "咸", "pinyin": "Xián", "nom": "L'Influence", "haut": "Lac", "bas": "Montagne"},
    32: {"caractere": "恆", "pinyin": "Héng", "nom": "La Durée", "haut": "Tonnerre", "bas": "Vent"},
    33: {"caractere": "遯", "pinyin": "Dùn", "nom": "La Retraite", "haut": "Ciel", "bas": "Montagne"},
    34: {"caractere": "大壯", "pinyin": "Dà Zhuàng", "nom": "La Puissance du Grand", "haut": "Tonnerre", "bas": "Ciel"},
    35: {"caractere": "晉", "pinyin": "Jìn", "nom": "Le Progrès", "haut": "Feu", "bas": "Terre"},
    36: {"caractere": "明夷", "pinyin": "Míng Yí", "nom": "L'Obscurcissement de la Lumière", "haut": "Terre", "bas": "Feu"},
    37: {"caractere": "家人", "pinyin": "Jiā Rén", "nom": "La Famille", "haut": "Vent", "bas": "Feu"},
    38: {"caractere": "睽", "pinyin": "Kuí", "nom": "L'Opposition", "haut": "Feu", "bas": "Lac"},
    39: {"caractere": "蹇", "pinyin": "Jiǎn", "nom": "L'Obstacle", "haut": "Eau", "bas": "Montagne"},
    40: {"caractere": "解", "pinyin": "Xiè", "nom": "La Libération", "haut": "Tonnerre", "bas": "Eau"},
    41: {"caractere": "損", "pinyin": "Sǔn", "nom": "La Diminution", "haut": "Montagne", "bas": "Lac"},
    42: {"caractere": "益", "pinyin": "Yì", "nom": "L'Augmentation", "haut": "Vent", "bas": "Tonnerre"},
    43: {"caractere": "夬", "pinyin": "Guài", "nom": "La Percée", "haut": "Lac", "bas": "Ciel"},
    44: {"caractere": "姤", "pinyin": "Gòu", "nom": "Venir à la Rencontre", "haut": "Ciel", "bas": "Vent"},
    45: {"caractere": "萃", "pinyin": "Cuì", "nom": "Le Rassemblement", "haut": "Lac", "bas": "Terre"},
    46: {"caractere": "升", "pinyin": "Shēng", "nom": "La Poussée vers le Haut", "haut": "Terre", "bas": "Vent"},
    47: {"caractere": "困", "pinyin": "Kùn", "nom": "L'Accablement", "haut": "Lac", "bas": "Eau"},
    48: {"caractere": "井", "pinyin": "Jǐng", "nom": "Le Puits", "haut": "Eau", "bas": "Vent"},
    49: {"caractere": "革", "pinyin": "Gé", "nom": "La Révolution", "haut": "Lac", "bas": "Feu"},
    50: {"caractere": "鼎", "pinyin": "Dǐng", "nom": "Le Chaudron", "haut": "Feu", "bas": "Vent"},
    51: {"caractere": "震", "pinyin": "Zhèn", "nom": "L'Éveilleur (Tonnerre)", "haut": "Tonnerre", "bas": "Tonnerre"},
    52: {"caractere": "艮", "pinyin": "Gèn", "nom": "L'Immobilisation (Montagne)", "haut": "Montagne", "bas": "Montagne"},
    53: {"caractere": "漸", "pinyin": "Jiàn", "nom": "Le Développement", "haut": "Vent", "bas": "Montagne"},
    54: {"caractere": "歸妹", "pinyin": "Guī Mèi", "nom": "L'Épousée", "haut": "Tonnerre", "bas": "Lac"},
    55: {"caractere": "豐", "pinyin": "Fēng", "nom": "L'Abondance", "haut": "Tonnerre", "bas": "Feu"},
    56: {"caractere": "旅", "pinyin": "Lǚ", "nom": "Le Voyageur", "haut": "Feu", "bas": "Montagne"},
    57: {"caractere": "巽", "pinyin": "Xùn", "nom": "Le Doux (Vent)", "haut": "Vent", "bas": "Vent"},
    58: {"caractere": "兌", "pinyin": "Duì", "nom": "Le Joyeux (Lac)", "haut": "Lac", "bas": "Lac"},
    59: {"caractere": "渙", "pinyin": "Huàn", "nom": "La Dispersion", "haut": "Vent", "bas": "Eau"},
    60: {"caractere": "節", "pinyin": "Jié", "nom": "La Limitation", "haut": "Eau", "bas": "Lac"},
    61: {"caractere": "中孚", "pinyin": "Zhōng Fú", "nom": "La Vérité Intérieure", "haut": "Vent", "bas": "Lac"},
    62: {"caractere": "小過", "pinyin": "Xiǎo Guò", "nom": "La Prépondérance du Petit", "haut": "Tonnerre", "bas": "Montagne"},
    63: {"caractere": "既濟", "pinyin": "Jì Jì", "nom": "Après l'Accomplissement", "haut": "Eau", "bas": "Feu"},
    64: {"caractere": "未濟", "pinyin": "Wèi Jì", "nom": "Avant l'Accomplissement", "haut": "Feu", "bas": "Eau"},
}

# Table binaire -> hexagramme
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
    "Ciel": {"symbole": "☰", "element": "Métal", "qualite": "Force créatrice", "freq": 852},
    "Terre": {"symbole": "☷", "element": "Terre", "qualite": "Réceptivité", "freq": 396},
    "Tonnerre": {"symbole": "☳", "element": "Bois", "qualite": "Éveil", "freq": 417},
    "Eau": {"symbole": "☵", "element": "Eau", "qualite": "Profondeur", "freq": 528},
    "Montagne": {"symbole": "☶", "element": "Terre", "qualite": "Immobilité", "freq": 639},
    "Vent": {"symbole": "☴", "element": "Bois", "qualite": "Pénétration", "freq": 741},
    "Feu": {"symbole": "☲", "element": "Feu", "qualite": "Clarté", "freq": 963},
    "Lac": {"symbole": "☱", "element": "Métal", "qualite": "Joie", "freq": 432}
}

FREQ_TRAITS = {
    6: {"freq": 216, "note": "LA-1", "nom": "Yin mutant", "couleur": "#E91E63"},
    7: {"freq": 256, "note": "DO", "nom": "Yang stable", "couleur": "#4CAF50"},
    8: {"freq": 192, "note": "SOL-1", "nom": "Yin stable", "couleur": "#2196F3"},
    9: {"freq": 288, "note": "RÉ", "nom": "Yang mutant", "couleur": "#FF9800"}
}

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def tirer_trait():
    """Simule le tirage de 3 pièces"""
    return sum(random.choice([2, 3]) for _ in range(3))

def get_hexagramme(traits):
    """Trouve l'hexagramme correspondant aux traits"""
    binaire = tuple(1 if t in [7, 9] else 0 for t in traits)
    numero = BINAIRE_TO_HEX.get(binaire, 1)
    return {"numero": numero, **HEXAGRAMMES[numero]}

def get_mutation(traits):
    """Calcule l'hexagramme de mutation"""
    if not any(t in [6, 9] for t in traits):
        return None
    binaire_orig = tuple(1 if t in [7, 9] else 0 for t in traits)
    binaire_mute = tuple(
        (0 if t == 9 else 1 if t == 6 else b)
        for t, b in zip(traits, binaire_orig)
    )
    numero = BINAIRE_TO_HEX.get(binaire_mute, 1)
    return {"numero": numero, **HEXAGRAMMES[numero]}

def get_image_key(trait_val, position):
    """Retourne le nom de fichier de l'image"""
    is_yang = trait_val in [7, 9]
    is_mutant = trait_val in [6, 9]
    key = "YANG" if is_yang else "YING"
    if is_mutant:
        key += "-MUT"
    return f"lldh-YY-{key}-{position}.png"

def generer_grille(traits, images_dir, mutation=False):
    """Génère la grille composite"""
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

def generate_tone(frequency, duration, sample_rate=44100):
    """Génère une sinusoïde"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(2 * np.pi * frequency * t) * 0.3
    
    # Fade in/out
    fade_len = int(sample_rate * 0.05)
    tone[:fade_len] *= np.linspace(0, 1, fade_len)
    tone[-fade_len:] *= np.linspace(1, 0, fade_len)
    
    return tone

def generate_audio_sequence(traits, sample_rate=44100):
    """Génère la séquence audio du tirage"""
    # Drone intro
    intro = generate_tone(432, 2.0, sample_rate)
    silence = np.zeros(int(sample_rate * 0.3))
    
    parts = [intro, silence]
    
    for trait in traits:
        freq = FREQ_TRAITS[trait]['freq']
        tone = generate_tone(freq, 2.0, sample_rate)
        
        if trait in [6, 9]:
            beat = generate_tone(freq + 3, 2.0, sample_rate) * 0.5
            tone = tone * 0.7 + beat * 0.3
        
        parts.append(tone)
        parts.append(silence)
    
    # Accord final
    t = np.linspace(0, 4, int(sample_rate * 4), False)
    chord = np.zeros_like(t)
    intervals = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25]
    
    for i, trait in enumerate(traits):
        freq = FREQ_TRAITS[trait]['freq'] * intervals[i]
        chord += np.sin(2 * np.pi * freq * t) / (i + 1)
    
    chord = chord / np.max(np.abs(chord)) * 0.4
    fade_len = int(sample_rate * 0.3)
    chord[:fade_len] *= np.linspace(0, 1, fade_len)
    chord[-fade_len:] *= np.linspace(1, 0, fade_len)
    
    parts.append(chord)
    
    audio = np.concatenate(parts)
    audio = audio / np.max(np.abs(audio))
    
    return (audio * 32767).astype(np.int16)

def audio_to_base64(audio_data, sample_rate=44100):
    """Convertit audio en base64 pour lecture web"""
    buffer = BytesIO()
    wavfile.write(buffer, sample_rate, audio_data)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode()

def generate_pdf_report(traits, question, hexagramme, hex_mute, grille_img):
    """Génère le rapport PDF"""
    buffer = BytesIO()
    width, height = A4
    margin = 20 * mm
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Couleurs
    marron = HexColor('#8B4513')
    or_color = HexColor('#DAA520')
    creme = HexColor('#FFFAF0')
    gris = HexColor('#5D4037')
    
    # En-tête
    c.setFillColor(marron)
    c.rect(0, height - 45*mm, width, 45*mm, fill=1)
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height - 18*mm, "易經 Yi Jing Oracle")
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 28*mm, "Rapport de Consultation")
    
    c.setFont("Helvetica", 10)
    date_str = datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")
    c.drawCentredString(width/2, height - 38*mm, date_str)
    
    y = height - 55*mm
    
    # Question
    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "Question posée :")
    c.setFont("Helvetica", 10)
    c.drawString(margin, y - 6*mm, question[:90] if question else "Consultation générale")
    y -= 18*mm
    
    # Hexagramme
    c.setFillColor(creme)
    c.setStrokeColor(or_color)
    c.setLineWidth(2)
    c.roundRect(margin, y - 50*mm, width - 2*margin, 50*mm, 5, fill=1, stroke=1)
    
    c.setFillColor(marron)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y - 10*mm, f"HEXAGRAMME {hexagramme['numero']}")
    
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(HexColor('#2F4F4F'))
    c.drawCentredString(width/2, y - 28*mm, hexagramme['caractere'])
    
    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y - 40*mm, f"{hexagramme['pinyin']} - {hexagramme['nom']}")
    
    y -= 60*mm
    
    # Traits
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "Traits tirés :")
    y -= 7*mm
    
    for i, t in enumerate(traits):
        info = FREQ_TRAITS[t]
        symbole = "━━━━━" if t in [7, 9] else "━   ━"
        mut = " 🔄" if t in [6, 9] else ""
        c.setFont("Helvetica", 9)
        c.drawString(margin + 5*mm, y, f"Trait {i+1}: {symbole}  {info['nom']} ({info['freq']} Hz){mut}")
        y -= 5*mm
    
    y -= 8*mm
    
    # Grille
    if grille_img:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, y, "Grille La Livrée d'Hermès :")
        y -= 3*mm
        
        img_buffer = BytesIO()
        grille_img.save(img_buffer, 'PNG')
        img_buffer.seek(0)
        
        from reportlab.lib.utils import ImageReader
        img_reader = ImageReader(img_buffer)
        c.drawImage(img_reader, margin, y - 70*mm, width=50*mm, height=70*mm, preserveAspectRatio=True)
    
    # Pied de page
    c.setFillColor(HexColor('#9E9E9E'))
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 10*mm, "Yi Jing Oracle - La Livrée d'Hermès | CyberMind.FR")
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# ============================================================================
# CSS PERSONNALISÉ
# ============================================================================

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .hex-card {
        background: linear-gradient(135deg, #FFFAF0 0%, #FFF8DC 100%);
        border: 3px solid #DAA520;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .hex-caractere {
        font-size: 5rem;
        color: #2F4F4F;
    }
    
    .hex-nom {
        font-size: 1.5rem;
        color: #8B4513;
        font-weight: bold;
    }
    
    .trait-box {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.2rem;
        border-radius: 10px;
        font-family: monospace;
        font-size: 1.1rem;
    }
    
    .trait-yang { background: #E8F5E9; border: 2px solid #4CAF50; }
    .trait-yin { background: #E3F2FD; border: 2px solid #2196F3; }
    .trait-yang-mut { background: #FFF3E0; border: 2px solid #FF9800; }
    .trait-yin-mut { background: #FCE4EC; border: 2px solid #E91E63; }
    
    .freq-card {
        background: #F3E5F5;
        border-left: 5px solid #9C27B0;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 10px 10px 0;
    }
    
    .mutation-card {
        background: linear-gradient(135deg, #FCE4EC 0%, #F8BBD9 100%);
        border: 3px solid #E91E63;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.2rem;
        border-radius: 10px;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #A0522D 0%, #8B4513 100%);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# APPLICATION PRINCIPALE
# ============================================================================

# Initialiser le state
if 'traits' not in st.session_state:
    st.session_state.traits = None
if 'hexagramme' not in st.session_state:
    st.session_state.hexagramme = None
if 'hex_mute' not in st.session_state:
    st.session_state.hex_mute = None
if 'question' not in st.session_state:
    st.session_state.question = ""

# Header
st.markdown("""
<div class="main-header">
    <h1>☯ 易經 Yi Jing Oracle</h1>
    <p>avec Grilles "La Livrée d'Hermès" & Fréquences Sacrées</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎴 Consultation")
    
    question = st.text_area(
        "Votre question (optionnel) :",
        placeholder="Quelle direction prendre ?",
        height=100
    )
    
    st.divider()
    
    mode = st.radio(
        "Mode de tirage :",
        ["🎲 Tirage aléatoire", "✏️ Saisie manuelle"]
    )
    
    if mode == "✏️ Saisie manuelle":
        st.write("Traits (6=Yin mut, 7=Yang, 8=Yin, 9=Yang mut)")
        cols = st.columns(6)
        manual_traits = []
        for i, col in enumerate(cols):
            with col:
                t = st.selectbox(f"{i+1}", [6, 7, 8, 9], index=1, key=f"trait_{i}")
                manual_traits.append(t)
    
    st.divider()
    
    if st.button("🎴 Consulter l'Oracle", type="primary", use_container_width=True):
        st.session_state.question = question
        
        if mode == "🎲 Tirage aléatoire":
            st.session_state.traits = [tirer_trait() for _ in range(6)]
        else:
            st.session_state.traits = manual_traits
        
        st.session_state.hexagramme = get_hexagramme(st.session_state.traits)
        st.session_state.hex_mute = get_mutation(st.session_state.traits)
    
    st.divider()
    
    # Config images
    images_dir = st.text_input(
        "📁 Dossier images :",
        value="images",
        help="Chemin vers les 24 images PNG des grilles"
    )

# Contenu principal
if st.session_state.traits is not None:
    traits = st.session_state.traits
    hex_data = st.session_state.hexagramme
    hex_mute = st.session_state.hex_mute
    
    # Colonnes principales
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Hexagramme principal
        st.markdown(f"""
        <div class="hex-card">
            <div style="font-size: 0.9rem; color: #8B4513;">HEXAGRAMME {hex_data['numero']}</div>
            <div class="hex-caractere">{hex_data['caractere']}</div>
            <div class="hex-nom">{hex_data['pinyin']}</div>
            <div style="font-size: 1.2rem; color: #5D4037; font-style: italic;">{hex_data['nom']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Trigrammes
        trig_haut = TRIGRAMMES[hex_data['haut']]
        trig_bas = TRIGRAMMES[hex_data['bas']]
        
        st.markdown("#### ☯ Trigrammes")
        tcol1, tcol2 = st.columns(2)
        with tcol1:
            st.metric(
                f"{trig_haut['symbole']} Supérieur",
                hex_data['haut'],
                f"{trig_haut['freq']} Hz"
            )
        with tcol2:
            st.metric(
                f"{trig_bas['symbole']} Inférieur",
                hex_data['bas'],
                f"{trig_bas['freq']} Hz"
            )
    
    with col2:
        # Traits
        st.markdown("#### 📊 Traits tirés")
        
        for i in range(5, -1, -1):  # Du haut vers le bas
            t = traits[i]
            info = FREQ_TRAITS[t]
            
            is_yang = t in [7, 9]
            is_mut = t in [6, 9]
            
            symbole = "━━━━━━━━━" if is_yang else "━━━   ━━━"
            
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
                <strong>{i+1}</strong> {symbole} {info['nom']} ({info['freq']} Hz){mut_icon}
            </div>
            """, unsafe_allow_html=True)
        
        # Mutation
        if hex_mute:
            st.markdown(f"""
            <div class="mutation-card">
                <div style="font-size: 0.9rem;">🔄 MUTATION VERS</div>
                <div style="font-size: 3rem;">{hex_mute['caractere']}</div>
                <div style="font-weight: bold;">{hex_mute['numero']}. {hex_mute['pinyin']}</div>
                <div style="font-style: italic;">{hex_mute['nom']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Grilles
    st.markdown("### 🎮 Grilles La Livrée d'Hermès")
    
    images_path = Path(images_dir)
    
    if images_path.exists():
        gcol1, gcol2 = st.columns(2)
        
        with gcol1:
            grille = generer_grille(traits, images_path, mutation=False)
            if grille:
                st.image(grille, caption="Hexagramme Principal", use_container_width=True)
                
                # Téléchargement
                buf = BytesIO()
                grille.save(buf, format='PNG')
                st.download_button(
                    "📥 Télécharger la grille",
                    buf.getvalue(),
                    f"grille-hex{hex_data['numero']}.png",
                    "image/png"
                )
        
        with gcol2:
            if hex_mute:
                grille_mut = generer_grille(traits, images_path, mutation=True)
                if grille_mut:
                    st.image(grille_mut, caption="Après Mutation", use_container_width=True)
                    
                    buf = BytesIO()
                    grille_mut.save(buf, format='PNG')
                    st.download_button(
                        "📥 Télécharger mutation",
                        buf.getvalue(),
                        f"grille-hex{hex_mute['numero']}-mutation.png",
                        "image/png"
                    )
            else:
                st.info("Pas de mutation (aucun trait mutant)")
    else:
        st.warning(f"⚠️ Dossier images non trouvé : {images_path}")
        st.info("Placez les 24 fichiers PNG des grilles dans le dossier 'images/'")
    
    st.divider()
    
    # Fréquences
    st.markdown("### 🎵 Fréquences Sacrées")
    
    fcol1, fcol2 = st.columns(2)
    
    with fcol1:
        st.markdown("""
        <div class="freq-card">
            <strong>📖 Solfège Ancien</strong><br>
            • 396 Hz - Libération<br>
            • 417 Hz - Transformation<br>
            • 432 Hz - Harmonie universelle<br>
            • 528 Hz - Réparation ADN
        </div>
        """, unsafe_allow_html=True)
    
    with fcol2:
        st.markdown("""
        <div class="freq-card">
            <strong>🎧 Protocole d'écoute</strong><br>
            1. Ancrage : 432 Hz (2 min)<br>
            2. Activation : Trigramme haut (5 min)<br>
            3. Harmonisation (5 min)<br>
            4. Intégration : 528 Hz (3 min)
        </div>
        """, unsafe_allow_html=True)
    
    # Génération audio
    st.markdown("#### 🔊 Séquence Sonore du Tirage")
    
    if st.button("🎵 Générer la séquence audio"):
        with st.spinner("Génération de l'audio..."):
            audio_data = generate_audio_sequence(traits)
            audio_b64 = audio_to_base64(audio_data)
            
            st.audio(f"data:audio/wav;base64,{audio_b64}", format="audio/wav")
            
            # Téléchargement
            audio_buffer = BytesIO()
            wavfile.write(audio_buffer, 44100, audio_data)
            st.download_button(
                "📥 Télécharger l'audio",
                audio_buffer.getvalue(),
                f"yijing-audio-hex{hex_data['numero']}.wav",
                "audio/wav"
            )
    
    st.divider()
    
    # Export PDF
    st.markdown("### 📄 Rapport PDF")
    
    if st.button("📄 Générer le rapport PDF"):
        with st.spinner("Génération du PDF..."):
            grille_for_pdf = None
            if images_path.exists():
                grille_for_pdf = generer_grille(traits, images_path, mutation=False)
            
            pdf_data = generate_pdf_report(
                traits, 
                st.session_state.question, 
                hex_data, 
                hex_mute,
                grille_for_pdf
            )
            
            st.download_button(
                "📥 Télécharger le rapport PDF",
                pdf_data,
                f"yijing-rapport-hex{hex_data['numero']}.pdf",
                "application/pdf"
            )
            
            st.success("✅ Rapport généré avec succès !")

else:
    # Page d'accueil
    st.markdown("""
    ### 🌟 Bienvenue dans l'Oracle du Yi Jing
    
    Le **Yi Jing** (易經), ou *Livre des Mutations*, est l'un des plus anciens textes 
    de sagesse chinoise. Il utilise un système de 64 hexagrammes pour guider 
    la réflexion et la prise de décision.
    
    #### Comment consulter l'oracle ?
    
    1. **Formulez votre question** dans la barre latérale (optionnel)
    2. **Choisissez le mode** : tirage aléatoire ou saisie manuelle
    3. **Cliquez sur "Consulter l'Oracle"**
    4. **Explorez** l'hexagramme, les grilles et les fréquences
    
    #### Les Grilles "La Livrée d'Hermès"
    
    Cette application utilise les grilles créées par **Anibal Edelbert Amiot** 
    pour visualiser de manière unique chaque consultation.
    
    #### Les Fréquences Sacrées
    
    Chaque trigramme et chaque trait est associé à une fréquence du 
    **Solfège ancien** (396-963 Hz), créant une expérience sonore méditative.
    """)
    
    # Tableau des hexagrammes
    with st.expander("📚 Les 64 Hexagrammes"):
        cols = st.columns(4)
        for i, (num, data) in enumerate(HEXAGRAMMES.items()):
            with cols[i % 4]:
                st.write(f"**{num}.** {data['caractere']} {data['pinyin']}")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #9E9E9E; font-size: 0.9rem;">
    易經 Yi Jing Oracle | Grilles : Anibal Edelbert Amiot | CyberMind.FR<br>
    <em>Le changement est la seule constante de l'univers</em>
</div>
""", unsafe_allow_html=True)
