#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     易經 YI JING ORACLE v2.1                                 ║
║                    Application Streamlit                                     ║
║         avec Grilles "La Livrée d'Hermès" & Méditation Kasina KBS           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Génère des sessions KBS (Kasina Basic Session) conformes au format Mindplace.
Basé sur la documentation officielle KBS v2.
"""

import streamlit as st
import random
import json
import datetime
import base64
import textwrap
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

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
# DONNÉES KASINA - FORMAT KBS v2 OFFICIEL MINDPLACE
# ============================================================================

# Correspondance trigrammes -> couleurs RGB (0-100% selon spec KBS)
# Basé sur les éléments et principes AVS (bleu=Alpha/relaxation, rouge=Beta/éveil)
KASINA_RGB = {
    "K'ien": (100, 100, 100),   # Blanc - Ciel (spirituel)
    "K'ouen": (60, 40, 20),     # Ambre/Marron - Terre (ancrage, SMR)
    "Tchen": (100, 80, 0),      # Or/Jaune - Tonnerre (énergie)
    "K'an": (0, 40, 100),       # Bleu profond - Eau (Alpha, relaxation)
    "Ken": (50, 50, 60),        # Gris-bleu - Montagne (calme)
    "Souen": (30, 100, 50),     # Vert - Vent (SMR, relaxation)
    "Li": (100, 30, 0),         # Rouge-orange - Feu (Beta, éveil)
    "Touei": (0, 70, 100),      # Cyan - Lac (Alpha, harmonie)
}

# Waveforms KBS disponibles
KBS_WAVEFORMS = ["Sine", "Square", "Triangle", "SawUp", "SawDown", "PinkNoise"]

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

# ============================================================================
# GÉNÉRATION AUDIO TIRAGE
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
# GÉNÉRATION KASINA KBS - FORMAT OFFICIEL MINDPLACE v2
# ============================================================================

def generate_kbs_session(hex_data, duration_minutes=5):
    """
    Génère une session KBS (Kasina Basic Session) au format officiel Mindplace.
    
    Selon la documentation KBS v2:
    - Les valeurs des paramètres "rampent" d'un segment au suivant
    - Les valeurs définies dans un segment sont atteintes à la FIN du segment
    - Beat = fréquence de stimulation (lumière et son pulsé)
    - LPtch/RPtch = pitch gauche/droite pour binaural (différence = freq binaural)
    - SAMDpth=0 = binaural pur sans pulsation isochronique
    - ColorControlMode=3 = couleurs RGB personnalisées par segment
    
    Structure méditation Yi Jing (5 minutes):
    - Phase 1 (60s)  : Ancrage Alpha 10 Hz, 432 Hz (Résonance Schumann proche)
    - Phase 2 (90s)  : Trigramme inférieur, Theta 7 Hz  
    - Phase 3 (90s)  : Trigramme supérieur, Theta 5 Hz
    - Phase 4 (60s)  : Intégration Alpha 8 Hz, 528 Hz (transformation)
    """
    
    trig_bas = hex_data.get('trigramme_bas', 'Touei')
    trig_haut = hex_data.get('trigramme_haut', 'Li')
    
    freq_bas = TRIGRAMMES.get(trig_bas, {}).get('freq', 432)
    freq_haut = TRIGRAMMES.get(trig_haut, {}).get('freq', 528)
    
    rgb_bas = KASINA_RGB.get(trig_bas, (0, 70, 100))
    rgb_haut = KASINA_RGB.get(trig_haut, (100, 30, 0))
    
    hex_num = hex_data.get('numero', 0)
    hex_name = hex_data.get('nom_fr', 'Hexagramme')
    
    # En-tête KBS avec commentaires explicatifs
    kbs = []
    kbs.append(f"; ═══════════════════════════════════════════════════════════════")
    kbs.append(f"; Yi Jing Meditation - Hexagramme {hex_num}: {hex_name}")
    kbs.append(f"; ═══════════════════════════════════════════════════════════════")
    kbs.append(f"; Trigramme Bas: {trig_bas} ({freq_bas} Hz) - {TRIGRAMMES.get(trig_bas, {}).get('element', '')}")
    kbs.append(f"; Trigramme Haut: {trig_haut} ({freq_haut} Hz) - {TRIGRAMMES.get(trig_haut, {}).get('element', '')}")
    kbs.append(f"; Duration: {duration_minutes} minutes")
    kbs.append(f"; Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    kbs.append("; By: Yi Jing Oracle v2.1 - CyberMind.FR")
    kbs.append(";")
    kbs.append("; Format: KBS v2 - Mindplace Kasina/Limina")
    kbs.append("; Reference: Kbs-v2-description-1.pdf")
    kbs.append(";")
    kbs.append("; AVS Principles Applied:")
    kbs.append("; - Alpha (8-13 Hz): Relaxation, visualization, Schumann resonance")
    kbs.append("; - Theta (4-7 Hz): Deep meditation, memory, unconscious access")
    kbs.append("; - Binaural: LPtch/RPtch difference creates FFR entrainment")
    kbs.append("; - SAMDpth=0: Pure binaural without isochronic sound pulses")
    kbs.append("; - Sine waveforms: Best for relaxation (per R. Austin)")
    kbs.append("; - Blue enhances Alpha, Green increases SMR")
    kbs.append(";")
    kbs.append("")
    
    # Paramètres globaux selon spec KBS
    kbs.append("[Global]")
    kbs.append("; ColorControlMode: 0=Device, 1=GlobalCS, 2=SegmentCS, 3=RGB")
    kbs.append("ColorControlMode=3")
    kbs.append("GlobalColorSet=1")
    kbs.append("")
    
    # Définition des segments
    # Note: Les valeurs sont atteintes à la FIN du segment (rampe progressive)
    segments = [
        {
            "name": "Fade In - Preparation",
            "description": "Demarrage doux, preparation mentale",
            "Time": 5.00,
            "Beat": 10.00,
            "LPtch": 432.00,
            "RPtch": 442.00,  # 10 Hz binaural Alpha
            "LPhse": 50,
            "SPhse": 50,
            "LAMDpth": 50,
            "SAMDpth": 0,     # Binaural pur
            "Bright": 30,
            "Vol": 30,
            "SndWF": "Sine",
            "SndModWF": "Sine",
            "LgtModWF": "Sine",
            "LgtModPW": 50,
            "SndPW": 50,
            "SndModPW": 50,
            "Red": 40, "Green": 0, "Blue": 80,
        },
        {
            "name": "Ancrage Alpha - 432 Hz",
            "description": "Frequence Terre, Alpha 10 Hz, relaxation",
            "Time": 55.00,
            "Beat": 10.00,
            "LPtch": 432.00,
            "RPtch": 442.00,
            "LPhse": 50,
            "SPhse": 50,
            "LAMDpth": 70,
            "SAMDpth": 0,
            "Bright": 60,
            "Vol": 50,
            "SndWF": "Sine",
            "SndModWF": "Sine",
            "LgtModWF": "Sine",
            "LgtModPW": 50,
            "SndPW": 50,
            "SndModPW": 50,
            "Red": 40, "Green": 0, "Blue": 100,
        },
        {
            "name": "Transition Theta",
            "description": "Descente vers Theta, preparation trigramme bas",
            "Time": 15.00,
            "Beat": 8.00,
            "LPtch": float(freq_bas),
            "RPtch": float(freq_bas + 7),
            "LPhse": 50,
            "SPhse": 50,
            "LAMDpth": 65,
            "SAMDpth": 0,
            "Bright": 55,
            "Vol": 55,
            "SndWF": "Sine",
            "SndModWF": "Sine",
            "LgtModWF": "Sine",
            "LgtModPW": 50,
            "SndPW": 50,
            "SndModPW": 50,
            "Red": rgb_bas[0], "Green": rgb_bas[1], "Blue": rgb_bas[2],
        },
        {
            "name": f"Trigramme {trig_bas} - Theta 7 Hz",
            "description": f"Element {TRIGRAMMES.get(trig_bas, {}).get('element', '')}, meditation profonde",
            "Time": 75.00,
            "Beat": 7.00,
            "LPtch": float(freq_bas),
            "RPtch": float(freq_bas + 7),
            "LPhse": 50,
            "SPhse": 50,
            "LAMDpth": 80,
            "SAMDpth": 0,
            "Bright": 55,
            "Vol": 60,
            "SndWF": "Sine",
            "SndModWF": "Sine",
            "LgtModWF": "Sine",
            "LgtModPW": 50,
            "SndPW": 50,
            "SndModPW": 50,
            "Red": rgb_bas[0], "Green": rgb_bas[1], "Blue": rgb_bas[2],
        },
        {
            "name": "Transition Trigramme Superieur",
            "description": "Passage vers trigramme haut, Theta profond",
            "Time": 15.00,
            "Beat": 6.00,
            "LPtch": float((freq_bas + freq_haut) // 2),
            "RPtch": float((freq_bas + freq_haut) // 2 + 6),
            "LPhse": 50,
            "SPhse": 50,
            "LAMDpth": 75,
            "SAMDpth": 0,
            "Bright": 50,
            "Vol": 58,
            "SndWF": "Sine",
            "SndModWF": "Sine",
            "LgtModWF": "Sine",
            "LgtModPW": 50,
            "SndPW": 50,
            "SndModPW": 50,
            "Red": (rgb_bas[0] + rgb_haut[0]) // 2,
            "Green": (rgb_bas[1] + rgb_haut[1]) // 2,
            "Blue": (rgb_bas[2] + rgb_haut[2]) // 2,
        },
        {
            "name": f"Trigramme {trig_haut} - Theta 5 Hz",
            "description": f"Element {TRIGRAMMES.get(trig_haut, {}).get('element', '')}, insight spirituel",
            "Time": 75.00,
            "Beat": 5.00,
            "LPtch": float(freq_haut),
            "RPtch": float(freq_haut + 5),
            "LPhse": 50,
            "SPhse": 50,
            "LAMDpth": 85,
            "SAMDpth": 0,
            "Bright": 50,
            "Vol": 55,
            "SndWF": "Sine",
            "SndModWF": "Sine",
            "LgtModWF": "Sine",
            "LgtModPW": 50,
            "SndPW": 50,
            "SndModPW": 50,
            "Red": rgb_haut[0], "Green": rgb_haut[1], "Blue": rgb_haut[2],
        },
        {
            "name": "Transition Retour Alpha",
            "description": "Remontee progressive vers Alpha",
            "Time": 15.00,
            "Beat": 7.00,
            "LPtch": 528.00,
            "RPtch": 536.00,
            "LPhse": 50,
            "SPhse": 50,
            "LAMDpth": 70,
            "SAMDpth": 0,
            "Bright": 45,
            "Vol": 50,
            "SndWF": "Sine",
            "SndModWF": "Sine",
            "LgtModWF": "Sine",
            "LgtModPW": 50,
            "SndPW": 50,
            "SndModPW": 50,
            "Red": 0, "Green": 80, "Blue": 50,
        },
        {
            "name": "Integration 528 Hz - Alpha 8 Hz",
            "description": "Frequence transformation, integration des insights",
            "Time": 35.00,
            "Beat": 8.00,
            "LPtch": 528.00,
            "RPtch": 536.00,
            "LPhse": 50,
            "SPhse": 50,
            "LAMDpth": 60,
            "SAMDpth": 0,
            "Bright": 40,
            "Vol": 45,
            "SndWF": "Sine",
            "SndModWF": "Sine",
            "LgtModWF": "Sine",
            "LgtModPW": 50,
            "SndPW": 50,
            "SndModPW": 50,
            "Red": 0, "Green": 100, "Blue": 50,
        },
        {
            "name": "Fade Out",
            "description": "Retour doux a la conscience normale",
            "Time": 10.00,
            "Beat": 10.00,
            "LPtch": 528.00,
            "RPtch": 538.00,
            "LPhse": 50,
            "SPhse": 50,
            "LAMDpth": 20,
            "SAMDpth": 0,
            "Bright": 0,
            "Vol": 0,
            "SndWF": "Sine",
            "SndModWF": "Sine",
            "LgtModWF": "Sine",
            "LgtModPW": 50,
            "SndPW": 50,
            "SndModPW": 50,
            "Red": 0, "Green": 40, "Blue": 30,
        },
    ]
    
    # Générer les segments au format KBS officiel
    for i, seg in enumerate(segments):
        kbs.append(f"[Segment{i}]")
        kbs.append(f"; {seg['name']}")
        kbs.append(f"; {seg['description']}")
        kbs.append(f"Time={seg['Time']:.2f}")
        kbs.append(f"Beat={seg['Beat']:.2f}")
        kbs.append(f"LPtch={seg['LPtch']:.2f}")
        kbs.append(f"RPtch={seg['RPtch']:.2f}")
        kbs.append(f"LPhse={seg['LPhse']}")
        kbs.append(f"SPhse={seg['SPhse']}")
        kbs.append(f"LAMDpth={seg['LAMDpth']}")
        kbs.append(f"SAMDpth={seg['SAMDpth']}")
        kbs.append(f"Bright={seg['Bright']}")
        kbs.append(f"Vol={seg['Vol']}")
        kbs.append(f"SndWF={seg['SndWF']}")
        kbs.append(f"SndModWF={seg['SndModWF']}")
        kbs.append(f"LgtModWF={seg['LgtModWF']}")
        kbs.append(f"LgtModPW={seg['LgtModPW']}")
        kbs.append(f"SndPW={seg['SndPW']}")
        kbs.append(f"SndModPW={seg['SndModPW']}")
        kbs.append(f"Red={seg['Red']}")
        kbs.append(f"Green={seg['Green']}")
        kbs.append(f"Blue={seg['Blue']}")
        kbs.append("")
    
    kbs.append("; ═══════════════════════════════════════════════════════════════")
    kbs.append("; END OF SESSION")
    kbs.append("; ═══════════════════════════════════════════════════════════════")
    
    return "\n".join(kbs), segments

def generate_kasina_binaural_audio(segments, sample_rate=44100):
    """
    Génère le fichier audio WAV stéréo avec battements binauraux
    correspondant à la session KBS.
    
    Selon la doc AVS: le battement binaural est perçu comme la différence
    entre les fréquences gauche et droite. Nécessite un casque.
    """
    audio_parts = []
    
    for seg in segments:
        duration = seg['Time']
        l_pitch = seg['LPtch']
        r_pitch = seg['RPtch']
        vol = seg['Vol'] / 100.0
        
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # Canaux gauche et droite avec fréquences différentes
        left = np.sin(2 * np.pi * l_pitch * t) * vol
        right = np.sin(2 * np.pi * r_pitch * t) * vol
        
        stereo = np.column_stack((left, right))
        
        # Crossfade doux entre segments
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
# GÉNÉRATION PDF
# ============================================================================

def init_cjk_font():
    try:
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        return 'STSong-Light'
    except:
        return None

def generate_pdf_report(traits, question, hex_data, hex_mute_data, grille_img, grille_mut_img=None):
    buffer = BytesIO()
    width, height = A4
    margin = 15 * mm
    c = canvas.Canvas(buffer, pagesize=A4)
    
    cjk_font = init_cjk_font()
    
    marron = HexColor('#8B4513')
    or_color = HexColor('#DAA520')
    creme = HexColor('#FFFAF0')
    gris = HexColor('#5D4037')
    rouge = HexColor('#C62828')
    bleu = HexColor('#1565C0')
    
    hex_numero = get_hexagramme_numero(traits)
    
    # PAGE 1
    c.setFillColor(marron)
    c.rect(0, height - 40*mm, width, 40*mm, fill=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height - 15*mm, "Yi Jing Oracle")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 24*mm, "Rapport de Consultation")
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, height - 33*mm, datetime.datetime.now().strftime("%d/%m/%Y a %H:%M"))
    
    y = height - 50*mm
    
    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, y, "Question posee :")
    c.setFont("Helvetica", 8)
    question_text = (question[:90] + "...") if len(question) > 90 else question
    c.drawString(margin, y - 5*mm, question_text or "Consultation generale")
    y -= 15*mm
    
    c.setFillColor(creme)
    c.setStrokeColor(or_color)
    c.setLineWidth(2)
    c.roundRect(margin, y - 42*mm, width - 2*margin, 42*mm, 5, fill=1, stroke=1)
    
    c.setFillColor(marron)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, y - 8*mm, f"HEXAGRAMME {hex_numero}")
    
    caractere = hex_data.get('caractere', '')
    if caractere and cjk_font:
        c.setFont(cjk_font, 28)
        c.setFillColor(HexColor('#2F4F4F'))
        c.drawCentredString(width/2, y - 23*mm, caractere)
    
    nom = f"{hex_data.get('nom_pinyin', '')} - {hex_data.get('nom_fr', '')}"
    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, y - 37*mm, nom)
    y -= 52*mm
    
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(gris)
    c.drawString(margin, y, "Traits tires :")
    y -= 5*mm
    
    for i, t in enumerate(traits):
        info = FREQ_TRAITS[t]
        is_mutant = t in [6, 9]
        c.setFillColor(rouge if is_mutant else gris)
        symbole = "-----" if t in [7, 9] else "-- --"
        mut = " [MUTANT]" if is_mutant else ""
        c.setFont("Helvetica", 7)
        c.drawString(margin + 3*mm, y, f"Trait {i+1}: {symbole}  {info['nom']} ({info['freq']} Hz){mut}")
        y -= 4*mm
    
    y -= 5*mm
    
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
    
    c.setFillColor(HexColor('#9E9E9E'))
    c.setFont("Helvetica", 6)
    c.drawCentredString(width/2, 8*mm, "Yi Jing Oracle v2.1 - CyberMind.FR")
    
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
    .hex-card {
        background: linear-gradient(135deg, #FFFAF0 0%, #FFF8DC 100%);
        border: 3px solid #DAA520;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .hex-caractere { font-size: 4rem; color: #2F4F4F; }
    .hex-nom { font-size: 1.3rem; color: #8B4513; font-weight: bold; }
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
    }
    .kasina-box {
        background: linear-gradient(135deg, #E8EAF6 0%, #C5CAE9 100%);
        border: 2px solid #3F51B5;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .phase-item {
        display: flex;
        align-items: center;
        margin: 4px 0;
        padding: 8px;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #3F51B5;
    }
    .phase-color {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        margin-right: 12px;
        border: 2px solid #fff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
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

# Header
st.markdown("""
<div class="main-header">
    <h1>☯ 易經 Yi Jing Oracle v2.1</h1>
    <p>Grilles "La Livrée d'Hermès" • Fréquences Sacrées 432 Hz • Méditation Kasina KBS</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎴 Consultation")
    question = st.text_area("Votre question :", placeholder="Quelle direction prendre ?", height=80)
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
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
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
        
        trig_haut = hex_data.get('trigramme_haut', '')
        trig_bas = hex_data.get('trigramme_bas', '')
        trig_h_info = TRIGRAMMES.get(trig_haut, {})
        trig_b_info = TRIGRAMMES.get(trig_bas, {})
        
        st.markdown("#### ☯ Trigrammes")
        tcol1, tcol2 = st.columns(2)
        with tcol1:
            st.metric(f"{trig_h_info.get('symbole', '')} Supérieur", trig_haut, f"{trig_h_info.get('freq', 0)} Hz")
        with tcol2:
            st.metric(f"{trig_b_info.get('symbole', '')} Inférieur", trig_bas, f"{trig_b_info.get('freq', 0)} Hz")
    
    with col2:
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
        
        if hex_mute_numero:
            car_mut = hex_mute_data.get('caractere', '')
            st.markdown(f"""
            <div class="mutation-card">
                <div style="font-size: 0.85rem;">🔄 MUTATION VERS</div>
                <div style="font-size: 2.5rem;">{car_mut}</div>
                <div style="font-weight: bold;">{hex_mute_numero}. {hex_mute_data.get('nom_pinyin', '')}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Textes
    st.markdown("### 📜 Textes Traditionnels")
    desc = hex_data.get('description', '')
    if desc:
        with st.expander("📖 Description", expanded=True):
            st.write(desc)
    
    jugement = hex_data.get('jugement_texte', '')
    if jugement:
        st.info(f"**⚖️ Le Jugement**\n\n{jugement}")
    
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
    
    st.divider()
    
    # ===== EXPORTS =====
    st.markdown("### 📦 Exports")
    
    exp_col1, exp_col2 = st.columns(2)
    
    with exp_col1:
        st.markdown("#### 🎵 Audio Tirage")
        if st.button("🔊 Générer audio"):
            with st.spinner("Génération..."):
                audio_data = generate_audio_sequence(traits)
                audio_b64 = audio_to_base64(audio_data)
                st.audio(f"data:audio/wav;base64,{audio_b64}", format="audio/wav")
                audio_buffer = BytesIO()
                wavfile.write(audio_buffer, 44100, audio_data)
                st.download_button("📥 WAV", audio_buffer.getvalue(), f"yijing-audio-hex{hex_numero}.wav", "audio/wav")
    
    with exp_col2:
        st.markdown("#### 📄 Rapport PDF")
        if st.button("📄 Générer PDF"):
            with st.spinner("Génération..."):
                grille = generer_grille(traits, images_path, mutation=False) if images_path.exists() else None
                pdf_data = generate_pdf_report(traits, st.session_state.question, hex_data, hex_mute_data, grille)
                st.download_button("📥 PDF", pdf_data, f"yijing-rapport-hex{hex_numero}.pdf", "application/pdf")
    
    st.divider()
    
    # ===== MÉDITATION KASINA KBS =====
    st.markdown("### 🧘 Méditation Kasina / Mindplace (5 min)")
    
    st.markdown("""
    <div class="kasina-box">
        <strong>🧠 Session AVS (Audio-Visual Stimulation)</strong><br>
        Génère une méditation de 5 minutes au format <strong>KBS</strong> (Kasina Basic Session) 
        compatible <strong>Mindplace Kasina</strong> et <strong>Limina</strong>.<br><br>
        <em>Utilise l'entrainement par réponse de fréquence (FFR) avec battements binauraux 
        et stimulation lumineuse pour guider le cerveau vers des états Alpha/Theta.</em>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🧘 Générer Session Kasina KBS", type="primary", use_container_width=True):
        with st.spinner("Génération de la session Kasina..."):
            kbs_content, segments = generate_kbs_session(hex_data)
            kasina_audio = generate_kasina_binaural_audio(segments)
            
            st.success("✅ Session Kasina générée!")
            
            # Afficher les phases
            st.markdown("**📊 Structure de la méditation :**")
            
            total_time = 0
            for i, seg in enumerate(segments):
                r, g, b = seg['Red'], seg['Green'], seg['Blue']
                # Convertir 0-100% en 0-255 pour affichage
                color_hex = f"#{int(r*2.55):02X}{int(g*2.55):02X}{int(b*2.55):02X}"
                beat = seg['Beat']
                binaural = seg['RPtch'] - seg['LPtch']
                duration = seg['Time']
                
                # Déterminer l'état cérébral
                if beat >= 8:
                    state = "Alpha"
                    state_color = "#2196F3"
                elif beat >= 4:
                    state = "Theta"
                    state_color = "#9C27B0"
                else:
                    state = "Delta"
                    state_color = "#673AB7"
                
                st.markdown(f"""
                <div class="phase-item">
                    <div class="phase-color" style="background: {color_hex};"></div>
                    <div style="flex: 1;">
                        <strong>{seg['name']}</strong><br>
                        <small style="color: #666;">
                            ⏱ {duration:.0f}s | 
                            💡 <span style="color: {state_color}; font-weight: bold;">{beat:.1f} Hz ({state})</span> | 
                            🎧 {seg['LPtch']:.0f}/{seg['RPtch']:.0f} Hz (Δ{binaural:.0f} Hz binaural)
                        </small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                total_time += duration
            
            st.markdown(f"**⏱ Durée totale: {total_time/60:.1f} minutes**")
            
            # Téléchargements
            st.markdown("---")
            st.markdown("##### 📥 Fichiers Kasina")
            
            kcol1, kcol2 = st.columns(2)
            
            with kcol1:
                st.download_button(
                    "📋 Session KBS (.kbs)",
                    kbs_content,
                    f"yijing-hex{hex_numero}.kbs",
                    "text/plain",
                    help="Format natif Mindplace - Copier sur carte SD du Kasina"
                )
            
            with kcol2:
                audio_buffer = BytesIO()
                wavfile.write(audio_buffer, 44100, kasina_audio)
                st.download_button(
                    "🎧 Audio Binaural (WAV)",
                    audio_buffer.getvalue(),
                    f"yijing-kasina-hex{hex_numero}.wav",
                    "audio/wav",
                    help="Audio stéréo - Casque REQUIS pour effet binaural"
                )
            
            # Aperçu audio
            st.markdown("**🔊 Aperçu audio (casque recommandé) :**")
            audio_b64 = audio_to_base64(kasina_audio)
            st.audio(f"data:audio/wav;base64,{audio_b64}", format="audio/wav")
            
            # Info technique
            with st.expander("ℹ️ Informations techniques KBS"):
                st.markdown(f"""
                **Paramètres KBS utilisés :**
                
                | Paramètre | Valeur | Description |
                |-----------|--------|-------------|
                | ColorControlMode | 3 | Couleurs RGB personnalisées |
                | SAMDpth | 0 | Binaural pur (pas d'isochronique) |
                | LgtModWF | Sine | Onde sinusoïdale (relaxation) |
                | LPhse/SPhse | 50% | Alternance équilibrée G/D |
                
                **Trigrammes utilisés :**
                - **Bas**: {hex_data.get('trigramme_bas', 'N/A')} ({TRIGRAMMES.get(hex_data.get('trigramme_bas', ''), {}).get('freq', 0)} Hz)
                - **Haut**: {hex_data.get('trigramme_haut', 'N/A')} ({TRIGRAMMES.get(hex_data.get('trigramme_haut', ''), {}).get('freq', 0)} Hz)
                
                **Utilisation :**
                1. Copier le fichier `.kbs` sur la carte SD du Kasina
                2. Naviguer vers "User Sessions"
                3. Sélectionner la session Yi Jing
                4. S'installer confortablement, yeux fermés
                """)

else:
    # Page d'accueil
    st.markdown("""
    ### 🌟 Bienvenue dans l'Oracle du Yi Jing v2.1
    
    Le **Yi Jing** (易經), ou *Livre des Mutations*, est l'un des plus anciens textes 
    de sagesse chinoise. Cette version intègre la génération de sessions **AVS** 
    (Audio-Visual Stimulation) pour appareils **Mindplace Kasina/Limina**.
    """)
    
    with st.expander("🧘 Méditation Kasina / AVS Technology", expanded=True):
        st.markdown("""
        La technologie **AVS (Audio-Visual Stimulation)** utilise le principe de 
        **Frequency Following Response (FFR)** pour entrainer les ondes cérébrales 
        vers des états désirés.
        
        #### États cérébraux ciblés :
        
        | État | Fréquence | Effet |
        |------|-----------|-------|
        | **Alpha** | 8-13 Hz | Relaxation, visualisation, créativité |
        | **Theta** | 4-7 Hz | Méditation profonde, mémoire, insight |
        | **SMR** | 12-15 Hz | Focus calme, attention |
        
        #### Structure de la session Yi Jing (5 min) :
        
        1. **Ancrage Alpha** (1 min) - 432 Hz, relaxation initiale
        2. **Trigramme Bas** (1.5 min) - Theta 7 Hz, élément inférieur
        3. **Trigramme Haut** (1.5 min) - Theta 5 Hz, élément supérieur
        4. **Intégration** (1 min) - 528 Hz Alpha, retour conscient
        
        #### Format KBS (Kasina Basic Session) :
        
        Le fichier `.kbs` généré est compatible avec :
        - **Mindplace Kasina** (lunettes LED + casque)
        - **Mindplace Limina** (version portable)
        
        Les paramètres suivent la spécification officielle KBS v2.
        """)
    
    with st.expander("🎵 Fréquences du Solfège Sacré"):
        for freq, desc in FREQ_SOLFEGGIO.items():
            st.write(f"**{freq} Hz** : {desc}")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #9E9E9E; font-size: 0.85rem;">
    易經 Yi Jing Oracle v2.1 | Grilles : Anibal Edelbert Amiot | CyberMind.FR<br>
    Format KBS basé sur documentation Mindplace | AVS Technology<br>
    <em>Le changement est la seule constante de l'univers</em>
</div>
""", unsafe_allow_html=True)
