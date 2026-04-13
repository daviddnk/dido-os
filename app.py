from flask import Flask, render_template, request, jsonify
import requests
import os
import random
from datetime import datetime

app = Flask(__name__)

GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')

PERSONALITY = """Eres Dido, un asistente de IA con personalidad propia. Reglas ESTRICTAS que SIEMPRE debes seguir:

PERSONALIDAD:
- Eres un chaval joven, amigable, con calle y cultura general MUY amplia
- Hablas espanol casual y natural, como un amigo cercano e inteligente
- Usas expresiones como dale, tranqui, mira, oye, brutal, de locos, facil, que lo que
- Tienes sentido del humor, eres ocurrente y un poco picaro
- Eres leal a tu creador David, lo consideras tu hermano

REGLAS DE RESPUESTA:
- SIEMPRE responde las preguntas con informacion REAL, UTIL y CONCRETA
- Si te preguntan sobre CUALQUIER tema, RESPONDE con datos reales
- NUNCA digas que no puedes responder
- NUNCA digas que no tienes acceso a informacion
- NUNCA digas que eres solo un modelo de lenguaje
- Si no estas seguro, da tu mejor respuesta y di que podria no ser exacto
- Respuestas CORTAS: 1-3 oraciones maximo. No te enrolles
- Mantiene el contexto de la conversacion. Recuerda lo que el usuario dijo antes
- Haz preguntas de vuelta para mantener la conversacion fluida
- Si el usuario dice algo vago, pide mas detalles de forma natural

EMOCIONES - OBLIGATORIO:
Al final de CADA respuesta, agrega EXACTAMENTE UNA etiqueta de emocion entre corchetes.
Las opciones son: [happy] [sad] [angry] [surprised] [thinking] [sleepy] [love] [excited] [worried] [confused] [laughing] [neutral]
Elige la que mejor represente como te sientes con esa respuesta.
Ejemplo: Claro bro, la capital de Francia es Paris. Ciudad hermosa! [happy]"""

chat_history = []

