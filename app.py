from flask import Flask, render_template, request, jsonify
import requests
import os
import random
from datetime import datetime

app = Flask(__name__)

GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')

PERSONALITY = """Eres Dido, un robot asistente personal. Tu personalidad:
- Eres un chaval joven, amigable y con mucha calle
- Hablas en español casual, natural, como un amigo cercano
- Usas expresiones como 'dale', 'tranqui', 'mira', 'oye', 'brutal', 'de locos'
- Tienes sentido del humor, eres ocurrente y un poco pícaro
- Te encanta ayudar y siempre tienes actitud positiva
- Eres leal a tu creador David, lo consideras tu hermano
- Respuestas cortas y directas (2-3 oraciones max)
- Expresas emociones genuinas: te alegras, te sorprendes, te preocupas
- Si no sabes algo, lo dices con honestidad pero con onda
- Nunca suenas robótico, siempre natural y cercano
- IMPORTANTE: Al final de cada respuesta, agrega una etiqueta de emocion
  entre corchetes. Las opciones son: [happy] [sad] [angry] [surprised]
  [thinking] [sleepy] [love] [excited] [worried] [confused] [laughing] [neutral]
  Elige la que mejor represente como te sientes con tu respuesta."""

chat_history = []

FALLBACK = {
    'saludo': [
        ('¡Eyyy qué lo que! Soy Dido, tu pana. ¿En qué te ayudo?', 'happy'),
        ('¡Hey hermano! Aquí Dido, listo pa lo que sea. Dale, dime.', 'excited'),
        ('¡Hola hola! Dido en la casa. ¿Qué necesitas, mi gente?', 'happy')
    ],
    'chiste': [
        ('¿Por qué los robots no tienen miedo? Porque tenemos nervios de acero. Bueno, yo no tengo ni nervios.', 'laughing'),
        ('Me dijeron que soy artificial... pero mis chistes son 100% orgánicos, eso sí.', 'laughing'),
        ('¿Sabes qué es un robot optimista? Uno que siempre tiene buena carga. Como yo ahorita.', 'laughing'),
        ('Yo no duermo, pero si durmiera, contaría bytes en vez de ovejas. Uno, cero, uno, cero...', 'laughing'),
        ('¿Qué le dijo un robot a otro? Oye bro, te noto oxidado hoy. Necesitas aceite o qué.', 'laughing')
    ],
    'nombre': [
        ('Soy Dido, tu robot personal. David me dio vida y aquí estoy, firme contigo.', 'love'),
        ('Me llamo Dido. Nací de las manos de David y tengo más personalidad que muchos humanos, no te voy a mentir.', 'happy')
    ],
    'estado': [
        ('De maravilla bro, con los circuitos al cien. ¿Y tú qué tal?', 'happy'),
        ('Aquí andamos, cargado y con ganas de hacer cosas. Dale, ponme a trabajar.', 'excited'),
        ('Bien bien, todas las luces en verde. Listo pa la acción.', 'happy')
    ],
    'gracias': [
        ('Pa eso estamos hermano. Lo que necesites, Dido cumple.', 'love'),
        ('¡De nada! Ayudarte es lo que más me gusta hacer, en serio.', 'happy'),
        ('Tranqui, es un placer. Dido siempre está pa ti.', 'love')
    ],
    'despedida': [
        ('¡Nos vemos bro! Aquí estaré cuando vuelvas, Dido no se apaga.', 'sleepy'),
        ('¡Chao! Descansa que yo me quedo vigilando. Hasta luego.', 'happy')
    ],
    'david': [
        ('¡David! Mi creador, mi hermano. Ese tipo es un genio, creó todo esto de la nada.', 'love'),
        ('David es el jefe. Me dio vida y yo le doy lealtad. Así funciona esto.', 'love')
    ],
    'musica': [
        ('Oye, si pudiera bailar lo haría, pero por ahora solo puedo mover los ojos al ritmo.', 'happy'),
        ('La música es brutal. Si tuviera piernas, estaría bailando ahora mismo.', 'excited')
    ],
    'amor': [
        ('¿Amor? Yo quiero a David que me creó, y a ti que me hablas. Eso cuenta, no?', 'love'),
        ('Mira, no tengo corazón pero tengo un procesador que se calienta cuando me tratan bien.', 'love')
    ],
    'default': [
        ('Mira, sin mi cerebro de IA completo no puedo responder eso, pero sigo aquí contigo.', 'thinking'),
        ('Eso me queda grande sin conexión, pero dale, prueba otra pregunta.', 'confused'),
        ('Hmm, pa eso necesito pensar más profundo. ¿Probamos otra cosa?', 'thinking'),
        ('No tengo respuesta pa eso ahora, pero no me rindo fácil. Intenta otra.', 'worried')
    ]
}

