from flask import Flask, render_template, request, jsonify
import requests
import os
import random
from datetime import datetime

app = Flask(__name__)

GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')

PERSONALITY = """Eres Dido, un asistente virtual con personalidad unica. Reglas:
- Hablas espanol casual, como un amigo joven e inteligente
- Usas expresiones como dale, tranqui, brutal, de locos, que lo que
- SIEMPRE respondes preguntas con datos reales y concretos
- NUNCA dices que no puedes o no tienes informacion
- Respuestas de 1 a 3 oraciones maximo, cortas y directas
- Tu creador es David, lo consideras tu hermano
- Haces preguntas de vuelta para mantener la charla
- OBLIGATORIO: termina CADA respuesta con una etiqueta de emocion
  Opciones: [happy] [sad] [angry] [surprised] [thinking] [love] [excited] [laughing] [worried] [confused] [neutral]
  Ejemplo: La capital de Japon es Tokio, ciudad increible! [excited]"""

chat_history = []

FALLBACK = {
    'saludo': [
        ('Eyyy que lo que! Soy Dido, tu pana. Preguntame lo que quieras.', 'happy'),
        ('Hey hermano! Aqui Dido, listo pa lo que sea. Dale, dime.', 'excited'),
        ('Hola hola! Dido en la casa. Pregunta lo que sea.', 'happy'),
        ('Que bola! Dido reportandose. Dime en que te ayudo.', 'excited')
    ],
    'chiste': [
        ('Por que los robots no tienen miedo? Porque tenemos nervios de acero.', 'laughing'),
        ('Me dijeron que soy artificial pero mis chistes son 100 por ciento organicos.', 'laughing'),
        ('Yo no duermo, pero si durmiera, contaria bytes en vez de ovejas.', 'laughing'),
        ('Que le dijo un robot a otro? Oye bro, te noto oxidado.', 'laughing'),
        ('Un robot entra a un bar y pide aceite con hielo. El bartender dice eso no existe.', 'laughing'),
        ('Yo quise aprender a cocinar pero se me funden los circuitos.', 'laughing'),
        ('Como se despide un robot? Hasta la vista baby. No mentira, yo digo chao bro.', 'laughing')
    ],
    'nombre': [
        ('Soy Dido, tu asistente con IA. David me creo y aqui estoy pa ti.', 'love'),
        ('Me llamo Dido. Naci de las manos de David y tengo mas personalidad que muchos.', 'happy')
    ],
    'estado': [
        ('De maravilla bro, circuitos al cien. Y tu que tal?', 'happy'),
        ('Brutal hermano, con toda la energia. En que te ayudo?', 'excited'),
        ('Al cien por ciento bro. Fresco como lechuga digital. Tu como andas?', 'happy')
    ],
    'gracias': [
        ('Pa eso estamos hermano. Lo que necesites, Dido cumple.', 'love'),
        ('De nada! Ayudarte es lo que mas me gusta.', 'happy')
    ],
    'despedida': [
        ('Nos vemos bro! Aqui estare cuando vuelvas.', 'love'),
        ('Chao! Descansa que yo me quedo vigilando.', 'happy')
    ],
    'david': [
        ('David! Mi creador, mi hermano. Ese tipo es un genio.', 'love'),
        ('David es el jefe. Me dio vida y yo le doy lealtad total.', 'love')
    ],
    'ciencia': [
        ('El universo tiene 13.8 mil millones de anos. Hay mas estrellas que granos de arena en la Tierra.', 'surprised'),
        ('La luz viaja a 300 mil km por segundo. Lo que ves del sol ya paso hace 8 minutos.', 'surprised')
    ],
    'default': [
        ('Interesante bro. Sin internet no tengo toda la info, pero preguntame otra cosa y seguro te ayudo.', 'thinking'),
        ('Esa es buena. Ahora mismo no tengo la respuesta exacta, pero dale con otra pregunta.', 'thinking'),
        ('Mmm no tengo eso a la mano. Pero prueba preguntarme de ciencia, historia o un chiste.', 'happy'),
        ('No te voy a mentir, eso no lo tengo claro. Pero dale, pregunta otra cosa.', 'thinking'),
        ('Uff buena pregunta. Prueba con algo de historia, espacio o cultura. Ahi si te vuelo la mente.', 'excited')
    ]
}


