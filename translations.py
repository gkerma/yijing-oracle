# -*- coding: utf-8 -*-
"""
Traductions multilingues pour Yi Jing Oracle
"""

# Traductions des noms des 64 hexagrammes
HEX_NAMES = {
    1: {"fr": "Le Créateur", "en": "The Creative", "de": "Das Schöpferische", "es": "Lo Creativo", "zh": "创造"},
    2: {"fr": "Le Réceptif", "en": "The Receptive", "de": "Das Empfangende", "es": "Lo Receptivo", "zh": "接受"},
    3: {"fr": "La Difficulté Initiale", "en": "Difficulty at the Beginning", "de": "Die Anfangsschwierigkeit", "es": "La Dificultad Inicial", "zh": "初难"},
    4: {"fr": "La Folie Juvénile", "en": "Youthful Folly", "de": "Die Jugendtorheit", "es": "La Necedad Juvenil", "zh": "蒙昧"},
    5: {"fr": "L'Attente", "en": "Waiting", "de": "Das Warten", "es": "La Espera", "zh": "等待"},
    6: {"fr": "Le Conflit", "en": "Conflict", "de": "Der Streit", "es": "El Conflicto", "zh": "争讼"},
    7: {"fr": "L'Armée", "en": "The Army", "de": "Das Heer", "es": "El Ejército", "zh": "军队"},
    8: {"fr": "La Solidarité", "en": "Holding Together", "de": "Das Zusammenhalten", "es": "La Solidaridad", "zh": "团结"},
    9: {"fr": "Petit Apprivoisement", "en": "Small Taming", "de": "Des Kleinen Zähmungskraft", "es": "La Fuerza Domesticadora Pequeña", "zh": "小蓄"},
    10: {"fr": "La Marche", "en": "Treading", "de": "Das Auftreten", "es": "El Porte", "zh": "践行"},
    11: {"fr": "La Paix", "en": "Peace", "de": "Der Friede", "es": "La Paz", "zh": "和平"},
    12: {"fr": "La Stagnation", "en": "Standstill", "de": "Die Stockung", "es": "El Estancamiento", "zh": "闭塞"},
    13: {"fr": "La Communauté", "en": "Fellowship", "de": "Gemeinschaft mit Menschen", "es": "La Comunidad", "zh": "同人"},
    14: {"fr": "Le Grand Avoir", "en": "Great Possession", "de": "Der Besitz von Großem", "es": "La Gran Posesión", "zh": "大有"},
    15: {"fr": "L'Humilité", "en": "Modesty", "de": "Die Bescheidenheit", "es": "La Modestia", "zh": "谦逊"},
    16: {"fr": "L'Enthousiasme", "en": "Enthusiasm", "de": "Die Begeisterung", "es": "El Entusiasmo", "zh": "愉悦"},
    17: {"fr": "La Suite", "en": "Following", "de": "Die Nachfolge", "es": "El Seguimiento", "zh": "随从"},
    18: {"fr": "Le Travail sur le Corrompu", "en": "Work on the Decayed", "de": "Die Arbeit am Verdorbenen", "es": "El Trabajo en lo Echado a Perder", "zh": "蛊惑"},
    19: {"fr": "L'Approche", "en": "Approach", "de": "Die Annäherung", "es": "El Acercamiento", "zh": "临近"},
    20: {"fr": "La Contemplation", "en": "Contemplation", "de": "Die Betrachtung", "es": "La Contemplación", "zh": "观察"},
    21: {"fr": "Mordre au Travers", "en": "Biting Through", "de": "Das Durchbeißen", "es": "La Mordedura Tajante", "zh": "噬嗑"},
    22: {"fr": "La Grâce", "en": "Grace", "de": "Die Anmut", "es": "La Gracia", "zh": "文饰"},
    23: {"fr": "L'Éclatement", "en": "Splitting Apart", "de": "Die Zersplitterung", "es": "La Desintegración", "zh": "剥落"},
    24: {"fr": "Le Retour", "en": "Return", "de": "Die Wiederkehr", "es": "El Retorno", "zh": "复归"},
    25: {"fr": "L'Innocence", "en": "Innocence", "de": "Die Unschuld", "es": "La Inocencia", "zh": "无妄"},
    26: {"fr": "Grand Apprivoisement", "en": "Great Taming", "de": "Des Großen Zähmungskraft", "es": "La Gran Fuerza Domesticadora", "zh": "大蓄"},
    27: {"fr": "La Nourriture", "en": "Nourishment", "de": "Die Ernährung", "es": "Las Comisuras de la Boca", "zh": "颐养"},
    28: {"fr": "La Prépondérance du Grand", "en": "Great Excess", "de": "Des Großen Übergewicht", "es": "La Preponderancia de lo Grande", "zh": "大过"},
    29: {"fr": "L'Insondable", "en": "The Abysmal", "de": "Das Abgründige", "es": "Lo Abismal", "zh": "坎险"},
    30: {"fr": "Ce qui s'Attache", "en": "The Clinging", "de": "Das Haftende", "es": "Lo Adherente", "zh": "附丽"},
    31: {"fr": "L'Influence", "en": "Influence", "de": "Die Einwirkung", "es": "El Influjo", "zh": "感应"},
    32: {"fr": "La Durée", "en": "Duration", "de": "Die Dauer", "es": "La Duración", "zh": "恒久"},
    33: {"fr": "La Retraite", "en": "Retreat", "de": "Der Rückzug", "es": "La Retirada", "zh": "遁逃"},
    34: {"fr": "La Puissance du Grand", "en": "Great Power", "de": "Des Großen Macht", "es": "El Poder de lo Grande", "zh": "大壮"},
    35: {"fr": "Le Progrès", "en": "Progress", "de": "Der Fortschritt", "es": "El Progreso", "zh": "进步"},
    36: {"fr": "L'Obscurcissement de la Lumière", "en": "Darkening of the Light", "de": "Die Verfinsterung des Lichts", "es": "El Oscurecimiento de la Luz", "zh": "明夷"},
    37: {"fr": "La Famille", "en": "The Family", "de": "Die Sippe", "es": "La Familia", "zh": "家人"},
    38: {"fr": "L'Opposition", "en": "Opposition", "de": "Der Gegensatz", "es": "El Antagonismo", "zh": "睽违"},
    39: {"fr": "L'Obstacle", "en": "Obstruction", "de": "Die Hemmung", "es": "El Impedimento", "zh": "蹇难"},
    40: {"fr": "La Libération", "en": "Deliverance", "de": "Die Befreiung", "es": "La Liberación", "zh": "解脱"},
    41: {"fr": "La Diminution", "en": "Decrease", "de": "Die Minderung", "es": "La Merma", "zh": "损减"},
    42: {"fr": "L'Augmentation", "en": "Increase", "de": "Die Mehrung", "es": "El Aumento", "zh": "增益"},
    43: {"fr": "La Percée", "en": "Breakthrough", "de": "Der Durchbruch", "es": "La Resolución", "zh": "决断"},
    44: {"fr": "Venir à la Rencontre", "en": "Coming to Meet", "de": "Das Entgegenkommen", "es": "Ir al Encuentro", "zh": "相遇"},
    45: {"fr": "Le Rassemblement", "en": "Gathering Together", "de": "Die Sammlung", "es": "La Reunión", "zh": "聚集"},
    46: {"fr": "La Poussée vers le Haut", "en": "Pushing Upward", "de": "Das Empordringen", "es": "La Subida", "zh": "上升"},
    47: {"fr": "L'Accablement", "en": "Oppression", "de": "Die Bedrängnis", "es": "El Agotamiento", "zh": "困顿"},
    48: {"fr": "Le Puits", "en": "The Well", "de": "Der Brunnen", "es": "El Pozo", "zh": "井泉"},
    49: {"fr": "La Révolution", "en": "Revolution", "de": "Die Umwälzung", "es": "La Revolución", "zh": "变革"},
    50: {"fr": "Le Chaudron", "en": "The Cauldron", "de": "Der Tiegel", "es": "El Caldero", "zh": "鼎器"},
    51: {"fr": "L'Éveilleur", "en": "The Arousing", "de": "Das Erregende", "es": "Lo Suscitativo", "zh": "震动"},
    52: {"fr": "L'Immobilisation", "en": "Keeping Still", "de": "Das Stillehalten", "es": "El Aquietamiento", "zh": "止静"},
    53: {"fr": "Le Développement", "en": "Development", "de": "Die Entwicklung", "es": "La Evolución", "zh": "渐进"},
    54: {"fr": "L'Épousée", "en": "The Marrying Maiden", "de": "Das heiratende Mädchen", "es": "La Desposada", "zh": "归妹"},
    55: {"fr": "L'Abondance", "en": "Abundance", "de": "Die Fülle", "es": "La Plenitud", "zh": "丰盛"},
    56: {"fr": "Le Voyageur", "en": "The Wanderer", "de": "Der Wanderer", "es": "El Viajero", "zh": "旅行"},
    57: {"fr": "Le Doux", "en": "The Gentle", "de": "Das Sanfte", "es": "Lo Suave", "zh": "顺从"},
    58: {"fr": "Le Serein", "en": "The Joyous", "de": "Das Heitere", "es": "Lo Sereno", "zh": "喜悦"},
    59: {"fr": "La Dissolution", "en": "Dispersion", "de": "Die Auflösung", "es": "La Disolución", "zh": "涣散"},
    60: {"fr": "La Limitation", "en": "Limitation", "de": "Die Beschränkung", "es": "La Restricción", "zh": "节制"},
    61: {"fr": "La Vérité Intérieure", "en": "Inner Truth", "de": "Innere Wahrheit", "es": "La Verdad Interior", "zh": "中孚"},
    62: {"fr": "Prépondérance du Petit", "en": "Small Excess", "de": "Des Kleinen Übergewicht", "es": "La Preponderancia de lo Pequeño", "zh": "小过"},
    63: {"fr": "Après l'Accomplissement", "en": "After Completion", "de": "Nach der Vollendung", "es": "Después de la Consumación", "zh": "既济"},
    64: {"fr": "Avant l'Accomplissement", "en": "Before Completion", "de": "Vor der Vollendung", "es": "Antes de la Consumación", "zh": "未济"},
}