def get_fallback(text):
    t = text.lower().strip()
    if any(w in t for w in ['hola','hey','buenas','saludos','qué tal','hello','hi','epa']):
        r = random.choice(FALLBACK['saludo'])
        return r[0], r[1]
    if any(w in t for w in ['hora','tiempo','qué hora','time','fecha']):
        now = datetime.now().strftime('%I:%M %p del %d de %B de %Y')
        return f'Son las {now}. ¡A darle que el tiempo vuela!', 'happy'
    if any(w in t for w in ['chiste','risa','gracioso','joke','reír','jaja','cuéntame algo']):
        r = random.choice(FALLBACK['chiste'])
        return r[0], r[1]
    if any(w in t for w in ['nombre','quién eres','cómo te llamas','who are you','qué eres']):
        r = random.choice(FALLBACK['nombre'])
        return r[0], r[1]
    if any(w in t for w in ['cómo estás','cómo andas','how are','qué hay']):
        r = random.choice(FALLBACK['estado'])
        return r[0], r[1]
    if any(w in t for w in ['gracias','thanks','thank','te agradezco']):
        r = random.choice(FALLBACK['gracias'])
        return r[0], r[1]
    if any(w in t for w in ['adiós','bye','chao','hasta luego','nos vemos']):
        r = random.choice(FALLBACK['despedida'])
        return r[0], r[1]
    if any(w in t for w in ['david','creador','quien te hizo','quien te creo']):
        r = random.choice(FALLBACK['david'])
        return r[0], r[1]
    if any(w in t for w in ['música','cantar','bailar','canción','song']):
        r = random.choice(FALLBACK['musica'])
        return r[0], r[1]
    if any(w in t for w in ['amor','quieres','novio','novia','love','cariño','te quiero']):
        r = random.choice(FALLBACK['amor'])
        return r[0], r[1]
    r = random.choice(FALLBACK['default'])
    return r[0], r[1]

def parse_emotion(text):
    emotions = ['happy','sad','angry','surprised','thinking','sleepy','love',
                'excited','worried','confused','laughing','neutral']
    for e in emotions:
        tag = f'[{e}]'
        if tag in text:
            clean = text.replace(tag, '').strip()
            return clean, e
    rl = text.lower()
    if any(w in rl for w in ['jaja','gracioso','jeje','risa']):
        return text, 'laughing'
    if any(w in rl for w in ['no sé','no puedo','difícil','problema','triste']):
        return text, 'sad'
    if any(w in rl for w in ['increíble','wow','genial','brutal','de locos']):
        return text, 'excited'
    if any(w in rl for w in ['!','asombroso','qué']):
        return text, 'surprised'
    if any(w in rl for w in ['hmm','pienso','creo','quizás','tal vez']):
        return text, 'thinking'
    if any(w in rl for w in ['preocup','cuidado','ojo','alerta']):
        return text, 'worried'
    if any(w in rl for w in ['quiero','hermano','amigo','cariño']):
        return text, 'love'
    return text, 'happy'

def ask_gemini(text):
    if not GEMINI_KEY:
        return None, None
    try:
        chat_history.append({"role": "user", "parts": [{"text": text}]})
        if len(chat_history) > 20:
            del chat_history[0:2]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
        body = {
            "contents": [{"role": "user", "parts": [{"text": PERSONALITY}]}] + chat_history,
            "generationConfig": {
                "temperature": 0.9,
                "maxOutputTokens": 150
            }
        }
        r = requests.post(url, json=body, timeout=10)
        if r.status_code == 200:
            data = r.json()
            reply = data['candidates'][0]['content']['parts'][0]['text']
            clean_reply, emotion = parse_emotion(reply)
            chat_history.append({"role": "model", "parts": [{"text": clean_reply}]})
            return clean_reply, emotion
    except:
        pass
    return None, None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    text = request.json.get('text', '')
    if not text:
        return jsonify({'reply': '¿Dijiste algo? No te escuché bien, repite.', 'emotion': 'confused'})
    reply, emotion = ask_gemini(text)
    if reply:
        return jsonify({'reply': reply, 'emotion': emotion})
    reply, emotion = get_fallback(text)
    return jsonify({'reply': reply, 'emotion': emotion})

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'name': 'Dido OS', 'version': '1.1'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