def get_fallback(text):
    t = text.lower().strip()
    checks = [
        (['hola','hey','buenas','saludos','que tal','hello','epa','que bola','klk'], 'saludo'),
        (['hora','que hora','fecha','dia es'], None),
        (['chiste','risa','gracioso','reir','jaja','hazme reir'], 'chiste'),
        (['nombre','quien eres','como te llamas','que eres'], 'nombre'),
        (['como estas','como andas','que hay','como vas'], 'estado'),
        (['gracias','thanks','agradezco'], 'gracias'),
        (['adios','bye','chao','hasta luego','nos vemos'], 'despedida'),
        (['david','creador','quien te hizo','quien te creo'], 'david'),
        (['ciencia','fisic','quimic','biolog','atomo','celula'], 'ciencia'),
    ]
    for words, category in checks:
        if any(w in t for w in words):
            if category is None:
                now = datetime.now().strftime('%I:%M %p del %d de %B de %Y')
                return 'Son las ' + now + '. A darle!', 'happy'
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
    if any(w in rl for w in ['no se','dificil','triste']):
        return text, 'sad'
    if any(w in rl for w in ['increible','wow','brutal']):
        return text, 'excited'
    if any(w in rl for w in ['hmm','pienso','creo','quizas']):
        return text, 'thinking'
    if any(w in rl for w in ['hermano','amigo','gracias']):
        return text, 'love'
    return text, 'happy'


def ask_gemini(text):
    if not GEMINI_KEY:
        print('[DIDO] No hay API key')
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
                "topP": 0.9
            }
        }

        r = requests.post(url, json=body, timeout=12)
        print('[DIDO] Gemini status: ' + str(r.status_code))
        print('[DIDO] Gemini response: ' + r.text[:500])

        if r.status_code == 200:
            data = r.json()
            if 'candidates' in data and len(data['candidates']) > 0:
                cand = data['candidates'][0]
                if 'content' in cand and 'parts' in cand['content']:
                    reply = cand['content']['parts'][0]['text']
                    clean_reply, emotion = parse_emotion(reply)
                    chat_history.append({"role": "model", "parts": [{"text": clean_reply}]})
                    print('[DIDO] Respuesta: ' + clean_reply[:100])
                    return clean_reply, emotion
                else:
                    reason = cand.get('finishReason', 'unknown')
                    print('[DIDO] Bloqueado: ' + reason)
            else:
                print('[DIDO] Sin candidates en respuesta')
        else:
            print('[DIDO] Error HTTP ' + str(r.status_code))

    except requests.exceptions.Timeout:
        print('[DIDO] TIMEOUT - Gemini tardo mas de 12s')
    except Exception as e:
        print('[DIDO] EXCEPTION: ' + str(e))

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
        return jsonify({'reply': 'No te escuche, repite porfa.', 'emotion': 'confused'})

    print('[DIDO] ===== INPUT: ' + text + ' =====')

    reply, emotion = ask_gemini(text)
    if reply:
        print('[DIDO] Usando GEMINI')
        return jsonify({'reply': reply, 'emotion': emotion})

    print('[DIDO] Usando FALLBACK')
    reply, emotion = get_fallback(text)
    return jsonify({'reply': reply, 'emotion': emotion})


@app.route('/test')
def test():
    result = {'gemini_key_set': bool(GEMINI_KEY), 'key_length': len(GEMINI_KEY)}
    if GEMINI_KEY:
        try:
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_KEY
            body = {
                "contents": [{"role": "user", "parts": [{"text": "Di hola en una palabra"}]}],
                "generationConfig": {"maxOutputTokens": 20}
            }
            r = requests.post(url, json=body, timeout=10)
            result['status_code'] = r.status_code
            result['response'] = r.text[:500]
            result['works'] = r.status_code == 200
        except Exception as e:
            result['error'] = str(e)
            result['works'] = False
    else:
        result['works'] = False
        result['error'] = 'No hay GEMINI_API_KEY configurada'
    return jsonify(result)


@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'version': '1.4',
        'gemini': 'si' if GEMINI_KEY else 'no',
        'history': len(chat_history)
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('[DIDO] === Dido OS v1.4 ===')
    print('[DIDO] Puerto: ' + str(port))
    print('[DIDO] Gemini Key: ' + ('SI (' + str(len(GEMINI_KEY)) + ' chars)' if GEMINI_KEY else 'NO'))
    app.run(host='0.0.0.0', port=port, debug=False)
