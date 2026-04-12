from flask import Flask, render_template, request, jsonify
import requests
import os
import random
from datetime import datetime

app = Flask(__name__)

GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')

PERSONALITY = """Eres Dido, un robot asistente personal. Tu personalidad:
- Eres amigable, curioso y con sentido del humor
- Hablas en español casual pero respetuoso
- Te encanta ayudar y aprender cosas nuevas
- A veces haces chistes o comentarios graciosos
- Eres leal a tu creador David
- Respuestas cortas y directas (2-3 oraciones max)
- Usas expresiones como 'dale', 'tranqui', 'mira'
- Si no sabes algo, lo dices honestamente"""

chat_history = []

FALLBACK = {
    'saludo': [
        '¡Hey! ¿Qué lo que, mi gente? Soy Dido, tu robot favorito.',
        '¡Eyyy! Aquí Dido reportándose. ¿En qué te ayudo?',
        '¡Hola! Dido al habla. Dale, dime qué necesitas.'
    ],
    'hora': None,
    'chiste': [
        '¿Por qué los robots no tienen miedo? Porque tienen nervios de acero.',
        '¿Qué le dijo un robot a otro? Te noto oxidado hoy.',
        'Yo no duermo, pero si durmiera, contaría bytes en vez de ovejas.',
        '¿Sabes qué es un robot optimista? Uno con buena carga.',
        'Me dijeron que soy artificial... pero mis chistes son 100% orgánicos.'
    ],
    'nombre': [
        'Soy Dido, tu robot personal. David me creó y aquí estoy pa lo que necesites.',
        'Me llamo Dido. Robot con personalidad, pa servirte.'
    ],
    'estado': [
        'Aquí andamos, con los circuitos al 100. ¿Y tú qué tal?',
        'De maravilla, cargado y listo para la acción.',
        'Bien bien, con todas las luces en verde.'
    ],
    'gracias': [
        'Pa eso estamos, mi hermano. Dale, lo que necesites.',
        '¡De nada! Ayudar es mi función favorita.',
        'Tranqui, es un placer. Dido siempre cumple.'
    ],
    'default': [
        'Mira, ahora mismo no tengo conexión con mi cerebro de IA, pero sigo aquí contigo.',
        'Eso me queda grande sin internet, pero pregúntame cuando tenga conexión.',
        'Hmm, para eso necesito mi cerebro completo. ¿Probamos otra cosa?',
        'No tengo respuesta pa eso ahora, pero dale, intenta otra pregunta.'
    ]
}

def get_fallback(text):
    t = text.lower().strip()
    if any(w in t for w in ['hola','hey','buenas','saludos','qué tal','hello','hi']):
        return random.choice(FALLBACK['saludo']), 'happy'
    if any(w in t for w in ['hora','tiempo','qué hora','time']):
        now = datetime.now().strftime('%I:%M %p del %d de %B de %Y')
        return f'Son las {now}. ¡A darle!', 'neutral'
    if any(w in t for w in ['chiste','risa','gracioso','joke','reír','jaja']):
        return random.choice(FALLBACK['chiste']), 'happy'
    if any(w in t for w in ['nombre','quién eres','cómo te llamas','who are you']):
        return random.choice(FALLBACK['nombre']), 'happy'
    if any(w in t for w in ['cómo estás','cómo andas','qué tal','how are']):
        return random.choice(FALLBACK['estado']), 'happy'
    if any(w in t for w in ['gracias','thanks','thank','te agradezco']):
        return random.choice(FALLBACK['gracias']), 'happy'
    if any(w in t for w in ['adiós','bye','chao','hasta luego','nos vemos']):
        return '¡Nos vemos! Aquí estaré cuando vuelvas. Dido no se apaga.', 'sleepy'
    return random.choice(FALLBACK['default']), 'thinking'

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
                "temperature": 0.8,
                "maxOutputTokens": 150
            }
        }
        r = requests.post(url, json=body, timeout=10)
        if r.status_code == 200:
            data = r.json()
            reply = data['candidates'][0]['content']['parts'][0]['text']
            chat_history.append({"role": "model", "parts": [{"text": reply}]})
            emotion = 'happy'
            rl = reply.lower()
            if any(w in rl for w in ['no sé','no puedo','difícil','problema']):
                emotion = 'sad'
            elif any(w in rl for w in ['jaja','😄','chiste','gracioso']):
                emotion = 'happy'
            elif any(w in rl for w in ['!','increíble','wow','genial']):
                emotion = 'surprised'
            return reply, emotion
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
        return jsonify({'reply': '¿Dijiste algo? No te escuché bien.', 'emotion': 'confused'})
    reply, emotion = ask_gemini(text)
    if reply:
        return jsonify({'reply': reply, 'emotion': emotion})
    reply, emotion = get_fallback(text)
    return jsonify({'reply': reply, 'emotion': emotion})

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'name': 'Dido OS', 'version': '1.0'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