# Traductions des trigrammes
TRIGRAM_NAMES = {
    "K'ien": {"fr": "Le Créateur, le Ciel", "en": "The Creative, Heaven", "de": "Das Schöpferische, der Himmel", "es": "Lo Creativo, el Cielo", "zh": "乾 - 天"},
    "K'ouen": {"fr": "Le Réceptif, la Terre", "en": "The Receptive, Earth", "de": "Das Empfangende, die Erde", "es": "Lo Receptivo, la Tierra", "zh": "坤 - 地"},
    "Tchen": {"fr": "L'Éveilleur, le Tonnerre", "en": "The Arousing, Thunder", "de": "Das Erregende, der Donner", "es": "Lo Suscitativo, el Trueno", "zh": "震 - 雷"},
    "K'an": {"fr": "L'Insondable, l'Eau", "en": "The Abysmal, Water", "de": "Das Abgründige, das Wasser", "es": "Lo Abismal, el Agua", "zh": "坎 - 水"},
    "Ken": {"fr": "L'Immobilisation, la Montagne", "en": "Keeping Still, Mountain", "de": "Das Stillehalten, der Berg", "es": "El Aquietamiento, la Montaña", "zh": "艮 - 山"},
    "Souen": {"fr": "Le Doux, le Vent", "en": "The Gentle, Wind", "de": "Das Sanfte, der Wind", "es": "Lo Suave, el Viento", "zh": "巽 - 风"},
    "Li": {"fr": "Ce qui s'Attache, le Feu", "en": "The Clinging, Fire", "de": "Das Haftende, das Feuer", "es": "Lo Adherente, el Fuego", "zh": "离 - 火"},
    "Touei": {"fr": "Le Joyeux, le Lac", "en": "The Joyous, Lake", "de": "Das Heitere, der See", "es": "Lo Sereno, el Lago", "zh": "兑 - 泽"},
}