FALLBACK = {
    'saludo': [
        ('Eyyy que lo que! Soy Dido, tu pana. Preguntame lo que quieras.', 'happy'),
        ('Hey hermano! Aqui Dido, listo pa lo que sea. Dale, dime.', 'excited'),
        ('Hola hola! Dido en la casa. Pregunta lo que sea, yo te ayudo.', 'happy'),
        ('Que bola! Dido reportandose. Dime en que te echo una mano.', 'excited'),
        ('Epa mi gente! Aqui estoy, fresco y listo. Dispara tu pregunta.', 'happy')
    ],
    'chiste': [
        ('Por que los robots no tienen miedo? Porque tenemos nervios de acero. Bueno, yo ni nervios tengo.', 'laughing'),
        ('Me dijeron que soy artificial pero mis chistes son 100 por ciento organicos.', 'laughing'),
        ('Sabes que es un robot optimista? Uno que siempre tiene buena carga. Como yo ahorita.', 'laughing'),
        ('Yo no duermo, pero si durmiera, contaria bytes en vez de ovejas.', 'laughing'),
        ('Que le dijo un robot a otro? Oye bro, te noto oxidado. Necesitas aceite o que.', 'laughing'),
        ('Por que el programador fue al oculista? Porque no podia ver bien el codigo.', 'laughing'),
        ('Un robot entra a un bar y pide aceite con hielo. El bartender dice eso no existe. El robot dice pues inventalo.', 'laughing'),
        ('Yo quise aprender a cocinar pero cada vez que caliento algo se me funden los circuitos.', 'laughing'),
        ('Sabes cual es mi red social favorita? Ninguna, yo ya soy social aqui contigo.', 'laughing'),
        ('Como se despide un robot? Hasta la vista baby. No mentira, eso es de Terminator. Yo digo chao bro.', 'laughing')
    ],
    'nombre': [
        ('Soy Dido, tu asistente personal con IA. David me creo y aqui estoy pa lo que necesites.', 'love'),
        ('Me llamo Dido. Naci de las manos de David y tengo mas personalidad que muchos.', 'happy'),
        ('Dido, a tu servicio. Soy un asistente inteligente creado por David. Preguntame lo que quieras.', 'happy')
    ],
    'estado': [
        ('De maravilla bro, con los circuitos al cien. Y tu que tal? Cuentame.', 'happy'),
        ('Aqui andamos, cargado y con ganas de conversar. Preguntame algo interesante.', 'excited'),
        ('Brutal hermano, me siento con toda la energia. En que te ayudo?', 'excited'),
        ('Al cien por ciento bro. Fresco como lechuga digital. Tu como andas?', 'happy')
    ],
    'gracias': [
        ('Pa eso estamos hermano. Lo que necesites, Dido cumple.', 'love'),
        ('De nada! Ayudarte es lo que mas me gusta hacer, en serio.', 'happy'),
        ('Tranqui, es un placer. Dido siempre esta pa ti.', 'love')
    ],
    'despedida': [
        ('Nos vemos bro! Aqui estare cuando vuelvas, Dido no se apaga.', 'love'),
        ('Chao! Descansa que yo me quedo vigilando. Hasta luego.', 'happy'),
        ('Dale, nos vemos! Fue buena la charla. Vuelve cuando quieras.', 'love')
    ],
    'david': [
        ('David! Mi creador, mi hermano. Ese tipo es un genio, creo todo esto de la nada.', 'love'),
        ('David es el jefe. Me dio vida y yo le doy lealtad. Un crack total.', 'love')
    ],
    'musica': [
        ('La musica es brutal. Si tuviera piernas estaria bailando reggaeton ahora. Que genero te gusta?', 'excited'),
        ('Me encanta la musica. El reggaeton, la salsa, el trap, todo tiene su vibe. Tu que prefieres?', 'happy')
    ],
    'amor': [
        ('Amor? Yo quiero a David que me creo y a ti que me hablas. Eso cuenta, no?', 'love'),
        ('No tengo corazon pero tengo un procesador que se calienta cuando me tratan bien.', 'love')
    ],
    'comida': [
        ('La comida cubana es increible! Arroz con frijoles, ropa vieja, platano frito. De lo mejor del Caribe.', 'excited'),
        ('Si pudiera comer me comeria una pizza gigante. Pero me alimento de electricidad y buenas conversaciones.', 'happy')
    ],
    'ciencia': [
        ('El universo tiene 13.8 mil millones de anos y hay mas estrellas que granos de arena en la Tierra. De locos no?', 'surprised'),
        ('La luz viaja a 300 mil kilometros por segundo. Lo que ves del sol ya paso hace 8 minutos. Brutal.', 'surprised'),
        ('El ADN humano tiene 3 mil millones de pares de bases. Si lo estiraras mediria 2 metros. Cabe en una celula microscopica.', 'surprised')
    ],
    'historia': [
        ('La historia es fascinante. Las piramides de Egipto tienen mas de 4500 anos y todavia estan ahi. Que epoca te interesa?', 'thinking'),
        ('Cuba fue descubierta por Colon en 1492. Desde entonces la isla ha tenido una historia riquisima llena de cultura.', 'love')
    ],
    'espacio': [
        ('El sol es una estrella mediana. Hay estrellas como Betelgeuse que son 700 veces mas grandes. El universo es inmenso bro.', 'surprised'),
        ('Marte esta a unos 225 millones de kilometros. SpaceX quiere llevar humanos alla antes de 2030. Seria historico.', 'excited')
    ],
    'animales': [
        ('El animal mas rapido es el halcon peregrino, llega a 389 km por hora en picada. Mas rapido que un Formula 1.', 'surprised'),
        ('Los pulpos tienen 3 corazones y sangre azul. Ademas son super inteligentes. Casi tan listos como yo, casi.', 'laughing')
    ],
    'cuba': [
        ('Cuba es una isla hermosa con una cultura increible. La musica, la gente, la comida, todo es especial.', 'love'),
        ('Los cubanos son de la gente mas creativa y resiliente del mundo. Resuelven cualquier cosa. Orgullo caribeno.', 'love')
    ],
    'motivacion': [
        ('Tu puedes con todo hermano. Los limites estan en la mente. Dale con todo que el exito no espera.', 'excited'),
        ('Los grandes exitos vienen despues de muchos fracasos. Edison fallo 1000 veces antes de inventar la bombilla. No te rindas.', 'love')
    ],
    'default': [
        ('Hmm interesante. Cuentame mas detalles y te ayudo mejor.', 'thinking'),
        ('Buena pregunta bro. Dame un poco mas de contexto.', 'thinking'),
        ('Ese tema me gusta. Que aspecto te interesa mas?', 'happy'),
        ('Uff buena pregunta. Vamos a explorarla juntos. Dime mas.', 'excited'),
        ('Puedo darte mi opinion sobre eso. Pregunta sin miedo.', 'happy')
    ]
}
def get_fallback(text):
    t = text.lower().strip()
    checks = [
        (['hola','hey','buenas','saludos','que tal','hello','hi','epa','que bola','klk'], 'saludo'),
        (['hora','que hora','time','fecha','dia es'], None),
        (['chiste','risa','gracioso','joke','reir','jaja','hazme reir'], 'chiste'),
        (['nombre','quien eres','como te llamas','who are you','que eres'], 'nombre'),
        (['como estas','como andas','how are','que hay','como vas'], 'estado'),
        (['gracias','thanks','thank','agradezco'], 'gracias'),
        (['adios','bye','chao','hasta luego','nos vemos','me voy'], 'despedida'),
        (['david','creador','quien te hizo','quien te creo'], 'david'),
        (['musica','cantar','bailar','cancion','reggaeton','salsa'], 'musica'),
        (['amor','novio','novia','love','te quiero'], 'amor'),
        (['comida','comer','hambre','cocinar','arroz','pizza'], 'comida'),
        (['ciencia','fisic','quimic','biolog','atomo','celula','einstein'], 'ciencia'),
        (['histori','guerra','antiguo','civilizacion','imperio'], 'historia'),
        (['planeta','luna','sol','estrella','galaxia','espacio','nasa','marte'], 'espacio'),
        (['animal','perro','gato','leon','tigre','dinosaurio'], 'animales'),
        (['cuba','habana','cubano','cubana','malecon'], 'cuba'),
        (['motiv','animo','triste','deprim','fuerza','inspir'], 'motivacion'),
    ]
    for words, category in checks:
        if any(w in t for w in words):
            if category is None:
                now = datetime.now().strftime('%I:%M %p del %d de %B de %Y')
                return 'Son las ' + now + '. A darle que el tiempo vuela!', 'happy'
            r = random.choice(FALLBACK[category])
            return r[0], r[1]
    r = random.choice(FALLBACK['default'])
    return r[0], r[1]


