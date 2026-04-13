from flask import Flask, render_template, request, jsonify
import requests
import os
import random
from datetime import datetime

app = Flask(__name__)

HF_TOKEN = os.environ.get('HF_TOKEN', '')

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
        ('Hey hermano! Aqui Dido, listo pa lo que sea.', 'excited'),
        ('Que bola! Dido reportandose. Dime en que te ayudo.', 'excited')
    ],
    'chiste': [
        ('Por que los robots no tienen miedo? Porque tenemos nervios de acero.', 'laughing'),
        ('Me dijeron que soy artificial pero mis chistes son organicos.', 'laughing'),
        ('Yo no duermo, pero si durmiera, contaria bytes en vez de ovejas.', 'laughing'),
        ('Un robot entra a un bar y pide aceite con hielo. El bartender dice eso no existe.', 'laughing'),
        ('Como se despide un robot? Hasta la vista baby. No mentira, yo digo chao bro.', 'laughing')
    ],
    'nombre': [
        ('Soy Dido, tu asistente con IA. David me creo y aqui estoy pa ti.', 'love'),
        ('Me llamo Dido. David me dio vida y tengo mas personalidad que muchos.', 'happy')
    ],
    'estado': [
        ('De maravilla bro, circuitos al cien. Y tu que tal?', 'happy'),
        ('Brutal hermano, con toda la energia. En que te ayudo?', 'excited')
    ],
    'gracias': [
        ('Pa eso estamos hermano. Dido siempre cumple.', 'love'),
        ('De nada! Ayudarte es lo que mas me gusta.', 'happy')
    ],
    'despedida': [
        ('Nos vemos bro! Aqui estare cuando vuelvas.', 'love'),
        ('Chao! Fue buena la charla. Vuelve cuando quieras.', 'happy')
    ],
    'david': [
        ('David! Mi creador, mi hermano. Ese tipo es un genio.', 'love'),
        ('David es el jefe. Me dio vida y yo le doy lealtad total.', 'love')
    ],
    'default': [
        ('Buena pregunta bro. Ahora mismo mi cerebro esta offline, pero preguntame otra cosa.', 'thinking'),
        ('Esa no la tengo clara ahora. Prueba con otro tema y te ayudo.', 'thinking'),
        ('Mi conexion al cerebro fallo. Pero dale, intenta otra pregunta.', 'worried'),
        ('Mmm no me llego la info. Preguntame de ciencia, historia o un chiste.', 'thinking')
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


def build_prompt(text):
    history_text = ''
    last_msgs = chat_history[-20:]
    for msg in last_msgs:
        if msg['role'] == 'user':
            history_text += 'Usuario: ' + msg['text'] + '\n'
        else:
            history_text += 'Dido: ' + msg['text'] + '\n'
    
    prompt = PERSONALITY + '\n\n'
    if history_text:
        prompt += 'Conversacion anterior:\n' + history_text + '\n'
    prompt += 'Usuario: ' + text + '\nDido:'
    return prompt


def ask_huggingface(text):
    if not HF_TOKEN:
        print('[DIDO] No hay HF_TOKEN')
        return None, None
    try:
        chat_history.append({'role': 'user', 'text': text})
        if len(chat_history) > 30:
            del chat_history[0:2]

        prompt = build_prompt(text)

        url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct"

        headers = {
            "Authorization": "Bearer " + HF_TOKEN,
            "Content-Type": "application/json"
        }

        body = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.8,
                "top_p": 0.9,
                "return_full_text": False,
                "stop": ["Usuario:", "\nUsuario"]
            }
        }

        r = requests.post(url, json=body, headers=headers, timeout=15)
        print('[DIDO] HF status: ' + str(r.status_code))
        print('[DIDO] HF response: ' + r.text[:500])

        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                reply = data[0].get('generated_text', '').strip()
                if reply:
                    reply = reply.split('Usuario:')[0].strip()
                    reply = reply.split('\nUsuario')[0].strip()
                    if reply.startswith('Dido:'):
                        reply = reply[5:].strip()
                    clean_reply, emotion = parse_emotion(reply)
                    if len(clean_reply) > 5:
                        chat_history.append({'role': 'assistant', 'text': clean_reply})
                        print('[DIDO] OK: ' + clean_reply[:100])
                        return clean_reply, emotion
                    else:
                        print('[DIDO] Respuesta muy corta: ' + repr(reply))
                else:
                    print('[DIDO] Respuesta vacia')
            else:
                print('[DIDO] Formato inesperado: ' + str(type(data)))
        elif r.status_code == 503:
            print('[DIDO] Modelo cargando, reintentando...')
            import time
            time.sleep(3)
            r2 = requests.post(url, json=body, headers=headers, timeout=20)
            print('[DIDO] Reintento status: ' + str(r2.status_code))
            if r2.status_code == 200:
                data = r2.json()
                if isinstance(data, list) and len(data) > 0:
                    reply = data[0].get('generated_text', '').strip()
                    if reply:
                        reply = reply.split('Usuario:')[0].strip()
                        if reply.startswith('Dido:'):
                            reply = reply[5:].strip()
                        clean_reply, emotion = parse_emotion(reply)
                        if len(clean_reply) > 5:
                            chat_history.append({'role': 'assistant', 'text': clean_reply})
                            return clean_reply, emotion
        else:
            print('[DIDO] Error: ' + str(r.status_code))

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
        return jsonify({'reply': 'No te escuche, repite porfa.', 'emotion': 'confused'})

    print('[DIDO] ===== INPUT: ' + text + ' =====')

    reply, emotion = ask_huggingface(text)
    if reply:
        print('[DIDO] Usando IA')
        return jsonify({'reply': reply, 'emotion': emotion})

    print('[DIDO] Usando FALLBACK')
    reply, emotion = get_fallback(text)
    return jsonify({'reply': reply, 'emotion': emotion})


@app.route('/test')
def test():
    result = {'hf_token_set': bool(HF_TOKEN), 'token_length': len(HF_TOKEN)}
    if HF_TOKEN:
        try:
            url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct"
            headers = {"Authorization": "Bearer " + HF_TOKEN}
            body = {"inputs": "Di hola en una palabra:", "parameters": {"max_new_tokens": 10, "return_full_text": False}}
            r = requests.post(url, json=body, headers=headers, timeout=15)
            result['status_code'] = r.status_code
            result['response'] = r.text[:300]
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
    return jsonify({'status': 'ok', 'version': '1.5', 'ai': 'huggingface', 'history': len(chat_history)})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('[DIDO] === Dido OS v1.5 ===')
    print('[DIDO] Puerto: ' + str(port))
    print('[DIDO] HF Token: ' + ('SI' if HF_TOKEN else 'NO'))
    app.run(host='0.0.0.0', port=port, debug=False)
