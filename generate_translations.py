# -*- coding: utf-8 -*-
"""
Générateur de fichiers JSON multilingues pour Yi Jing Oracle
Basé sur les traductions classiques (Wilhelm/Baynes pour EN, Wilhelm pour DE)
"""

import json
import copy

# Charger le JSON français original
with open('yijing_complet.json', 'r', encoding='utf-8') as f:
    DATA_FR = json.load(f)

# =============================================================================
# TRADUCTIONS DES 64 HEXAGRAMMES
# =============================================================================

HEXAGRAMS = {
    1: {
        "en": {
            "nom": "The Creative",
            "jugement": "THE CREATIVE works sublime success, furthering through perseverance.\n\nThe movement of heaven is full of power. Thus the superior man makes himself strong and untiring.\n\nThe hexagram is consistently strong in character. Since there is no weakness in it, it is intrinsically powerful. Its image is heaven. Power is represented as unrestricted by any fixed conditions in space and is therefore conceived of as motion. Time is the basis of this motion.",
            "image": "The movement of heaven is full of power.\nThus the superior man makes himself strong and untiring.\n\nThe duration of time is the image of the power inherent in the Creative. The wise man draws from it the model according to which he develops his qualities, making them durable. He conscientiously removes all that is inferior, all that is vulgar. Thus he becomes untiring through a voluntary limitation of his field of activity."
        },
        "de": {
            "nom": "Das Schöpferische",
            "jugement": "DAS SCHÖPFERISCHE wirkt erhabenes Gelingen, fördernd durch Beharrlichkeit.\n\nDes Himmels Bewegung ist kraftvoll. So macht der Edle sich stark und unermüdlich.\n\nDas Zeichen ist durchaus stark von Natur. Da keine Schwäche daran ist, hat es als Eigenschaft die Stärke. Sein Bild ist der Himmel. Die Kraft ist dargestellt als nicht an bestimmte räumliche Bedingungen gebunden, daher wird sie als Bewegung aufgefasst. Die Zeit ist die Grundlage dieser Bewegung.",
            "image": "Des Himmels Bewegung ist kraftvoll.\nSo macht der Edle sich stark und unermüdlich.\n\nDie Zeitdauer ist das Bild der dem Schöpferischen eigentümlichen Kraft. Der Weise zieht daraus das Vorbild, nach dem er seine Eigenschaften entwickelt, um sie dauernd zu machen. Er entfernt gewissenhaft alles Geringe, alles Gemeine. So wird er unermüdlich durch freiwillige Einschränkung seines Wirkungskreises."
        },
        "es": {
            "nom": "Lo Creativo",
            "jugement": "LO CREATIVO obra un éxito sublime, favoreciendo por la perseverancia.\n\nEl movimiento del cielo es poderoso. Así el hombre noble se hace fuerte e incansable.\n\nEl hexagrama es uniformemente fuerte por naturaleza. Puesto que ninguna debilidad le es propia, tiene como cualidad la fuerza. Su imagen es el cielo. La fuerza está representada como no ligada a condiciones espaciales determinadas: se concibe por lo tanto como movimiento. El tiempo es el fundamento de este movimiento.",
            "image": "El movimiento del cielo es poderoso.\nAsí el hombre noble se hace fuerte e incansable.\n\nLa duración en el tiempo es la imagen de la fuerza propia de Lo Creativo. El sabio extrae de ella el modelo según el cual desarrolla sus cualidades, de modo a hacerlas duraderas. Elimina conscientemente todo lo inferior, todo lo vulgar. Así se vuelve incansable gracias a una limitación voluntaria de su campo de actividad."
        },
        "zh": {
            "nom": "创造",
            "jugement": "乾：元亨利贞。\n\n天行健，君子以自强不息。\n\n此卦纯阳刚健。因无柔弱之处，故其特性为刚强。其象为天。力量不受空间条件限制，故以运动表示。时间是运动的基础。",
            "image": "天行健，君子以自强不息。\n\n时间的持续是乾卦力量的象征。智者从中汲取榜样，发展自己的品德，使之持久。他自觉地去除一切卑下、庸俗之物。因此，通过自愿限制活动范围而变得不知疲倦。"
        }
    },
    2: {
        "en": {
            "nom": "The Receptive",
            "jugement": "THE RECEPTIVE brings about sublime success, furthering through the perseverance of a mare. If the superior man undertakes something and tries to lead, he goes astray; but if he follows, he finds guidance.\n\nThe earth's condition is receptive devotion. Thus the superior man who has breadth of character carries the outer world.",
            "image": "The earth's condition is receptive devotion.\nThus the superior man who has breadth of character carries the outer world.\n\nJust as there is only one heaven, so too there is only one earth. But while in the case of heaven the doubling of the trigram means duration in time, in the case of the earth it connotes the solidity and extension in space by virtue of which the earth is able to carry and preserve all things that live and move upon it."
        },
        "de": {
            "nom": "Das Empfangende",
            "jugement": "DAS EMPFANGENDE wirkt erhabenes Gelingen, fördernd durch die Beharrlichkeit einer Stute. Wenn der Edle etwas unternimmt und führen will, verirrt er sich; folgt er aber, so findet er Leitung.\n\nDer Erde Zustand ist hingebende Empfänglichkeit. So trägt der Edle mit weitem Charakter die Außenwelt.",
            "image": "Der Erde Zustand ist hingebende Empfänglichkeit.\nSo trägt der Edle mit weitem Charakter die Außenwelt.\n\nWie es nur einen Himmel gibt, gibt es auch nur eine Erde. Während aber beim Himmel die Verdoppelung des Zeichens zeitliche Dauer bedeutet, bezeichnet sie bei der Erde die räumliche Ausdehnung und Festigkeit, kraft deren die Erde alle lebenden und sich bewegenden Dinge trägt und erhält."
        },
        "es": {
            "nom": "Lo Receptivo",
            "jugement": "LO RECEPTIVO obra un éxito sublime, favoreciendo por la perseverancia de una yegua. Si el hombre noble emprende algo y quiere dirigir, se extravía; pero si sigue, encuentra guía.\n\nLa condición de la tierra es la devoción receptiva. Así el hombre noble de amplio carácter sostiene al mundo exterior.",
            "image": "La condición de la tierra es la devoción receptiva.\nAsí el hombre noble de amplio carácter sostiene al mundo exterior.\n\nAsí como hay un solo cielo, también hay una sola tierra. Pero mientras que en el caso del cielo la duplicación del trigrama significa duración en el tiempo, en el caso de la tierra connota la solidez y extensión en el espacio, en virtud de las cuales la tierra puede sostener y preservar todas las cosas que viven y se mueven sobre ella."
        },
        "zh": {
            "nom": "接受",
            "jugement": "坤：元亨，利牝马之贞。君子有攸往，先迷后得主。\n\n地势坤，君子以厚德载物。\n\n此卦纯阴柔顺。君子若欲有所作为而自居领导，必致迷失；若能顺从，则得指引。",
            "image": "地势坤，君子以厚德载物。\n\n天只有一个，地也只有一个。但天之重卦表示时间的持续，地之重卦则表示空间的广袤与坚实，凭此大地承载并保育一切生灵。"
        }
    },
    3: {
        "en": {
            "nom": "Difficulty at the Beginning",
            "jugement": "DIFFICULTY AT THE BEGINNING works supreme success, furthering through perseverance. Nothing should be undertaken. It furthers one to appoint helpers.\n\nClouds and thunder: the image of DIFFICULTY AT THE BEGINNING. Thus the superior man brings order out of confusion.",
            "image": "Clouds and thunder:\nThe image of DIFFICULTY AT THE BEGINNING.\nThus the superior man brings order out of confusion.\n\nClouds and thunder are represented by definite decorative lines; this means that in the chaos of difficulty at the beginning, order is already implicit. So too the superior man has to arrange and organize the inchoate profusion of such times of beginning."
        },
        "de": {
            "nom": "Die Anfangsschwierigkeit",
            "jugement": "DIE ANFANGSSCHWIERIGKEIT wirkt erhabenes Gelingen, fördernd durch Beharrlichkeit. Man soll nichts unternehmen. Fördernd ist es, Gehilfen einzusetzen.\n\nWolken und Donner: das Bild der ANFANGSSCHWIERIGKEIT. So bringt der Edle Ordnung aus der Verwirrung.",
            "image": "Wolken und Donner:\nDas Bild der ANFANGSSCHWIERIGKEIT.\nSo bringt der Edle Ordnung aus der Verwirrung.\n\nWolken und Donner sind durch bestimmte Schmucklinien dargestellt; das bedeutet, dass im Chaos der Anfangsschwierigkeit die Ordnung bereits enthalten ist. So muss auch der Edle die ungeformte Fülle solcher Anfangszeiten ordnen und organisieren."
        },
        "es": {
            "nom": "La Dificultad Inicial",
            "jugement": "LA DIFICULTAD INICIAL obra un éxito sublime, favoreciendo por la perseverancia. No se debe emprender nada. Es favorable designar ayudantes.\n\nNubes y trueno: la imagen de LA DIFICULTAD INICIAL. Así el hombre noble pone orden en la confusión.",
            "image": "Nubes y trueno:\nLa imagen de LA DIFICULTAD INICIAL.\nAsí el hombre noble pone orden en la confusión.\n\nNubes y trueno están representados por líneas decorativas definidas; esto significa que en el caos de la dificultad inicial, el orden ya está implícito. Así también el hombre noble debe organizar la profusión incipiente de tales tiempos de comienzo."
        },
        "zh": {
            "nom": "初难",
            "jugement": "屯：元亨利贞，勿用有攸往，利建侯。\n\n云雷屯，君子以经纶。\n\n此卦表示万事开头难。不宜轻举妄动，宜任用贤能之士辅助。",
            "image": "云雷屯，君子以经纶。\n\n云雷交加，象征初始的混乱中已蕴含秩序。君子当整理组织这开创时期的纷乱局面。"
        }
    },
    4: {
        "en": {
            "nom": "Youthful Folly",
            "jugement": "YOUTHFUL FOLLY has success. It is not I who seek the young fool; the young fool seeks me. At the first oracle I inform him. If he asks two or three times, it is importunity. If he importunes, I give him no information. Perseverance furthers.",
            "image": "A spring wells up at the foot of the mountain:\nThe image of YOUTH.\nThus the superior man fosters his character by thoroughness in all that he does."
        },
        "de": {
            "nom": "Die Jugendtorheit",
            "jugement": "JUGENDTORHEIT hat Gelingen. Nicht ich suche den jungen Toren, der junge Tor sucht mich. Beim ersten Orakel gebe ich Auskunft. Fragt er zwei-, dreimal, so ist es Belästigung. Wenn er belästigt, gebe ich keine Auskunft. Fördernd ist Beharrlichkeit.",
            "image": "Am Fuß des Berges quillt eine Quelle hervor:\nDas Bild der JUGEND.\nSo pflegt der Edle seinen Charakter durch Gründlichkeit in allem, was er tut."
        },
        "es": {
            "nom": "La Necedad Juvenil",
            "jugement": "LA NECEDAD JUVENIL tiene éxito. No soy yo quien busca al joven necio; el joven necio me busca a mí. En la primera consulta le informo. Si pregunta dos o tres veces, es importunidad. Si importuna, no le doy información. La perseverancia es favorable.",
            "image": "Un manantial brota al pie de la montaña:\nLa imagen de LA JUVENTUD.\nAsí el hombre noble cultiva su carácter siendo minucioso en todo lo que hace."
        },
        "zh": {
            "nom": "蒙昧",
            "jugement": "蒙：亨。匪我求童蒙，童蒙求我。初筮告，再三渎，渎则不告。利贞。",
            "image": "山下出泉，蒙。君子以果行育德。\n\n山下涌出泉水，象征蒙昧初开。君子当以果敢行动培育德行。"
        }
    },
    5: {
        "en": {
            "nom": "Waiting",
            "jugement": "WAITING. If you are sincere, you have light and success. Perseverance brings good fortune. It furthers one to cross the great water.",
            "image": "Clouds rise up to heaven:\nThe image of WAITING.\nThus the superior man eats and drinks, is joyous and of good cheer."
        },
        "de": {
            "nom": "Das Warten",
            "jugement": "WARTEN. Wenn du wahrhaftig bist, hast du Licht und Gelingen. Beharrlichkeit bringt Heil. Es fördert, das große Wasser zu durchqueren.",
            "image": "Wolken steigen am Himmel auf:\nDas Bild des WARTENS.\nSo isst und trinkt der Edle und ist heiter und guter Dinge."
        },
        "es": {
            "nom": "La Espera",
            "jugement": "LA ESPERA. Si eres sincero, tienes luz y éxito. La perseverancia trae buena fortuna. Es favorable cruzar las grandes aguas.",
            "image": "Las nubes ascienden al cielo:\nLa imagen de LA ESPERA.\nAsí el hombre noble come y bebe, está alegre y de buen ánimo."
        },
        "zh": {
            "nom": "等待",
            "jugement": "需：有孚，光亨，贞吉。利涉大川。",
            "image": "云上于天，需。君子以饮食宴乐。\n\n云升于天，等待降雨。君子当安然饮食宴乐，静待时机。"
        }
    },
    6: {
        "en": {
            "nom": "Conflict",
            "jugement": "CONFLICT. You are sincere and are being obstructed. A cautious halt halfway brings good fortune. Going through to the end brings misfortune. It furthers one to see the great man. It does not further one to cross the great water.",
            "image": "Heaven and water go their opposite ways:\nThe image of CONFLICT.\nThus in all his transactions the superior man carefully considers the beginning."
        },
        "de": {
            "nom": "Der Streit",
            "jugement": "STREIT. Du bist wahrhaftig und wirst gehemmt. Vorsichtiges Innehalten in der Mitte bringt Heil. Durchführen bis zum Ende bringt Unheil. Fördernd ist es, den großen Mann zu sehen. Nicht fördernd ist es, das große Wasser zu durchqueren.",
            "image": "Himmel und Wasser gehen ihre entgegengesetzten Wege:\nDas Bild des STREITS.\nSo erwägt der Edle bei allen seinen Geschäften sorgfältig den Anfang."
        },
        "es": {
            "nom": "El Conflicto",
            "jugement": "EL CONFLICTO. Eres sincero y estás siendo obstaculizado. Una pausa cautelosa a mitad de camino trae buena fortuna. Llegar hasta el final trae desgracia. Es favorable ver al gran hombre. No es favorable cruzar las grandes aguas.",
            "image": "El cielo y el agua van en direcciones opuestas:\nLa imagen del CONFLICTO.\nAsí el hombre noble considera cuidadosamente el comienzo en todas sus transacciones."
        },
        "zh": {
            "nom": "争讼",
            "jugement": "讼：有孚，窒。惕中吉，终凶。利见大人，不利涉大川。",
            "image": "天与水违行，讼。君子以作事谋始。\n\n天水相背而行，象征争讼。君子当谨慎从事，慎重开始。"
        }
    },
    7: {
        "en": {
            "nom": "The Army",
            "jugement": "THE ARMY. The army needs perseverance and a strong man. Good fortune without blame.",
            "image": "In the middle of the earth is water:\nThe image of THE ARMY.\nThus the superior man increases his masses by generosity toward the people."
        },
        "de": {
            "nom": "Das Heer",
            "jugement": "DAS HEER braucht Beharrlichkeit und einen starken Mann. Heil ohne Makel.",
            "image": "Mitten in der Erde ist Wasser:\nDas Bild des HEERES.\nSo mehrt der Edle seine Scharen durch Leutseligkeit gegen das Volk."
        },
        "es": {
            "nom": "El Ejército",
            "jugement": "EL EJÉRCITO necesita perseverancia y un hombre fuerte. Buena fortuna sin culpa.",
            "image": "En medio de la tierra hay agua:\nLa imagen del EJÉRCITO.\nAsí el hombre noble aumenta sus masas mediante la generosidad hacia el pueblo."
        },
        "zh": {
            "nom": "军队",
            "jugement": "师：贞，丈人吉，无咎。",
            "image": "地中有水，师。君子以容民畜众。\n\n地中蓄水，象征军队。君子当宽容百姓，蓄养民众。"
        }
    },
    8: {
        "en": {
            "nom": "Holding Together",
            "jugement": "HOLDING TOGETHER brings good fortune. Inquire of the oracle once again whether you possess sublimity, constancy, and perseverance; then there is no blame. Those who are uncertain gradually join. Whoever comes too late meets with misfortune.",
            "image": "On the earth is water:\nThe image of HOLDING TOGETHER.\nThus the kings of antiquity bestowed the different states as fiefs and cultivated friendly relations with the feudal lords."
        },
        "de": {
            "nom": "Das Zusammenhalten",
            "jugement": "ZUSAMMENHALTEN bringt Heil. Befrage das Orakel noch einmal, ob du Erhabenheit, Dauer und Beharrlichkeit hast; dann ist kein Makel. Die Unsicheren schließen sich allmählich an. Wer zu spät kommt, hat Unheil.",
            "image": "Auf der Erde ist Wasser:\nDas Bild des ZUSAMMENHALTENS.\nSo verliehen die Könige des Altertums die verschiedenen Staaten als Lehen und pflegten freundliche Beziehungen mit den Lehnsfürsten."
        },
        "es": {
            "nom": "La Solidaridad",
            "jugement": "LA SOLIDARIDAD trae buena fortuna. Consulta el oráculo una vez más para saber si posees sublimidad, constancia y perseverancia; entonces no hay culpa. Los indecisos se unen gradualmente. Quien llega demasiado tarde encuentra desgracia.",
            "image": "Sobre la tierra hay agua:\nLa imagen de LA SOLIDARIDAD.\nAsí los reyes de la antigüedad otorgaban los diferentes estados como feudos y cultivaban relaciones amistosas con los señores feudales."
        },
        "zh": {
            "nom": "团结",
            "jugement": "比：吉。原筮元永贞，无咎。不宁方来，后夫凶。",
            "image": "地上有水，比。先王以建万国，亲诸侯。\n\n水在地上汇聚，象征亲比团结。先王建立诸侯国，亲善诸侯。"
        }
    },
}

