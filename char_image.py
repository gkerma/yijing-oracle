"""
Module pour générer des images de caractères chinois
Utilisé comme fallback quand la police CJK ne fonctionne pas dans le PDF
"""
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

# Variable globale pour stocker le chemin de la police
_FONT_PATH = None

def set_font_path(path):
    """Définit le chemin de la police à utiliser"""
    global _FONT_PATH
    _FONT_PATH = path

def get_cjk_font_for_pil():
    """Trouve une police CJK pour PIL"""
    global _FONT_PATH
    
    # Si un chemin a été défini explicitement, l'utiliser
    if _FONT_PATH and os.path.exists(_FONT_PATH):
        return _FONT_PATH
    
    # Sinon, chercher dans les emplacements standards
    font_paths = [
        # Police embarquée (relatif au script appelant)
        os.path.join(os.path.dirname(__file__), 'fonts', 'ipag.ttf'),
        # Linux
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf',
        '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
        # macOS
        '/System/Library/Fonts/PingFang.ttc',
        '/Library/Fonts/Arial Unicode.ttf',
        # Windows
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/simsun.ttc',
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            return path
    return None

def create_character_image(char, size=100, color='#2F4F4F', bg_color=None, font_path=None):
    """
    Crée une image PNG d'un caractère chinois
    
    Args:
        char: Le caractère à dessiner
        size: Taille de la police
        color: Couleur du texte (hex)
        bg_color: Couleur de fond (None = transparent)
        font_path: Chemin explicite vers la police (optionnel)
    
    Returns:
        BytesIO contenant l'image PNG, ou None si échec
    """
    # Utiliser le chemin explicite si fourni
    if font_path and os.path.exists(font_path):
        actual_font_path = font_path
    else:
        actual_font_path = get_cjk_font_for_pil()
    
    if not actual_font_path:
        return None
    
    try:
        # Créer la police
        font = ImageFont.truetype(actual_font_path, size)
        
        # Calculer la taille du texte
        bbox = font.getbbox(char)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Ajouter un peu de marge
        img_width = text_width + 20
        img_height = text_height + 20
        
        # Créer l'image
        if bg_color:
            img = Image.new('RGBA', (img_width, img_height), bg_color)
        else:
            img = Image.new('RGBA', (img_width, img_height), (255, 255, 255, 0))
        
        draw = ImageDraw.Draw(img)
        
        # Convertir la couleur hex en RGB
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            color_rgb = (r, g, b)
        else:
            color_rgb = (47, 79, 79)  # Défaut gris foncé
        
        # Dessiner le caractère centré
        x = (img_width - text_width) // 2 - bbox[0]
        y = (img_height - text_height) // 2 - bbox[1]
        draw.text((x, y), char, font=font, fill=color_rgb)
        
        # Sauvegarder en PNG
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer
        
    except Exception as e:
        print(f"Erreur création image caractère: {e}")
        return None

def test_character_image():
    """Test la génération d'image"""
    chars = ['乾', '坤', '比', '師']
    for char in chars:
        img = create_character_image(char, size=80)
        if img:
            print(f"✓ {char} OK")
        else:
            print(f"✗ {char} ÉCHEC")

if __name__ == "__main__":
    test_character_image()