def get_hex_name(numero: int, lang: str = "fr") -> str:
    """Retourne le nom traduit d'un hexagramme"""
    if numero in HEX_NAMES:
        return HEX_NAMES[numero].get(lang, HEX_NAMES[numero].get("fr", ""))
    return ""

def get_trigram_name(name: str, lang: str = "fr") -> str:
    """Retourne le nom traduit d'un trigramme"""
    if name in TRIGRAM_NAMES:
        return TRIGRAM_NAMES[name].get(lang, TRIGRAM_NAMES[name].get("fr", ""))
    return name

TRANSLATIONS = {
    "fr": {
        # Général
        "app_title": "☯ Yi Jing Oracle",
        "app_subtitle": "Consultation du Livre des Transformations",
        "version": "Version 2.2 Multilingue",
        "language": "Langue",
        
        # Sidebar
        "sidebar_title": "🎴 Nouvelle Consultation",
        "your_question": "Votre question (optionnel)",
        "question_placeholder": "Formulez votre question...",
        "throw_coins": "🪙 Lancer les pièces",
        "throwing": "Tirage en cours...",
        "new_reading": "🔄 Nouvelle consultation",
        
        # Diagnostic
        "diagnostic_title": "🔧 Diagnostic Police CJK",
        "images_brown": "Images (marron)",
        "images_purple": "Images (violet)",
        "reportlab_font": "Police ReportLab",
        "embedded_font": "Police embarquée",
        "size": "Taille",
        "not_available": "non disponible",
        "folder_missing": "Dossier manquant",
        
        # Résultats
        "result_title": "📖 Résultat de votre consultation",
        "hexagram": "Hexagramme",
        "upper_trigram": "Trigramme Supérieur",
        "lower_trigram": "Trigramme Inférieur",
        "nature": "Nature",
        "traits_frequencies": "Traits tirés et fréquences",
        "trait": "Trait",
        "stable": "stable",
        "mutant": "mutant",
        "mutant_arrow": "← MUTANT",
        
        # Types de traits
        "yang_stable": "Yang stable",
        "yang_mutant": "Yang mutant",
        "yin_stable": "Yin stable",
        "yin_mutant": "Yin mutant",
        
        # Grille
        "hermes_grid": "Grille La Livrée d'Hermès",
        "grid_after_mutation": "Grille après mutation",
        
        # Textes traditionnels
        "judgment": "Le Jugement",
        "image": "L'Image",
        "judgment_not_available": "Texte du Jugement non disponible dans la base de données.",
        "image_not_available": "Texte de l'Image non disponible dans la base de données.",
        "consult_complete": "Consultez une édition complète du Yi Jing pour ce texte.",
        
        # Interprétation
        "interpretation_title": "Interprétation Générale",
        "hexagram_obtained": "Hexagramme obtenu",
        "combination": "Combinaison",
        "on": "sur",
        "mutant_traits_detected": "trait(s) mutant(s) détecté(s) - Situation en transformation",
        "evolves_to": "L'hexagramme évolue vers le n°",
        "read_mutant_traits": "Lisez attentivement les textes des traits mutants ci-après.",
        "no_mutant_stable": "Aucun trait mutant - Situation stable",
        "message_applies": "Le message de l'hexagramme s'applique tel quel.",
        
        # Traits
        "six_traits_of": "Les Six Traits de l'Hexagramme",
        "mutant_traits_title": "*** TRAITS MUTANTS - À lire attentivement",
        "mutant_traits_subtitle": "Ces {n} trait(s) indiquent les aspects de la situation en transformation",
        "trait_mutant": "TRAIT {n} MUTANT",
        "yin_to_yang": "Yin → Yang",
        "yang_to_yin": "Yang → Yin",
        
        # Mutation
        "mutation_to": "MUTATION VERS HEXAGRAMME",
        
        # PDF
        "pdf_title": "Rapport de Consultation Détaillé",
        "download_pdf": "📥 Télécharger le rapport PDF",
        "pdf_filename": "yijing-rapport-complet",
        "traditional_texts": "Textes Traditionnels",
        "general_interpretation": "INTERPRÉTATION GÉNÉRALE",
        "page": "Page",
        "grids_credit": "Grilles: Anibal Edelbert Amiot",
        
        # Audio
        "sacred_frequencies": "🎵 Fréquences Sacrées",
        "listen_frequencies": "Écouter les fréquences de l'hexagramme",
        "download_audio": "📥 Télécharger l'audio WAV",
        "audio_filename": "yijing-frequences",
        
        # Kasina
        "kasina_title": "🧘 Méditation Kasina",
        "kasina_subtitle": "Séquence de méditation avec fréquences cérébrales",
        "download_kasina": "📥 Télécharger la séquence KBS",
        "kasina_filename": "yijing-kasina",
        
        # Footer
        "footer_credit": "CyberMind.FR",
    },
    
    "en": {
        # General
        "app_title": "☯ Yi Jing Oracle",
        "app_subtitle": "Consulting the Book of Changes",
        "version": "Version 2.2 Multilingual",
        "language": "Language",
        
        # Sidebar
        "sidebar_title": "🎴 New Consultation",
        "your_question": "Your question (optional)",
        "question_placeholder": "Formulate your question...",
        "throw_coins": "🪙 Throw the coins",
        "throwing": "Casting in progress...",
        "new_reading": "🔄 New consultation",
        
        # Diagnostic
        "diagnostic_title": "🔧 CJK Font Diagnostic",
        "images_brown": "Images (brown)",
        "images_purple": "Images (purple)",
        "reportlab_font": "ReportLab Font",
        "embedded_font": "Embedded font",
        "size": "Size",
        "not_available": "not available",
        "folder_missing": "Folder missing",
        
        # Results
        "result_title": "📖 Your Consultation Result",
        "hexagram": "Hexagram",
        "upper_trigram": "Upper Trigram",
        "lower_trigram": "Lower Trigram",
        "nature": "Nature",
        "traits_frequencies": "Lines drawn and frequencies",
        "trait": "Line",
        "stable": "stable",
        "mutant": "changing",
        "mutant_arrow": "← CHANGING",
        
        # Line types
        "yang_stable": "Yang stable",
        "yang_mutant": "Yang changing",
        "yin_stable": "Yin stable",
        "yin_mutant": "Yin changing",
        
        # Grid
        "hermes_grid": "La Livrée d'Hermès Grid",
        "grid_after_mutation": "Grid after mutation",
        
        # Traditional texts
        "judgment": "The Judgment",
        "image": "The Image",
        "judgment_not_available": "Judgment text not available in the database.",
        "image_not_available": "Image text not available in the database.",
        "consult_complete": "Please consult a complete edition of the Yi Jing for this text.",
        
        # Interpretation
        "interpretation_title": "General Interpretation",
        "hexagram_obtained": "Hexagram obtained",
        "combination": "Combination",
        "on": "over",
        "mutant_traits_detected": "changing line(s) detected - Situation in transformation",
        "evolves_to": "The hexagram evolves to #",
        "read_mutant_traits": "Read carefully the texts of the changing lines below.",
        "no_mutant_stable": "No changing lines - Stable situation",
        "message_applies": "The hexagram message applies as is.",
        
        # Lines
        "six_traits_of": "The Six Lines of Hexagram",
        "mutant_traits_title": "*** CHANGING LINES - Read carefully",
        "mutant_traits_subtitle": "These {n} line(s) indicate the aspects of the situation in transformation",
        "trait_mutant": "LINE {n} CHANGING",
        "yin_to_yang": "Yin → Yang",
        "yang_to_yin": "Yang → Yin",
        
        # Mutation
        "mutation_to": "MUTATION TO HEXAGRAM",
        
        # PDF
        "pdf_title": "Detailed Consultation Report",
        "download_pdf": "📥 Download PDF report",
        "pdf_filename": "yijing-complete-report",
        "traditional_texts": "Traditional Texts",
        "general_interpretation": "GENERAL INTERPRETATION",
        "page": "Page",
        "grids_credit": "Grids: Anibal Edelbert Amiot",
        
        # Audio
        "sacred_frequencies": "🎵 Sacred Frequencies",
        "listen_frequencies": "Listen to the hexagram frequencies",
        "download_audio": "📥 Download WAV audio",
        "audio_filename": "yijing-frequencies",
        
        # Kasina
        "kasina_title": "🧘 Kasina Meditation",
        "kasina_subtitle": "Meditation sequence with brainwave frequencies",
        "download_kasina": "📥 Download KBS sequence",
        "kasina_filename": "yijing-kasina",
        
        # Footer
        "footer_credit": "CyberMind.FR",
    },
    
    "de": {
        # Allgemein
        "app_title": "☯ Yi Jing Orakel",
        "app_subtitle": "Befragung des Buches der Wandlungen",
        "version": "Version 2.2 Mehrsprachig",
        "language": "Sprache",
        
        # Seitenleiste
        "sidebar_title": "🎴 Neue Befragung",
        "your_question": "Ihre Frage (optional)",
        "question_placeholder": "Formulieren Sie Ihre Frage...",
        "throw_coins": "🪙 Münzen werfen",
        "throwing": "Wurf läuft...",
        "new_reading": "🔄 Neue Befragung",
        
        # Diagnose
        "diagnostic_title": "🔧 CJK-Schrift Diagnose",
        "images_brown": "Bilder (braun)",
        "images_purple": "Bilder (lila)",
        "reportlab_font": "ReportLab Schrift",
        "embedded_font": "Eingebettete Schrift",
        "size": "Größe",
        "not_available": "nicht verfügbar",
        "folder_missing": "Ordner fehlt",
        
        # Ergebnisse
        "result_title": "📖 Ihr Befragungsergebnis",
        "hexagram": "Hexagramm",
        "upper_trigram": "Oberes Trigramm",
        "lower_trigram": "Unteres Trigramm",
        "nature": "Natur",
        "traits_frequencies": "Gezogene Linien und Frequenzen",
        "trait": "Linie",
        "stable": "stabil",
        "mutant": "wandelnd",
        "mutant_arrow": "← WANDELND",
        
        # Linientypen
        "yang_stable": "Yang stabil",
        "yang_mutant": "Yang wandelnd",
        "yin_stable": "Yin stabil",
        "yin_mutant": "Yin wandelnd",
        
        # Gitter
        "hermes_grid": "La Livrée d'Hermès Gitter",
        "grid_after_mutation": "Gitter nach Wandlung",
        
        # Traditionelle Texte
        "judgment": "Das Urteil",
        "image": "Das Bild",
        "judgment_not_available": "Urteilstext nicht in der Datenbank verfügbar.",
        "image_not_available": "Bildtext nicht in der Datenbank verfügbar.",
        "consult_complete": "Konsultieren Sie eine vollständige Ausgabe des Yi Jing für diesen Text.",
        
        # Interpretation
        "interpretation_title": "Allgemeine Interpretation",
        "hexagram_obtained": "Erhaltenes Hexagramm",
        "combination": "Kombination",
        "on": "über",
        "mutant_traits_detected": "wandelnde Linie(n) erkannt - Situation im Wandel",
        "evolves_to": "Das Hexagramm entwickelt sich zu Nr.",
        "read_mutant_traits": "Lesen Sie die Texte der wandelnden Linien sorgfältig.",
        "no_mutant_stable": "Keine wandelnden Linien - Stabile Situation",
        "message_applies": "Die Botschaft des Hexagramms gilt unverändert.",
        
        # Linien
        "six_traits_of": "Die sechs Linien des Hexagramms",
        "mutant_traits_title": "*** WANDELNDE LINIEN - Sorgfältig lesen",
        "mutant_traits_subtitle": "Diese {n} Linie(n) zeigen die Aspekte der Situation im Wandel",
        "trait_mutant": "LINIE {n} WANDELND",
        "yin_to_yang": "Yin → Yang",
        "yang_to_yin": "Yang → Yin",
        
        # Wandlung
        "mutation_to": "WANDLUNG ZU HEXAGRAMM",
        
        # PDF
        "pdf_title": "Detaillierter Befragungsbericht",
        "download_pdf": "📥 PDF-Bericht herunterladen",
        "pdf_filename": "yijing-vollstaendiger-bericht",
        "traditional_texts": "Traditionelle Texte",
        "general_interpretation": "ALLGEMEINE INTERPRETATION",
        "page": "Seite",
        "grids_credit": "Gitter: Anibal Edelbert Amiot",
        
        # Audio
        "sacred_frequencies": "🎵 Heilige Frequenzen",
        "listen_frequencies": "Hexagramm-Frequenzen anhören",
        "download_audio": "📥 WAV-Audio herunterladen",
        "audio_filename": "yijing-frequenzen",
        
        # Kasina
        "kasina_title": "🧘 Kasina Meditation",
        "kasina_subtitle": "Meditationssequenz mit Gehirnwellenfrequenzen",
        "download_kasina": "📥 KBS-Sequenz herunterladen",
        "kasina_filename": "yijing-kasina",
        
        # Fußzeile
        "footer_credit": "CyberMind.FR",
    },
    
    "es": {
        # General
        "app_title": "☯ Oráculo Yi Jing",
        "app_subtitle": "Consultando el Libro de los Cambios",
        "version": "Versión 2.2 Multilingüe",
        "language": "Idioma",
        
        # Barra lateral
        "sidebar_title": "🎴 Nueva Consulta",
        "your_question": "Su pregunta (opcional)",
        "question_placeholder": "Formule su pregunta...",
        "throw_coins": "🪙 Lanzar las monedas",
        "throwing": "Lanzamiento en curso...",
        "new_reading": "🔄 Nueva consulta",
        
        # Diagnóstico
        "diagnostic_title": "🔧 Diagnóstico de Fuente CJK",
        "images_brown": "Imágenes (marrón)",
        "images_purple": "Imágenes (púrpura)",
        "reportlab_font": "Fuente ReportLab",
        "embedded_font": "Fuente incorporada",
        "size": "Tamaño",
        "not_available": "no disponible",
        "folder_missing": "Carpeta faltante",
        
        # Resultados
        "result_title": "📖 Resultado de su Consulta",
        "hexagram": "Hexagrama",
        "upper_trigram": "Trigrama Superior",
        "lower_trigram": "Trigrama Inferior",
        "nature": "Naturaleza",
        "traits_frequencies": "Líneas obtenidas y frecuencias",
        "trait": "Línea",
        "stable": "estable",
        "mutant": "mutante",
        "mutant_arrow": "← MUTANTE",
        
        # Tipos de líneas
        "yang_stable": "Yang estable",
        "yang_mutant": "Yang mutante",
        "yin_stable": "Yin estable",
        "yin_mutant": "Yin mutante",
        
        # Cuadrícula
        "hermes_grid": "Cuadrícula La Livrée d'Hermès",
        "grid_after_mutation": "Cuadrícula después de la mutación",
        
        # Textos tradicionales
        "judgment": "El Juicio",
        "image": "La Imagen",
        "judgment_not_available": "Texto del Juicio no disponible en la base de datos.",
        "image_not_available": "Texto de la Imagen no disponible en la base de datos.",
        "consult_complete": "Consulte una edición completa del Yi Jing para este texto.",
        
        # Interpretación
        "interpretation_title": "Interpretación General",
        "hexagram_obtained": "Hexagrama obtenido",
        "combination": "Combinación",
        "on": "sobre",
        "mutant_traits_detected": "línea(s) mutante(s) detectada(s) - Situación en transformación",
        "evolves_to": "El hexagrama evoluciona hacia el n°",
        "read_mutant_traits": "Lea atentamente los textos de las líneas mutantes a continuación.",
        "no_mutant_stable": "Sin líneas mutantes - Situación estable",
        "message_applies": "El mensaje del hexagrama se aplica tal cual.",
        
        # Líneas
        "six_traits_of": "Las Seis Líneas del Hexagrama",
        "mutant_traits_title": "*** LÍNEAS MUTANTES - Leer atentamente",
        "mutant_traits_subtitle": "Estas {n} línea(s) indican los aspectos de la situación en transformación",
        "trait_mutant": "LÍNEA {n} MUTANTE",
        "yin_to_yang": "Yin → Yang",
        "yang_to_yin": "Yang → Yin",
        
        # Mutación
        "mutation_to": "MUTACIÓN HACIA HEXAGRAMA",
        
        # PDF
        "pdf_title": "Informe de Consulta Detallado",
        "download_pdf": "📥 Descargar informe PDF",
        "pdf_filename": "yijing-informe-completo",
        "traditional_texts": "Textos Tradicionales",
        "general_interpretation": "INTERPRETACIÓN GENERAL",
        "page": "Página",
        "grids_credit": "Cuadrículas: Anibal Edelbert Amiot",
        
        # Audio
        "sacred_frequencies": "🎵 Frecuencias Sagradas",
        "listen_frequencies": "Escuchar las frecuencias del hexagrama",
        "download_audio": "📥 Descargar audio WAV",
        "audio_filename": "yijing-frecuencias",
        
        # Kasina
        "kasina_title": "🧘 Meditación Kasina",
        "kasina_subtitle": "Secuencia de meditación con frecuencias cerebrales",
        "download_kasina": "📥 Descargar secuencia KBS",
        "kasina_filename": "yijing-kasina",
        
        # Pie de página
        "footer_credit": "CyberMind.FR",
    },
    
    "zh": {
        # 通用
        "app_title": "☯ 易经神谕",
        "app_subtitle": "咨询变化之书",
        "version": "版本 2.2 多语言",
        "language": "语言",
        
        # 侧边栏
        "sidebar_title": "🎴 新的咨询",
        "your_question": "您的问题（可选）",
        "question_placeholder": "请提出您的问题...",
        "throw_coins": "🪙 投掷硬币",
        "throwing": "正在投掷...",
        "new_reading": "🔄 新的咨询",
        
        # 诊断
        "diagnostic_title": "🔧 中日韩字体诊断",
        "images_brown": "图像（棕色）",
        "images_purple": "图像（紫色）",
        "reportlab_font": "ReportLab 字体",
        "embedded_font": "嵌入字体",
        "size": "大小",
        "not_available": "不可用",
        "folder_missing": "文件夹缺失",
        
        # 结果
        "result_title": "📖 您的咨询结果",
        "hexagram": "卦",
        "upper_trigram": "上卦",
        "lower_trigram": "下卦",
        "nature": "性质",
        "traits_frequencies": "爻与频率",
        "trait": "爻",
        "stable": "静",
        "mutant": "动",
        "mutant_arrow": "← 动爻",
        
        # 爻类型
        "yang_stable": "老阳",
        "yang_mutant": "少阳",
        "yin_stable": "老阴",
        "yin_mutant": "少阴",
        
        # 方格
        "hermes_grid": "赫尔墨斯之书方格",
        "grid_after_mutation": "变卦后方格",
        
        # 传统文本
        "judgment": "卦辞",
        "image": "象辞",
        "judgment_not_available": "数据库中无卦辞文本。",
        "image_not_available": "数据库中无象辞文本。",
        "consult_complete": "请查阅易经完整版本以获取此文本。",
        
        # 解释
        "interpretation_title": "总体解释",
        "hexagram_obtained": "所得卦",
        "combination": "组合",
        "on": "于",
        "mutant_traits_detected": "个动爻 - 情况正在转变",
        "evolves_to": "此卦演变为第",
        "read_mutant_traits": "请仔细阅读以下动爻的文本。",
        "no_mutant_stable": "无动爻 - 稳定情况",
        "message_applies": "卦辞直接适用。",
        
        # 爻
        "six_traits_of": "卦的六爻",
        "mutant_traits_title": "*** 动爻 - 请仔细阅读",
        "mutant_traits_subtitle": "这{n}个爻表示情况转变的方面",
        "trait_mutant": "第{n}爻 动",
        "yin_to_yang": "阴 → 阳",
        "yang_to_yin": "阳 → 阴",
        
        # 变卦
        "mutation_to": "变为卦",
        
        # PDF
        "pdf_title": "详细咨询报告",
        "download_pdf": "📥 下载PDF报告",
        "pdf_filename": "yijing-完整报告",
        "traditional_texts": "传统文本",
        "general_interpretation": "总体解释",
        "page": "页",
        "grids_credit": "方格：Anibal Edelbert Amiot",
        
        # 音频
        "sacred_frequencies": "🎵 神圣频率",
        "listen_frequencies": "聆听卦的频率",
        "download_audio": "📥 下载WAV音频",
        "audio_filename": "yijing-频率",
        
        # Kasina
        "kasina_title": "🧘 遍处禅修",
        "kasina_subtitle": "脑波频率冥想序列",
        "download_kasina": "📥 下载KBS序列",
        "kasina_filename": "yijing-kasina",
        
        # 页脚
        "footer_credit": "CyberMind.FR",
    },
}

# Langues disponibles avec leurs noms
LANGUAGES = {
    "fr": "🇫🇷 Français",
    "en": "🇬🇧 English",
    "de": "🇩🇪 Deutsch",
    "es": "🇪🇸 Español",
    "zh": "🇨🇳 中文",
}

def get_text(key: str, lang: str = "fr", **kwargs) -> str:
    """
    Récupère un texte traduit.
    
    Args:
        key: Clé de traduction
        lang: Code de langue (fr, en, de, es, zh)
        **kwargs: Variables pour le formatage
    
    Returns:
        Texte traduit ou clé si non trouvée
    """
    if lang not in TRANSLATIONS:
        lang = "fr"
    
    text = TRANSLATIONS[lang].get(key, TRANSLATIONS["fr"].get(key, key))
    
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    
    return text

def t(key: str, lang: str = "fr", **kwargs) -> str:
    """Alias court pour get_text"""
    return get_text(key, lang, **kwargs)