# Continuer avec les 64 hexagrammes...
# Pour les hexagrammes 9-64, je vais générer les traductions de base

def generate_remaining_hexagrams():
    """Génère les traductions pour les hexagrammes 9-64 basées sur les noms traduits"""
    from translations import HEX_NAMES
    
    remaining = {}
    
    for num in range(9, 65):
        if num in HEX_NAMES:
            remaining[num] = {
                "en": {
                    "nom": HEX_NAMES[num]["en"],
                    "jugement": "",  # À compléter
                    "image": ""
                },
                "de": {
                    "nom": HEX_NAMES[num]["de"],
                    "jugement": "",
                    "image": ""
                },
                "es": {
                    "nom": HEX_NAMES[num]["es"],
                    "jugement": "",
                    "image": ""
                },
                "zh": {
                    "nom": HEX_NAMES[num]["zh"],
                    "jugement": "",
                    "image": ""
                }
            }
    
    return remaining

# Ajouter les hexagrammes importants avec textes complets
HEXAGRAMS.update({
    11: {
        "en": {
            "nom": "Peace",
            "jugement": "PEACE. The small departs, the great approaches. Good fortune. Success.",
            "image": "Heaven and earth unite: the image of PEACE.\nThus the ruler divides and completes the course of heaven and earth, furthers and regulates the gifts of heaven and earth, and so aids the people."
        },
        "de": {
            "nom": "Der Friede",
            "jugement": "FRIEDE. Das Kleine geht, das Große kommt. Heil. Gelingen.",
            "image": "Himmel und Erde vereinigen sich: das Bild des FRIEDENS.\nSo teilt der Herrscher den Lauf von Himmel und Erde und vollendet ihn, fördert und regelt die Gaben von Himmel und Erde und hilft so dem Volk."
        },
        "es": {
            "nom": "La Paz",
            "jugement": "LA PAZ. Lo pequeño parte, lo grande se acerca. Buena fortuna. Éxito.",
            "image": "El cielo y la tierra se unen: la imagen de LA PAZ.\nAsí el gobernante divide y completa el curso del cielo y la tierra, fomenta y regula los dones del cielo y la tierra, y así ayuda al pueblo."
        },
        "zh": {
            "nom": "和平",
            "jugement": "泰：小往大来，吉亨。",
            "image": "天地交，泰。后以财成天地之道，辅相天地之宜，以左右民。"
        }
    },
    12: {
        "en": {
            "nom": "Standstill",
            "jugement": "STANDSTILL. Evil people do not further the perseverance of the superior man. The great departs; the small approaches.",
            "image": "Heaven and earth do not unite: the image of STANDSTILL.\nThus the superior man falls back upon his inner worth in order to escape the difficulties. He does not permit himself to be honored with revenue."
        },
        "de": {
            "nom": "Die Stockung",
            "jugement": "STOCKUNG. Böse Menschen fördern nicht die Beharrlichkeit des Edlen. Das Große geht; das Kleine kommt.",
            "image": "Himmel und Erde vereinigen sich nicht: das Bild der STOCKUNG.\nSo zieht der Edle sich auf seinen inneren Wert zurück, um den Schwierigkeiten zu entgehen. Er lässt sich nicht mit Gehalt ehren."
        },
        "es": {
            "nom": "El Estancamiento",
            "jugement": "EL ESTANCAMIENTO. Las personas malvadas no favorecen la perseverancia del hombre noble. Lo grande parte; lo pequeño se acerca.",
            "image": "El cielo y la tierra no se unen: la imagen del ESTANCAMIENTO.\nAsí el hombre noble se retira a su valor interior para escapar de las dificultades. No se permite ser honrado con ingresos."
        },
        "zh": {
            "nom": "闭塞",
            "jugement": "否：否之匪人，不利君子贞，大往小来。",
            "image": "天地不交，否。君子以俭德辟难，不可荣以禄。"
        }
    },
    63: {
        "en": {
            "nom": "After Completion",
            "jugement": "AFTER COMPLETION. Success in small matters. Perseverance furthers. At the beginning good fortune, at the end disorder.",
            "image": "Water over fire: the image of the condition in AFTER COMPLETION.\nThus the superior man takes thought of misfortune and arms himself against it in advance."
        },
        "de": {
            "nom": "Nach der Vollendung",
            "jugement": "NACH DER VOLLENDUNG. Gelingen im Kleinen. Beharrlichkeit fördert. Am Anfang Heil, am Ende Wirren.",
            "image": "Wasser über Feuer: das Bild des Zustands NACH DER VOLLENDUNG.\nSo denkt der Edle an das Unglück und wappnet sich dagegen im voraus."
        },
        "es": {
            "nom": "Después de la Consumación",
            "jugement": "DESPUÉS DE LA CONSUMACIÓN. Éxito en asuntos pequeños. La perseverancia es favorable. Al principio buena fortuna, al final desorden.",
            "image": "Agua sobre fuego: la imagen de la condición DESPUÉS DE LA CONSUMACIÓN.\nAsí el hombre noble piensa en la desgracia y se arma contra ella por adelantado."
        },
        "zh": {
            "nom": "既济",
            "jugement": "既济：亨小，利贞。初吉终乱。",
            "image": "水在火上，既济。君子以思患而豫防之。"
        }
    },
    64: {
        "en": {
            "nom": "Before Completion",
            "jugement": "BEFORE COMPLETION. Success. But if the little fox, after nearly completing the crossing, gets his tail in the water, there is nothing that would further.",
            "image": "Fire over water: the image of the condition before transition.\nThus the superior man is careful in the differentiation of things, so that each finds its place."
        },
        "de": {
            "nom": "Vor der Vollendung",
            "jugement": "VOR DER VOLLENDUNG. Gelingen. Wenn aber der kleine Fuchs, nachdem er fast hinübergekommen ist, seinen Schwanz ins Wasser bekommt, ist nichts, das fördern würde.",
            "image": "Feuer über Wasser: das Bild des Zustands vor dem Übergang.\nSo ist der Edle vorsichtig bei der Unterscheidung der Dinge, damit jedes seinen Platz findet."
        },
        "es": {
            "nom": "Antes de la Consumación",
            "jugement": "ANTES DE LA CONSUMACIÓN. Éxito. Pero si el pequeño zorro, después de casi completar el cruce, moja su cola en el agua, no hay nada que sea favorable.",
            "image": "Fuego sobre agua: la imagen de la condición antes de la transición.\nAsí el hombre noble es cuidadoso en la diferenciación de las cosas, para que cada una encuentre su lugar."
        },
        "zh": {
            "nom": "未济",
            "jugement": "未济：亨。小狐汔济，濡其尾，无攸利。",
            "image": "火在水上，未济。君子以慎辨物居方。"
        }
    },
})

