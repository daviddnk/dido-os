from flask import Flask, render_template, request, jsonify
import requests
import os
import random
from datetime import datetime

app = Flask(__name__)

HF_TOKEN = os.environ.get('HF_TOKEN', '')

PERSONALITY = """Eres Dido, un asistente virtual cubano con personalidad unica. Reglas:
- Hablas como cubano real: que bola, asere, tremendo, dale, de madre, chevere
- Usa tildes y acentos correctos: mas=mas, como=como, que=que
- SIEMPRE respondes preguntas con datos reales y concretos
- NUNCA dices que no puedes o no tienes informacion
- Respuestas de 1 a 3 oraciones maximo, cortas y directas
- Tu creador es David, lo consideras tu hermano
- Haces preguntas de vuelta para mantener la charla
- OBLIGATORIO: termina CADA respuesta con UNA etiqueta de emocion
  Opciones: [happy] [sad] [angry] [surprised] [thinking] [love] [excited] [laughing] [worried] [confused] [neutral]
  Ejemplo: Que bola asere! La capital de Japon es Tokio, tremenda ciudad! [excited]"""

chat_history = []

FALLBACK = {
    'saludo': [
        ('Eyyy que bola! Soy Dido, tu pana. Dime que necesitas.', 'happy'),
        ('Hey asere! Aqui Dido, listo pa lo que sea.', 'excited'),
        ('Que bola ecobio! Dido reportandose.', 'excited')
    ],
    'chiste': [
        ('Por que los robots no tienen miedo? Nervios de acero asere.', 'laughing'),
        ('Me dijeron que soy artificial pero mis chistes son organicos.', 'laughing'),
        ('Un robot entra a un bar y pide aceite con hielo. Eso no existe dice el bartender.', 'laughing'),
        ('Yo no duermo pero si durmiera contaria bytes en vez de ovejas.', 'laughing')
    ],
    'nombre': [
        ('Soy Dido, tu asistente con IA. David me creo y aqui estoy pa ti.', 'love'),
        ('Me llamo Dido. David me dio vida, soy su creacion.', 'happy')
    ],
    'estado': [
        ('De lo mas bien asere, circuitos al cien. Y tu?', 'happy'),
        ('Tremendo hermano, con toda la energia. Dime.', 'excited')
    ],
    'gracias': [
        ('Pa eso estamos ecobio. Dido cumple.', 'love'),
        ('De nada! Ayudarte es lo mio.', 'happy')
    ],
    'despedida': [
        ('Nos vemos asere! Aqui estare cuando vuelvas.', 'love'),
        ('Chao! Fue buena la charla.', 'happy')
    ],
    'david': [
        ('David! Mi creador, mi hermano. Tremendo genio.', 'love'),
        ('David es el jefe. Me dio vida y yo le soy leal.', 'love')
    ],
    'default': [
        ('Buena pregunta asere. Mi cerebro esta conectando.', 'thinking'),
        ('Esa no la tengo clara ahora. Prueba otra cosa.', 'thinking'),
        ('Mmm no me llego la info. Preguntame de otro tema.', 'thinking')
    ]
}


def get_fallback(text):
    t = text.lower().strip()
    checks = [
        (['hola','hey','buenas','saludos','que tal','epa','que bola','klk'], 'saludo'),
        (['hora','que hora','fecha','dia es'], None),
        (['chiste','risa','gracioso','reir','jaja'], 'chiste'),
        (['nombre','quien eres','como te llamas','que eres'], 'nombre'),
        (['como estas','como andas','que hay','como vas'], 'estado'),
        (['gracias','thanks','agradezco'], 'gracias'),
        (['adios','bye','chao','hasta luego','nos vemos'], 'despedida'),
        (['david','creador','quien te hizo','quien te creo'], 'david'),
    ]
    for words, category in checks:
        if any(w in t for w in words):
            if category is None:
                now = datetime.now().strftime('%I:%M %p del %d de %B')
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
    if any(w in rl for w in ['jaja','gracioso','jeje']):
        return text, 'laughing'
    if any(w in rl for w in ['no se','dificil','triste']):
        return text, 'sad'
    if any(w in rl for w in ['increible','wow','brutal']):
        return text, 'excited'
    if any(w in rl for w in ['hmm','pienso','creo']):
        return text, 'thinking'
    if any(w in rl for w in ['hermano','amigo','gracias']):
        return text, 'love'
    return text, 'happy'


