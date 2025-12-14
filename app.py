#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     易經 YI JING ORACLE v2.0                                 ║
║                    Application Streamlit                                     ║
║         avec Grilles "La Livrée d'Hermès" & JSON Complet                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import random
import json
import datetime
import base64
import textwrap
from io import BytesIO
from pathlib import Path

# Imports pour images
from PIL import Image, ImageChops

# Imports pour PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

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
    "K'ien": {"symbole": "☰", "element": "Ciel", "freq": 852},
    "K'ouen": {"symbole": "☷", "element": "Terre", "freq": 396},
    "Tchen": {"symbole": "☳", "element": "Tonnerre", "freq": 417},
    "K'an": {"symbole": "☵", "element": "Eau", "freq": 528},
    "Ken": {"symbole": "☶", "element": "Montagne", "freq": 639},
    "Souen": {"symbole": "☴", "element": "Vent", "freq": 741},
    "Li": {"symbole": "☲", "element": "Feu", "freq": 963},
    "Touei": {"symbole": "☱", "element": "Lac", "freq": 432},
}

FREQ_TRAITS = {
    6: {"freq": 216, "note": "LA-1", "nom": "Yin mutant", "couleur": "#E91E63"},
    7: {"freq": 256, "note": "DO", "nom": "Yang stable", "couleur": "#4CAF50"},
    8: {"freq": 192, "note": "SOL-1", "nom": "Yin stable", "couleur": "#2196F3"},
    9: {"freq": 288, "note": "RÉ", "nom": "Yang mutant", "couleur": "#FF9800"}
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

# ============================================================================
# CHARGEMENT DES DONNÉES JSON
# ============================================================================

@st.cache_data
def load_yijing_data(json_path):
    """Charge les données Yi Jing depuis le fichier JSON"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning(f"⚠️ Fichier JSON non trouvé: {json_path}")
        return {"hexagrammes": []}

def get_hex_from_json(yijing_data, numero):
    """Récupère les données d'un hexagramme depuis le JSON"""
    for h in yijing_data.get('hexagrammes', []):
        if h.get('numero') == numero:
            return h
    return {}

# ============================================================================
# FONCTIONS DE TIRAGE
# ============================================================================

def tirer_trait():
    """Simule le tirage de 3 pièces"""
    return sum(random.choice([2, 3]) for _ in range(3))

def get_hexagramme_numero(traits):
    """Trouve le numéro d'hexagramme correspondant aux traits"""
    binaire = tuple(1 if t in [7, 9] else 0 for t in traits)
    return BINAIRE_TO_HEX.get(binaire, 1)

def get_mutation_numero(traits):
    """Calcule le numéro de l'hexagramme de mutation"""
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
    """Retourne le nom de fichier de l'image"""
    is_yang = trait_val in [7, 9]
    is_mutant = trait_val in [6, 9]
    key = "YANG" if is_yang else "YING"
    if is_mutant:
        key += "-MUT"
    return f"lldh-YY-{key}-{position}.png"

def generer_grille(traits, images_dir, mutation=False):
    """Génère la grille composite avec superposition multiplicative"""
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
        
        # Superposition multiplicative pour préserver les couleurs
        layer_with_bg = Image.new('RGBA', layer.size, (255, 255, 255, 255))
        layer_with_bg = Image.alpha_composite(layer_with_bg, layer)
        composite = ImageChops.multiply(composite, layer_with_bg)
    
    if composite:
        composite = composite.convert('RGB')
    
    return composite

# ============================================================================
# GÉNÉRATION AUDIO
# ============================================================================

def generate_audio_sequence(traits, sample_rate=44100):
    """Génère la séquence audio du tirage"""
    # Drone intro 432 Hz
    t_intro = np.linspace(0, 2, int(sample_rate * 2), False)
    intro = np.sin(2 * np.pi * 432 * t_intro) * 0.3
    silence = np.zeros(int(sample_rate * 0.3))
    
    parts = [intro, silence]
    
    for trait in traits:
        freq = FREQ_TRAITS[trait]['freq']
        t = np.linspace(0, 2, int(sample_rate * 2), False)
        tone = np.sin(2 * np.pi * freq * t) * 0.3
        
        # Battement pour traits mutants
        if trait in [6, 9]:
            beat = np.sin(2 * np.pi * (freq + 3) * t) * 0.15
            tone = tone + beat
        
        # Fade in/out
        fade_len = int(sample_rate * 0.05)
        tone[:fade_len] *= np.linspace(0, 1, fade_len)
        tone[-fade_len:] *= np.linspace(1, 0, fade_len)
        
        parts.append(tone)
        parts.append(silence)
    
    # Accord final
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
    """Convertit audio en base64 pour lecture web"""
    buffer = BytesIO()
    wavfile.write(buffer, sample_rate, audio_data)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode()

# ============================================================================
# GÉNÉRATION PDF
# ============================================================================

def init_cjk_font():
    """Initialise la police CJK pour ReportLab"""
    try:
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        return 'STSong-Light'
    except:
        return None

def generate_pdf_report(traits, question, hex_data, hex_mute_data, grille_img, grille_mut_img=None):
    """Génère le rapport PDF complet avec données JSON"""
    buffer = BytesIO()
    width, height = A4
    margin = 15 * mm
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Initialiser police CJK
    cjk_font = init_cjk_font()
    
    # Couleurs
    marron = HexColor('#8B4513')
    or_color = HexColor('#DAA520')
    creme = HexColor('#FFFAF0')
    gris = HexColor('#5D4037')
    rouge = HexColor('#C62828')
    bleu = HexColor('#1565C0')
    
    hex_numero = get_hexagramme_numero(traits)
    
    # ===== PAGE 1 =====
    # En-tête
    c.setFillColor(marron)
    c.rect(0, height - 40*mm, width, 40*mm, fill=1)
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height - 15*mm, "Yi Jing Oracle")
    
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 24*mm, "Rapport de Consultation - Grilles La Livree d'Hermes")
    
    c.setFont("Helvetica", 8)
    date_str = datetime.datetime.now().strftime("%d/%m/%Y a %H:%M")
    c.drawCentredString(width/2, height - 33*mm, date_str)
    
    y = height - 50*mm
    
    # Question
    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, y, "Question posee :")
    c.setFont("Helvetica", 8)
    question_text = (question[:90] + "...") if len(question) > 90 else question
    c.drawString(margin, y - 5*mm, question_text or "Consultation generale")
    y -= 15*mm
    
    # Hexagramme principal (cadre)
    c.setFillColor(creme)
    c.setStrokeColor(or_color)
    c.setLineWidth(2)
    c.roundRect(margin, y - 42*mm, width - 2*margin, 42*mm, 5, fill=1, stroke=1)
    
    c.setFillColor(marron)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, y - 8*mm, f"HEXAGRAMME {hex_numero}")
    
    # Caractère chinois avec police CJK
    caractere = hex_data.get('caractere', '')
    if caractere and cjk_font:
        c.setFont(cjk_font, 28)
        c.setFillColor(HexColor('#2F4F4F'))
        c.drawCentredString(width/2, y - 23*mm, caractere)
    
    # Nom
    nom = f"{hex_data.get('nom_pinyin', '')} - {hex_data.get('nom_fr', '')}"
    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, y - 37*mm, nom)
    
    y -= 52*mm
    
    # Traits
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(gris)
    c.drawString(margin, y, "Traits tires et Frequences :")
    y -= 5*mm
    
    for i, t in enumerate(traits):
        info = FREQ_TRAITS[t]
        is_mutant = t in [6, 9]
        c.setFillColor(rouge if is_mutant else gris)
        
        symbole = "-----" if t in [7, 9] else "-- --"
        mut = " [MUTANT]" if is_mutant else ""
        
        c.setFont("Helvetica", 7)
        c.drawString(margin + 3*mm, y, 
            f"Trait {i+1}: {symbole}  {info['nom']} ({info['freq']} Hz){mut}")
        y -= 4*mm
    
    y -= 5*mm
    
    # Trigrammes
    trig_haut = hex_data.get('trigramme_haut', '')
    trig_bas = hex_data.get('trigramme_bas', '')
    trig_h_info = TRIGRAMMES.get(trig_haut, {})
    trig_b_info = TRIGRAMMES.get(trig_bas, {})
    
    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(margin, y, "Trigrammes :")
    y -= 4*mm
    c.setFont("Helvetica", 7)
    c.drawString(margin + 3*mm, y, 
        f"Superieur: {trig_h_info.get('symbole', '')} {trig_haut} ({trig_h_info.get('freq', 0)} Hz) - {hex_data.get('trigramme_haut_desc', '')[:45]}")
    y -= 4*mm
    c.drawString(margin + 3*mm, y,
        f"Inferieur: {trig_b_info.get('symbole', '')} {trig_bas} ({trig_b_info.get('freq', 0)} Hz) - {hex_data.get('trigramme_bas_desc', '')[:45]}")
    
    y -= 8*mm
    
    # Grille
    if grille_img:
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(bleu)
        c.drawString(margin, y, "Grille La Livree d'Hermes :")
        y -= 3*mm
        
        img_buffer = BytesIO()
        grille_img.save(img_buffer, 'PNG')
        img_buffer.seek(0)
        
        from reportlab.lib.utils import ImageReader
        img_reader = ImageReader(img_buffer)
        c.drawImage(img_reader, margin, y - 60*mm, width=45*mm, height=60*mm, preserveAspectRatio=True)
        
        # Description à côté
        text_x = margin + 50*mm
        text_y = y - 5*mm
        
        c.setFillColor(gris)
        c.setFont("Helvetica", 6)
        
        desc = hex_data.get('description', '')
        if desc:
            lines = textwrap.wrap(desc, 50)
            for line in lines[:14]:
                c.drawString(text_x, text_y, line)
                text_y -= 3.5*mm
    
    # Pied de page 1
    c.setFillColor(HexColor('#9E9E9E'))
    c.setFont("Helvetica", 6)
    c.drawCentredString(width/2, 8*mm, "Yi Jing Oracle v2.0 - CyberMind.FR | Grilles: Anibal Edelbert Amiot | Page 1")
    
    # ===== PAGE 2 : JUGEMENT & IMAGE =====
    c.showPage()
    y = height - 20*mm
    
    c.setFillColor(marron)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, y, f"Hexagramme {hex_numero} - Textes Traditionnels")
    y -= 12*mm
    
    # Jugement
    jugement = hex_data.get('jugement_texte', '')
    if jugement:
        c.setFillColor(HexColor('#FFF3E0'))
        c.setStrokeColor(HexColor('#FF9800'))
        c.setLineWidth(1)
        
        jug_lines = textwrap.wrap(jugement, 95)
        box_height = min(len(jug_lines) * 3.5 + 12, 55) * mm
        
        c.roundRect(margin, y - box_height, width - 2*margin, box_height, 3, fill=1, stroke=1)
        
        c.setFillColor(HexColor('#E65100'))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin + 4*mm, y - 7*mm, "LE JUGEMENT")
        
        c.setFillColor(gris)
        c.setFont("Helvetica", 7)
        text_y = y - 13*mm
        for line in jug_lines[:12]:
            c.drawString(margin + 4*mm, text_y, line)
            text_y -= 3.5*mm
        
        y -= box_height + 6*mm
    
    # Image
    image_texte = hex_data.get('image_texte', '')
    if image_texte:
        c.setFillColor(HexColor('#E3F2FD'))
        c.setStrokeColor(HexColor('#2196F3'))
        c.setLineWidth(1)
        
        img_lines = textwrap.wrap(image_texte, 95)
        box_height = min(len(img_lines) * 3.5 + 12, 45) * mm
        
        c.roundRect(margin, y - box_height, width - 2*margin, box_height, 3, fill=1, stroke=1)
        
        c.setFillColor(bleu)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin + 4*mm, y - 7*mm, "L'IMAGE")
        
        c.setFillColor(gris)
        c.setFont("Helvetica", 7)
        text_y = y - 13*mm
        for line in img_lines[:10]:
            c.drawString(margin + 4*mm, text_y, line)
            text_y -= 3.5*mm
        
        y -= box_height + 6*mm
    
    # Traits mutants
    traits_mutants = [(i, traits[i]) for i in range(6) if traits[i] in [6, 9]]
    hex_traits = hex_data.get('traits', [])
    
    if traits_mutants and hex_traits:
        c.setFillColor(rouge)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin, y, "TRAITS MUTANTS - A lire attentivement :")
        y -= 6*mm
        
        for pos, val in traits_mutants:
            trait_data = next((t for t in hex_traits if t.get('position') == pos + 1), None)
            if trait_data:
                c.setFillColor(rouge)
                c.setFont("Helvetica-Bold", 7)
                titre = trait_data.get('titre', f'Trait {pos+1}')
                c.drawString(margin + 2*mm, y, titre[:65])
                y -= 4*mm
                
                c.setFillColor(gris)
                c.setFont("Helvetica", 6)
                texte = trait_data.get('texte', '')
                for line in textwrap.wrap(texte, 105)[:5]:
                    c.drawString(margin + 4*mm, y, line)
                    y -= 3*mm
                
                y -= 2*mm
                
                if y < 35*mm:
                    break
    
    c.setFillColor(HexColor('#9E9E9E'))
    c.setFont("Helvetica", 6)
    c.drawCentredString(width/2, 8*mm, "Page 2")
    
    # ===== PAGE 3 : MUTATION =====
    hex_mute_numero = get_mutation_numero(traits)
    if hex_mute_numero and hex_mute_data:
        c.showPage()
        y = height - 20*mm
        
        c.setFillColor(HexColor('#E91E63'))
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width/2, y, "HEXAGRAMME DE MUTATION")
        y -= 12*mm
        
        # Cadre mutation
        c.setFillColor(HexColor('#FCE4EC'))
        c.setStrokeColor(HexColor('#E91E63'))
        c.setLineWidth(2)
        c.roundRect(margin, y - 38*mm, width - 2*margin, 38*mm, 5, fill=1, stroke=1)
        
        c.setFillColor(HexColor('#AD1457'))
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(width/2, y - 7*mm, f"HEXAGRAMME {hex_mute_numero}")
        
        # Caractère
        car_mut = hex_mute_data.get('caractere', '')
        if car_mut and cjk_font:
            c.setFont(cjk_font, 24)
            c.drawCentredString(width/2, y - 20*mm, car_mut)
        
        nom_mut = f"{hex_mute_data.get('nom_pinyin', '')} - {hex_mute_data.get('nom_fr', '')}"
        c.setFillColor(gris)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(width/2, y - 33*mm, nom_mut)
        
        y -= 48*mm
        
        # Grille mutation
        if grille_mut_img:
            img_buffer = BytesIO()
            grille_mut_img.save(img_buffer, 'PNG')
            img_buffer.seek(0)
            
            from reportlab.lib.utils import ImageReader
            img_reader = ImageReader(img_buffer)
            c.drawImage(img_reader, margin, y - 55*mm, width=40*mm, height=55*mm, preserveAspectRatio=True)
            
            # Description mutation
            desc_mut = hex_mute_data.get('description', '')
            if desc_mut:
                text_x = margin + 45*mm
                c.setFillColor(gris)
                c.setFont("Helvetica", 6)
                text_y = y - 5*mm
                for line in textwrap.wrap(desc_mut, 55)[:15]:
                    c.drawString(text_x, text_y, line)
                    text_y -= 3.5*mm
            
            y -= 60*mm
        
        # Jugement mutation
        jug_mut = hex_mute_data.get('jugement_texte', '')
        if jug_mut and y > 50*mm:
            c.setFillColor(HexColor('#FFF3E0'))
            c.setStrokeColor(HexColor('#FF9800'))
            lines = textwrap.wrap(jug_mut, 95)
            bh = min(len(lines) * 3.5 + 10, 35) * mm
            c.roundRect(margin, y - bh, width - 2*margin, bh, 3, fill=1, stroke=1)
            c.setFillColor(HexColor('#E65100'))
            c.setFont("Helvetica-Bold", 8)
            c.drawString(margin + 4*mm, y - 6*mm, "Jugement")
            c.setFillColor(gris)
            c.setFont("Helvetica", 6)
            ty = y - 11*mm
            for line in lines[:8]:
                c.drawString(margin + 4*mm, ty, line)
                ty -= 3*mm
        
        c.setFillColor(HexColor('#9E9E9E'))
        c.setFont("Helvetica", 6)
        c.drawCentredString(width/2, 8*mm, "Page 3")
    
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
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.3rem;
    }
    
    .hex-card {
        background: linear-gradient(135deg, #FFFAF0 0%, #FFF8DC 100%);
        border: 3px solid #DAA520;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .hex-caractere {
        font-size: 4rem;
        color: #2F4F4F;
    }
    
    .hex-nom {
        font-size: 1.3rem;
        color: #8B4513;
        font-weight: bold;
    }
    
    .trait-box {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        margin: 0.15rem;
        border-radius: 8px;
        font-family: monospace;
        font-size: 0.95rem;
    }
    
    .trait-yang { background: #E8F5E9; border: 2px solid #4CAF50; }
    .trait-yin { background: #E3F2FD; border: 2px solid #2196F3; }
    .trait-yang-mut { background: #FFF3E0; border: 2px solid #FF9800; }
    .trait-yin-mut { background: #FCE4EC; border: 2px solid #E91E63; }
    
    .mutation-card {
        background: linear-gradient(135deg, #FCE4EC 0%, #F8BBD9 100%);
        border: 3px solid #E91E63;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .text-box {
        background: #FFFEF9;
        border-left: 4px solid #DAA520;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    .jugement-box { border-left-color: #FF9800; background: #FFF8E1; }
    .image-box { border-left-color: #2196F3; background: #E3F2FD; }
    .trait-mut-box { border-left-color: #E91E63; background: #FCE4EC; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# APPLICATION PRINCIPALE
# ============================================================================

# Initialiser le state
if 'traits' not in st.session_state:
    st.session_state.traits = None
if 'question' not in st.session_state:
    st.session_state.question = ""

# Header
st.markdown("""
<div class="main-header">
    <h1>☯ 易經 Yi Jing Oracle</h1>
    <p>Grilles "La Livrée d'Hermès" • Fréquences Sacrées 432 Hz • JSON Complet</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎴 Consultation")
    
    question = st.text_area(
        "Votre question :",
        placeholder="Quelle direction prendre ?",
        height=80
    )
    
    st.divider()
    
    mode = st.radio(
        "Mode de tirage :",
        ["🎲 Tirage aléatoire", "✏️ Saisie manuelle"]
    )
    
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
    
    st.divider()
    
    # Configuration
    json_path = st.text_input("📄 Fichier JSON :", value="yijing_complet.json")
    images_dir = st.text_input("📁 Dossier images :", value="images")

# Charger les données JSON
yijing_data = load_yijing_data(json_path)

# Contenu principal
if st.session_state.traits is not None:
    traits = st.session_state.traits
    hex_numero = get_hexagramme_numero(traits)
    hex_mute_numero = get_mutation_numero(traits)
    
    hex_data = get_hex_from_json(yijing_data, hex_numero)
    hex_mute_data = get_hex_from_json(yijing_data, hex_mute_numero) if hex_mute_numero else {}
    
    # Colonnes principales
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Hexagramme principal
        caractere = hex_data.get('caractere', '')
        nom_pinyin = hex_data.get('nom_pinyin', '')
        nom_fr = hex_data.get('nom_fr', '')
        
        st.markdown(f"""
        <div class="hex-card">
            <div style="font-size: 0.85rem; color: #8B4513;">HEXAGRAMME {hex_numero}</div>
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
        
        st.markdown("#### ☯ Trigrammes")
        tcol1, tcol2 = st.columns(2)
        with tcol1:
            st.metric(
                f"{trig_h_info.get('symbole', '')} Supérieur",
                trig_haut,
                f"{trig_h_info.get('freq', 0)} Hz"
            )
        with tcol2:
            st.metric(
                f"{trig_b_info.get('symbole', '')} Inférieur",
                trig_bas,
                f"{trig_b_info.get('freq', 0)} Hz"
            )
    
    with col2:
        # Traits
        st.markdown("#### 📊 Traits tirés")
        
        for i in range(5, -1, -1):
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
        if hex_mute_numero:
            car_mut = hex_mute_data.get('caractere', '')
            st.markdown(f"""
            <div class="mutation-card">
                <div style="font-size: 0.85rem;">🔄 MUTATION VERS</div>
                <div style="font-size: 2.5rem;">{car_mut}</div>
                <div style="font-weight: bold;">{hex_mute_numero}. {hex_mute_data.get('nom_pinyin', '')}</div>
                <div style="font-style: italic;">{hex_mute_data.get('nom_fr', '')}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Textes traditionnels
    st.markdown("### 📜 Textes Traditionnels")
    
    # Description
    desc = hex_data.get('description', '')
    if desc:
        with st.expander("📖 Description", expanded=True):
            st.write(desc)
    
    # Jugement
    jugement = hex_data.get('jugement_texte', '')
    if jugement:
        st.markdown(f"""
        <div class="text-box jugement-box">
            <strong>⚖️ Le Jugement</strong><br>{jugement}
        </div>
        """, unsafe_allow_html=True)
    
    # Image
    image_texte = hex_data.get('image_texte', '')
    if image_texte:
        st.markdown(f"""
        <div class="text-box image-box">
            <strong>🖼️ L'Image</strong><br>{image_texte}
        </div>
        """, unsafe_allow_html=True)
    
    # Traits mutants
    traits_mutants = [(i, traits[i]) for i in range(6) if traits[i] in [6, 9]]
    hex_traits = hex_data.get('traits', [])
    
    if traits_mutants and hex_traits:
        st.markdown("#### 🔄 Traits Mutants")
        for pos, val in traits_mutants:
            trait_data = next((t for t in hex_traits if t.get('position') == pos + 1), None)
            if trait_data:
                st.markdown(f"""
                <div class="text-box trait-mut-box">
                    <strong>{trait_data.get('titre', f'Trait {pos+1}')}</strong><br>
                    {trait_data.get('texte', '')}
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # Grilles
    st.markdown("### 🎮 Grilles La Livrée d'Hermès")
    
    images_path = Path(images_dir)
    
    if images_path.exists():
        gcol1, gcol2 = st.columns(2)
        
        grille = generer_grille(traits, images_path, mutation=False)
        grille_mut = generer_grille(traits, images_path, mutation=True) if hex_mute_numero else None
        
        with gcol1:
            if grille:
                st.image(grille, caption=f"Hexagramme {hex_numero}", use_container_width=True)
                buf = BytesIO()
                grille.save(buf, format='PNG')
                st.download_button("📥 Télécharger", buf.getvalue(), f"grille-hex{hex_numero}.png", "image/png")
        
        with gcol2:
            if grille_mut:
                st.image(grille_mut, caption=f"Mutation → Hex {hex_mute_numero}", use_container_width=True)
                buf = BytesIO()
                grille_mut.save(buf, format='PNG')
                st.download_button("📥 Télécharger mutation", buf.getvalue(), f"grille-hex{hex_mute_numero}-mutation.png", "image/png")
            else:
                st.info("Pas de mutation")
    else:
        st.warning(f"⚠️ Dossier images non trouvé: {images_path}")
    
    st.divider()
    
    # Exports
    st.markdown("### 📦 Exports")
    
    exp_col1, exp_col2 = st.columns(2)
    
    with exp_col1:
        st.markdown("#### 🎵 Audio")
        if st.button("🔊 Générer séquence audio"):
            with st.spinner("Génération..."):
                audio_data = generate_audio_sequence(traits)
                audio_b64 = audio_to_base64(audio_data)
                st.audio(f"data:audio/wav;base64,{audio_b64}", format="audio/wav")
                
                audio_buffer = BytesIO()
                wavfile.write(audio_buffer, 44100, audio_data)
                st.download_button("📥 Télécharger WAV", audio_buffer.getvalue(), f"yijing-audio-hex{hex_numero}.wav", "audio/wav")
    
    with exp_col2:
        st.markdown("#### 📄 Rapport PDF")
        if st.button("📄 Générer rapport PDF"):
            with st.spinner("Génération du PDF..."):
                grille = generer_grille(traits, images_path, mutation=False) if images_path.exists() else None
                grille_mut = generer_grille(traits, images_path, mutation=True) if hex_mute_numero and images_path.exists() else None
                
                pdf_data = generate_pdf_report(
                    traits, 
                    st.session_state.question, 
                    hex_data, 
                    hex_mute_data,
                    grille,
                    grille_mut
                )
                
                st.download_button("📥 Télécharger PDF", pdf_data, f"yijing-rapport-hex{hex_numero}.pdf", "application/pdf")
                st.success("✅ PDF généré!")

else:
    # Page d'accueil
    st.markdown("""
    ### 🌟 Bienvenue dans l'Oracle du Yi Jing v2.0
    
    Le **Yi Jing** (易經), ou *Livre des Mutations*, est l'un des plus anciens textes 
    de sagesse chinoise. Cette version intègre les données complètes des 64 hexagrammes.
    
    #### Nouveautés v2.0 :
    - ✅ **Données JSON complètes** : 64 hexagrammes avec textes traditionnels
    - ✅ **Caractères chinois** : Affichage correct dans le PDF
    - ✅ **Grilles couleur** : Violet et orange préservés
    - ✅ **Traits mutants** : Interprétation détaillée
    
    #### Comment utiliser :
    1. Formulez votre question dans la barre latérale
    2. Choisissez le mode de tirage
    3. Cliquez sur "Consulter l'Oracle"
    4. Explorez les résultats et exportez!
    """)
    
    # Aperçu des fréquences
    with st.expander("🎵 Fréquences du Solfège Sacré"):
        for freq, desc in FREQ_SOLFEGGIO.items():
            st.write(f"**{freq} Hz** : {desc}")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #9E9E9E; font-size: 0.85rem;">
    易經 Yi Jing Oracle v2.0 | Grilles : Anibal Edelbert Amiot | CyberMind.FR<br>
    <em>Le changement est la seule constante de l'univers</em>
</div>
""", unsafe_allow_html=True)