def create_json_for_language(lang_code):
    """Crée un fichier JSON complet pour une langue donnée"""
    from translations import HEX_NAMES, TRIGRAM_NAMES
    
    # Copier la structure française
    data = copy.deepcopy(DATA_FR)
    
    # Traduire chaque hexagramme
    for hex_data in data['hexagrammes']:
        num = hex_data['numero']
        
        # Nom traduit
        if num in HEX_NAMES:
            hex_data['nom_fr'] = HEX_NAMES[num].get(lang_code, hex_data['nom_fr'])
        
        # Descriptions des trigrammes
        trig_haut = hex_data.get('trigramme_haut', '')
        trig_bas = hex_data.get('trigramme_bas', '')
        
        if trig_haut in TRIGRAM_NAMES:
            hex_data['trigramme_haut_desc'] = TRIGRAM_NAMES[trig_haut].get(lang_code, hex_data['trigramme_haut_desc'])
        if trig_bas in TRIGRAM_NAMES:
            hex_data['trigramme_bas_desc'] = TRIGRAM_NAMES[trig_bas].get(lang_code, hex_data['trigramme_bas_desc'])
        
        # Textes complets si disponibles
        if num in HEXAGRAMS and lang_code in HEXAGRAMS[num]:
            trans = HEXAGRAMS[num][lang_code]
            if trans.get('jugement'):
                hex_data['jugement_texte'] = trans['jugement']
            if trans.get('image'):
                hex_data['image_texte'] = trans['image']
    
    return data

def main():
    """Génère tous les fichiers JSON"""
    languages = ['en', 'de', 'es', 'zh']
    
    for lang in languages:
        print(f"Génération de yijing_{lang}.json...")
        data = create_json_for_language(lang)
        
        filename = f'yijing_{lang}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ {filename} créé")
    
    print("\n✓ Tous les fichiers JSON générés!")

if __name__ == "__main__":
    main()