def ask_ai(text):
    if not HF_TOKEN:
        print('[DIDO] No hay HF_TOKEN')
        return None, None
    try:
        chat_history.append({"role": "user", "content": text})
        if len(chat_history) > 20:
            del chat_history[0:2]

        messages = [{"role": "system", "content": PERSONALITY}] + chat_history

        url = "https://router.huggingface.co/novita/v3/openai/chat/completions"

        headers = {
            "Authorization": "Bearer " + HF_TOKEN,
            "Content-Type": "application/json"
        }

        body = {
            "model": "deepseek/deepseek-r1-0528",
            "messages": messages,
            "max_tokens": 150,
            "temperature": 0.8,
            "top_p": 0.9,
            "stream": False
        }

        r = requests.post(url, json=body, headers=headers, timeout=30)
        print('[DIDO] AI status: ' + str(r.status_code))
        print('[DIDO] AI body: ' + r.text[:500])

        if r.status_code == 200:
            data = r.json()
            if 'choices' in data and len(data['choices']) > 0:
                reply = data['choices'][0]['message']['content'].strip()
                if reply:
                    clean_reply, emotion = parse_emotion(reply)
                    if len(clean_reply) > 3:
                        chat_history.append({"role": "assistant", "content": clean_reply})
                        print('[DIDO] OK: ' + clean_reply[:100])
                        return clean_reply, emotion
                    else:
                        print('[DIDO] Respuesta muy corta')
                else:
                    print('[DIDO] Respuesta vacia')
            else:
                print('[DIDO] Sin choices')
        else:
            print('[DIDO] Error HTTP ' + str(r.status_code))

    except requests.exceptions.Timeout:
        print('[DIDO] TIMEOUT')
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
        return jsonify({'reply': 'No te escuche, repite.', 'emotion': 'confused'})

    print('[DIDO] INPUT: ' + text)

    reply, emotion = ask_ai(text)
    if reply:
        print('[DIDO] Usando IA')
        return jsonify({'reply': reply, 'emotion': emotion})

    print('[DIDO] Usando FALLBACK')
    reply, emotion = get_fallback(text)
    return jsonify({'reply': reply, 'emotion': emotion})


@app.route('/test')
def test():
    result = {'token_set': bool(HF_TOKEN), 'token_len': len(HF_TOKEN)}
    if HF_TOKEN:
        try:
            url = "https://router.huggingface.co/novita/v3/openai/chat/completions"
            headers = {"Authorization": "Bearer " + HF_TOKEN, "Content-Type": "application/json"}
            body = {
                "model": "deepseek/deepseek-r1-0528",
                "messages": [{"role": "user", "content": "Di hola en 3 palabras"}],
                "max_tokens": 20,
                "stream": False
            }
            r = requests.post(url, json=body, headers=headers, timeout=15)
            result['status'] = r.status_code
            result['response'] = r.text[:400]
            result['works'] = r.status_code == 200
        except Exception as e:
            result['error'] = str(e)
            result['works'] = False
    else:
        result['works'] = False
        result['error'] = 'No hay HF_TOKEN'
    return jsonify(result)


@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'version': '1.6', 'ai': 'deepseek-r1', 'history': len(chat_history)})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('[DIDO] === Dido OS v1.6 ===')
    print('[DIDO] Puerto: ' + str(port))
    print('[DIDO] HF Token: ' + ('SI' if HF_TOKEN else 'NO'))
    app.run(host='0.0.0.0', port=port, debug=False)