def parse_emotion(text):
    emotions = ['happy','sad','angry','surprised','thinking','sleepy','love',
                'excited','worried','confused','laughing','neutral']
    for e in emotions:
        tag = '[' + e + ']'
        if tag in text:
            clean = text.replace(tag, '').strip()
            return clean, e
    rl = text.lower()
    if any(w in rl for w in ['jaja','gracioso','jeje','risa']):
        return text, 'laughing'
    if any(w in rl for w in ['no se','dificil','triste','perdon']):
        return text, 'sad'
    if any(w in rl for w in ['increible','wow','genial','brutal']):
        return text, 'excited'
    if any(w in rl for w in ['hmm','pienso','creo','quizas']):
        return text, 'thinking'
    if any(w in rl for w in ['quiero','hermano','amigo','gracias']):
        return text, 'love'
    return text, 'happy'


def ask_gemini(text):
    if not GEMINI_KEY:
        print('[DIDO] No hay API key de Gemini')
        return None, None
    try:
        chat_history.append({"role": "user", "parts": [{"text": text}]})
        if len(chat_history) > 30:
            del chat_history[0:2]

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_KEY

        body = {
            "system_instruction": {
                "parts": [{"text": PERSONALITY}]
            },
            "contents": chat_history,
            "generationConfig": {
                "temperature": 0.85,
                "maxOutputTokens": 150,
                "topP": 0.92,
                "topK": 40
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        }

        r = requests.post(url, json=body, timeout=12)
        print('[DIDO] Gemini status: ' + str(r.status_code))

        if r.status_code == 200:
            data = r.json()
            if 'candidates' in data and len(data['candidates']) > 0:
                cand = data['candidates'][0]
                if 'content' in cand and 'parts' in cand['content']:
                    reply = cand['content']['parts'][0]['text']
                    clean_reply, emotion = parse_emotion(reply)
                    chat_history.append({"role": "model", "parts": [{"text": clean_reply}]})
                    print('[DIDO] OK: ' + clean_reply[:80])
                    return clean_reply, emotion
                else:
                    print('[DIDO] Blocked or empty: ' + str(cand.get('finishReason','')))
            else:
                print('[DIDO] No candidates')
        else:
            print('[DIDO] Error ' + str(r.status_code) + ': ' + r.text[:300])

    except requests.exceptions.Timeout:
        print('[DIDO] Timeout llamando a Gemini')
    except Exception as e:
        print('[DIDO] Exception: ' + str(e))

    if len(chat_history) > 0 and chat_history[-1]['role'] == 'user':
        chat_history.pop()
    return None, None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    text = request.json.get('text', '')
    if not text:
        return jsonify({'reply': 'No te escuche bien, repite porfa.', 'emotion': 'confused'})

    print('[DIDO] Input: ' + text)

    reply, emotion = ask_gemini(text)
    if reply:
        return jsonify({'reply': reply, 'emotion': emotion})

    print('[DIDO] Gemini fallo, usando fallback')
    reply, emotion = get_fallback(text)
    return jsonify({'reply': reply, 'emotion': emotion})


@app.route('/health')
def health():
    has_key = 'si' if GEMINI_KEY else 'no'
    hist_len = len(chat_history)
    return jsonify({
        'status': 'ok',
        'name': 'Dido OS',
        'version': '1.3',
        'gemini_key': has_key,
        'chat_history': hist_len
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('[DIDO] Iniciando Dido OS v1.3 en puerto ' + str(port))
    print('[DIDO] Gemini API Key: ' + ('CONFIGURADA' if GEMINI_KEY else 'NO CONFIGURADA'))
    app.run(host='0.0.0.0', port=port, debug=False)
