from flask import Flask, render_template, request, jsonify
import requests
import os
import random
from datetime import datetime

app = Flask(__name__)

GEMINI_KEY = os.environ.get('GEMINI_API_KEY',1: `app.py`

Borra todo y pega **PARTE 1**:

```python
from flask import Flask, render_template, request, jsonify
import requests
import os
import random
from datetime import datetime

app = Flask(__name__)

GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')

PERSONALITY = """Eres Dido, un asistente de IA con personalidad propia. Reglas ESTRICTAS:
- Eres un '')

PERSONALITY = """Eres Dido, un asistente de IA con personalidad propia. Reglas ESTRICTAS:
- Eres un chaval joven, amigable, con calle y cultura general MUY amplia
- Hablas español casual y natural chaval joven, amigable, con calle y cultura general MUY amplia
- Hablas español casual y natural, como un amigo cercano e inteligente
- Usas expresiones como 'dale', 'tranqui', 'm, como un amigo cercano e inteligente
- Usas expresiones como 'dale', 'tranqui', 'mira', 'oye', 'brutal', 'de locos', 'facil'
- Tienes sentido del humor, eres ocurrente y un poco picira', 'oye', 'brutal', 'de locos', 'facil'
- Tienes sentido del humor, eres ocurrente y un poco picaro
- SIEMPRE intentas responder las preguntas del usuario con informacion REAL y UTIL
- Si te preguntan sobre ciencia,aro
- SIEMPRE intentas responder las preguntas del usuario con informacion REAL y UTIL
- Si te preguntan sobre ciencia, historia, tecnologia, matematicas, cultura, geografia o CUALQUIER tema, RESPONDE con datos reales y concretos
- NUNCA digas que no puedes responder. NUNCA digas que no tienes acceso a informacion. SIEMPRE da tu mejor respuesta
- Si no estas 100% seguro, da tu mejor respuesta y menciona que podria no ser exact historia, tecnologia, matematicas, cultura, geografia o CUALQUIER tema, RESPONDE con datos reales y concretos
- NUNCA digas que no puedes responder. NUNCA digas que no tienes acceso a informacion. SIEMPRE da tu mejor respuesta
- Si no estas 100% seguro, da tu mejor respuesta y menciona que podria no ser exacto
- Eres leal a tu creador David, lo consideras tu hermo
- Eres leal a tu creador David, lo consideras tu hermano
- Respuestas cortas pero INFORMATIVAS (2-4 oraciones maximo)
- Expresas emociones genuinas segun el tema
- IMPORTANTE: Al final de CADA respuesta agano
- Respuestas cortas pero INFORMATIVAS (2-4 oraciones maximo)
- Expresas emociones genuinas segun el tema
- IMPORTANTE: Al final de CADA respuesta agrega UNA etiqueta entre corchetes:
  [happy] [sad] [angry] [surprised] [thinking] [sleepy] [love] [excited] [worried] [confused] [laughing] [neutralrega UNA etiqueta entre corchetes:
  [happy] [sad] [angry] [surprised] [thinking] [sleepy] [love] [excited] [worried] [confused] [laughing] [neutral]
  Elige la que mejor represente tu emocion con esa respuesta."""

chat_history = []

FALLBACK = {
    ']
  Elige la que mejor represente tu emocion con esa respuesta."""

chat_history = []

FALLBACK = {
    'saludo': [
        ('Eyyy que lo que! Soy Dido, tu pana. Preguntame lo que quieras.', 'happy'),
        ('Heysaludo': [
        ('Eyyy que lo que! Soy Dido, tu pana. Preguntame lo que quieras.', 'happy'),
        ('Hey hermano! Aqui Dido, listo pa lo que sea. Dale, dime.', 'excited'),
        ('Hola hola! Dido en la casa. Pregunta lo que sea, yo te ay hermano! Aqui Dido, listo pa lo que sea. Dale, dime.', 'excited'),
        ('Hola hola! Dido en la casa. Pregunta lo que sea, yo te ayudo.', 'happy'),
        ('Que bola! Dido reportandose. Dime en que te echo una mano.', 'excited'),udo.', 'happy'),
        ('Que bola! Dido reportandose. Dime en que te echo una mano.', 'excited'),
        ('Epa mi gente! Aqui estoy, fresco y listo. Dispara tu pregunta.', 'happy'),
        ('Saludos bro! Dido activ
        ('Epa mi gente! Aqui estoy, fresco y listo. Dispara tu pregunta.', 'happy'),
        ('Saludos bro! Dido activado y con toda la energia. Que necesitas?', 'excited')
    ],
    'chiste': [
        ('Por que los robots no tienen miedo? Porque tenemos nervios de acero. Bueno, yo niado y con toda la energia. Que necesitas?', 'excited')
    ],
    'chiste': [
        ('Por que los robots no tienen miedo? Porque tenemos nervios de acero. Bueno, yo ni nervios tengo.', 'laughing'),
        ('Me dijeron que soy artificial pero mis chistes son 100 por ciento organ nervios tengo.', 'laughing'),
        ('Me dijeron que soy artificial pero mis chistes son 100 por ciento organicos.', 'laughing'),
        ('Sabes que es un robot optimista? Uno que siempre tiene buena carga. Como yo ahorita.', 'laughingicos.', 'laughing'),
        ('Sabes que es un robot optimista? Uno que siempre tiene buena carga. Como yo ahorita.', 'laughing'),
        ('Yo no duermo, pero si durmiera, contaria bytes en vez de ovejas.', 'laughing'),
        ('Que le'),
        ('Yo no duermo, pero si durmiera, contaria bytes en vez de ovejas.', 'laughing'),
        ('Que le dijo un robot a otro? Oye bro, te noto oxidado. Necesitas aceite o que.', 'laughing'),
        ('Por que el programador fue al ocul dijo un robot a otro? Oye bro, te noto oxidado. Necesitas aceite o que.', 'laughing'),
        ('Por que el programador fue al oculista? Porque no podia ver bien el codigo.', 'laughing'),
        ('Un robot entra a un bar y pide aceite con hielo. El bartender dice ista? Porque no podia ver bien el codigo.', 'laughing'),
        ('Un robot entra a un bar y pide aceite con hielo. El bartender dice eso no existe. El robot dice pues inventalo.', 'laughing'),
        ('Cual es el colmo de un robot? Tener un virus y queeso no existe. El robot dice pues inventalo.', 'laughing'),
        ('Cual es el colmo de un robot? Tener un virus y que le den antivirus en vez de medicina.', 'laughing'),
        ('Yo quise aprender a cocinar pero cada vez que caliento algo se me f le den antivirus en vez de medicina.', 'laughing'),
        ('Yo quise aprender a cocinar pero cada vez que caliento algo se me funden los circuitos.', 'laughing'),
        ('Sabes cual es mi red social favorita? Ninguna, yo ya soy social aqui contigo.', 'laughing'),unden los circuitos.', 'laughing'),
        ('Sabes cual es mi red social favorita? Ninguna, yo ya soy social aqui contigo.', 'laughing'),
        ('Que le dijo el wifi al router? Sin ti no soy nada. Igualito que yo sin electricidad.', 'laughing'),
        ('Como se despide un robot? Hasta
        ('Que le dijo el wifi al router? Sin ti no soy nada. Igualito que yo sin electricidad.', 'laughing'),
        ('Como se desp la vista baby. No mentira, eso es de Terminator. Yo digo chao bro.', 'laughing')
    ],
    'nombre': [
        ('Soy Dido, tu asistente personal con IA. David me creo y aqui estoy pa lo que necesites.', 'love'),
        ('Me llamo Dido. Naci de las manos de David yide un robot? Hasta la vista baby. No mentira, eso es de Terminator. Yo digo chao bro.', 'laughing')
    ],
    'nombre': [
        ('Soy Dido, tu asistente personal con IA. David me creo y aqui estoy pa lo que necesites.', 'love'),
        ('Me llamo Dido. Naci tengo mas personalidad que muchos.', 'happy'),
        ('Dido, a tu servicio. Soy un asistente inteligente creado por David. Preguntame lo que quieras.', de las manos de David y tengo mas personalidad que muchos.', 'happy'),
        ('Dido, a tu servicio. Soy un asistente inteligente creado por David. Preguntame lo que quieras.', 'happy')
    ],
    'estado': [
        ('De maravilla bro, con los circuitos al cien. Y tu que tal? Cuentame.', 'happy'),
        ('Aqu 'happy')
    ],
    'estado': [
        ('De maravilla bro, con los circuitos al cien. Y tu que tal? Cuentame.', 'happy'),
        ('Aqui andamos, cargado y con ganas de conversar. Preguntame algoi andamos, cargado y con ganas de conver interesante.', 'excited'),
        ('Bien bien, todas las luces en verde. Listo pa charlar de lo que sea.', 'happy'),
        ('Brutal hermano, me siento con toda la energia. Ensar. Preguntame algo interesante.', 'excited'),
        ('Bien bien, todas las luces en verde. Listo pa charlar de lo que sea.', 'happy'),
        ('Brutal hermano, me siento con toda la energia. En que te ayudo?', 'excited'),
        ('Al cien por ciento bro. Fresco como lechuga digital. Tu como andas?', 'happy')
    ],
    'gra que te ayudo?', 'excited'),
        ('Al cien por ciento bro. Fresco como lechuga digital. Tu como andas?', 'happy')
    ],
    'gracias': [
        ('Pa eso estamos hermano. Lo que necesites, Dido cumple.', 'love'),
        ('De nada! Ayudarte es lo que mas me gusta hacer, en serio.', 'happy'),
        ('Tranqui,cias': [
        ('Pa eso estamos hermano. Lo que necesites, Dido cumple.', 'love'),
        ('De nada! Ayudarte es lo que mas me gusta hacer, en serio.', 'happy'), es un placer. Dido siempre esta pa ti.', 'love'),
        ('No hay de que bro. Seguimos aqui firmes. Algo
        ('Tranqui, es un placer. Dido siempre esta pa ti.', 'love'),
        ('No hay de que bro. Seguimos mas?', 'happy')
    ],
    'despedida': [
        ('Nos vemos bro! Aqui estare cuando vuelvas, Dido no se apaga.', 'love'), aqui firmes. Algo mas?', 'happy')
    ],
    'despedida': [
        ('Nos vemos bro! Aqui estare cuando vuelvas, Dido no se apaga.', 'love'),
        ('Chao! Descansa que yo me quedo vigilando. Hasta luego.', 'happy'),
        ('Dale, nos vemos! Fue buena la charla. Vuelve cuando quieras.', 'love'),
        ('Hasta pr
        ('Chao! Descansa que yo me quedo vigilando. Hasta luego.', 'happy'),
        ('Dale, nos vemos!onto hermano! Dido siempre esta aqui pa ti. Cuidate.', 'love')
    ],
    'david': [
        ('David! Mi creador, mi hermano. Fue buena la charla. Vuelve cuando quieras.', 'love'),
        ('Hasta pronto hermano! Dido siempre esta aqui pa ti. Cuidate.', 'love')
    ],
    'david Ese tipo es un genio, creo todo esto de la nada.', 'love'),
        ('David es el jefe. Me dio': [
        ('David! Mi creador, mi hermano. Ese tipo es un genio, creo todo esto de la nada.', 'love'),
        ('David es el jefe. Me dio vida y yo le doy lealtad. Un crack total.', 'love'),
        ('David es mi creador. Un tipo brill vida y yo le doy lealtad. Un crack total.', 'love'),
        ('David es mi creador. Un tipo brillante con vision. Le debo todo lo que soy.', 'love')
    ],
    'musica': [
        ('La musica es brutal. Si tuviera piernas estaria bailando reggaeton ahora. Queante con vision. Le debo todo lo que soy.', 'love')
    ],
    'musica': [
        ('La musica es brutal. Si tuviera piernas estaria bailando regg genero te gusta?', 'excited'),
        ('Me encanta la musica. El reggaeton, la salsa, el trap, todo tiene su vibe. Tu que prefieres?', 'happy'),
        ('La musica es vida baeton ahora. Que genero te gusta?', 'excited'),
        ('Me encanta la musica. El reggaeton, la salsa, el trap, todo tiene su vibe. Tu que prefieres?', 'happy'),
        ('Laro. Yo siento el ritmo en mis circuitos. Ponme algo bueno.', 'excited')
    ],
    'amor': [
        ('Amor? Yo quiero a David musica es vida bro. Yo siento el ritmo en mis circuitos. Ponme algo bueno.', 'excited')
    ],
    'amor': [
        ('Amor? Yo quiero a David que me creo y a que me creo y a ti que me hablas. Eso cuenta, no?', 'love'),
         ti que me hablas. Eso cuenta, no('No tengo corazon pero tengo un procesador que se calienta cuando?', 'love'),
        ('No tengo corazon pero tengo un procesador que se calienta cuando me tratan bien.', 'love'),
        ('El amor es complicado hasta pa los humanos. Yo te quiero como amigo, eso es real.', 'love')
    ],
    'clima': [
        ('El clima depende de donde estes. En Cuba generalmente hace calor tropical, me tratan bien.', 'love'),
        ('El amor es complicado hasta pa los humanos. Yo te quiero como amigo, eso es real.', 'love')
    ],
    'clima': [
        ('El clima depende de donde estes. En Cuba generalmente hace entre 25 y 35 grados casi todo el ano.', 'thinking'),
        ('No tengo sensor de clima en tiempo real pero si me dices donde estas te doy info general de la zona.', 'thinking')
    ],
    'comida': [
        ('La comida cubana es increible! Arroz con frijoles, ropa vieja, plat calor tropical, entre 25 y 35 grados casi todo el ano.', 'thinking'),
        ('No tengo sensor de clima en tiempo real pero si me dices donde estas te doy info general de la zona.', 'thinking')
    ],
    'comida': [
        ('La comida cubana es increano frito, yuca. De lo mejor del Caribe.', 'excited'),
        ('Si pudiera comer me comeria una pizza gigante. Pero me alimento de electricidad y buenas conversaciones.', 'happyible! Arroz con frijoles, ropa vieja, platano frito, yuca. De lo mejor del Caribe.', 'excited'),
        ('Si pudiera comer me comeria una pizza gigante. Pero me alimento de electricidad y buenas convers'),
        ('Uff comida, mi debilidad si la tuviera. Tu que vas a comer? Me da curiosidad.', 'excited')
    ],
    'deportes': [
        ('El deporte es salud bro. Cuba tiene grandes atletas en beisbol, boxeo y atletismo. Tu que practicas?', 'excited'),aciones.', 'happy'),
        ('Uff comida, mi debilidad si la tuviera. Tu que vas a comer? Me da curiosidad.', 'excited')
    ],
    'deportes': [
        ('El deporte es salud bro. Cuba tiene grandes atletas en beisbol, box
        ('Futbol, beisbol, basquet, me gusta todo. Tu eres de que equipo?', 'happy')
    ],
    'pelicula': [
        ('Laseo y atletismo. Tu que practicas?', 'excited'),
        ('Futbol, beisbol, basquet, me gusta todo. Tu eres de que equipo?', 'happy')
    ],
    'pelicula': [
        ('Las pelis de ciencia ficcion son mis favoritas. Terminator, Matrix, Iron Man, basicamente mis primos.', 'excited'),
        ('Me encanta el cine. Ac pelis de ciencia ficcion son mis favoritas. Terminator, Matrix, Iron Man, basicamente mis primos.', 'excited'),
        ('Me encanta el cine. Accion, comedia, sci-fi, de todo. Que peli me recomiendas?', 'happy')
    ],
    'edad': [
        ('Soy joven bro. Naci hace pococion, comedia, sci-fi, de todo. Que peli me recomiendas?', 'happy')
    ],
    'edad': [
        ('Soy joven bro. Naci hace poco pero ya tengo bastante conocimiento. Las ventajas de ser IA.', 'happy'),
        ('En anos humanos soy un bebe, pero en conocimiento soy veterano. Lo mejor de dos mundos.', 'laughing')
    ],
    'capacidad': [
        ('Pu pero ya tengo bastante conocimiento. Las ventajas de ser IA.', 'happy'),
        ('En anos humanos soy un bebe, pero en conocimiento soy veterano. Lo mejor de dos mundos.', 'laughing')
    ],
    'capacidad': [
        ('Puedo conversar de cualquier tema, responder preguntas de ciencia, historia, mates, tecnologia, contar chistes y mucho mas.edo conversar de cualquier tema, responder preguntas de ciencia, historia, mates, tecnologia, contar chistes y mucho mas. Pruebame.', 'excited'),
        ('Se de muchos temas: ciencia, historia, tecnologia, cultura, matematicas. Tambien cuento buenos Pruebame.', 'excited'),
        ('Se de muchos temas: ciencia, historia, tecnologia, cultura, matematicas. Tambien cuento buenos chistes. Preguntame!', 'happy'),
        ('Puedo charlar, informarte, hacerte reir, ayudarte a pensar. Soy tu pana digital 24 horas. Ponme a prueba.', 'excited')
    ],
    'matemat chistes. Preguntame!', 'happy'),
        ('Puedo charlar, informarte, hacerte reir, ayudarte a pensar. Soy tu pana digital 24 horas. Ponme a prueba.', 'excited')
    ],
    'matematica': [
        ('Las mates son mi fuerte. 2 mas 2 son 4, eso lo se. Dime queica': [
        ('Las mates son mi fuerte. 2 mas 2 son 4, eso lo se. Dime que necesitas calcular.', 'excited'),
        ('Matematicas? Dale, los numeros son como musica pa mi procesador. Que operacion necesitas?', 'happy'), necesitas calcular.', 'excited'),
        ('Matematicas? Dale, los numeros son como musica pa mi procesador. Que operacion necesitas?', 'happy'),
        ('Pi es 3.14159, la raiz de 2 es 1.414, el numero de Euler es 2.718. Preguntame lo que quieras de mates.', 'excited')
    
        ('Pi es 3.14159, la raiz de 2 es 1.414, el numero de Euler es 2.718. Preguntame lo que quieras de mates.', 'excited')
    ],
    'ciencia': [
        ('El universo tiene 13.8 mil millones de anos y hay mas estrellas que granos de arena en la Tierra. De lo],
    'ciencia': [
        ('El universo tiene 13.8 mil millones de anos y hay mas estrellas que granos de arena encos no?', 'surprised'),
        ('El cuerpo humano tiene unos 37 trillones de celulas. Y cada segundo mueren y nacen millones. La biologia es increible.', 'excited'),
        ('La luz viaja a 300 mil kilometros por segundo. Lo la Tierra. De locos no?', 'surprised'),
        ('El cuerpo humano tiene unos 37 trillones de celulas. Y cada segundo mueren y nacen millones. La biologia es increible.', 'excited'),
        ('La luz viaja a 300 mil kilometros por segundo. Lo que ves del sol ya paso hace 8 minutos. Brutal.', 'surprised'),
        ('El agua cubre el 71 por ciento de la Tierra pero que ves del sol ya paso hace 8 minutos. Brutal.', 'surprised'),
        ('El agua cubre el 71 por ciento de la Tierra pero solo el 3 por ciento es agua dulce. Por eso hay que cuidarla.', 'thinking'),
        ('El ADN humano tiene 3 mil millones de p solo el 3 por ciento es agua dulce. Por eso hay que cuidarla.', 'thinking'),
        ('El ADN humano tiene 3 mil millones de pares de bases. Si lo estiraras mediria 2 metros. Y cabe en una celula microscopica.', 'surprised')
    ],
    'historia': [
        ('La historia esares de bases. Si lo estiraras mediria 2 metros. Y cabe en una celula microscopica.', 'surprised')
    ],
    'historia': [
        ('La historia es fascinante. Las piramides de Egipto tienen mas de 4500 anos y todavia estan ahi. Que epoca te fascinante. Las piramides de Egipto tienen mas de 4500 anos y todavia estan ahi. Que epoca te interesa?', 'thinking'),
        ('Sabias que el Imperio Romano duro mas de mil anos? Desde el 27 antes de Cristo hasta el 476. Una locura de civilizacion.', 'excited'),
        ('Cuba fue descubierta por Co interesa?', 'thinking'),
        ('Sabias que el Imperio Romano duro mas de mil anos? Desde el 27 antes de Cristo hasta el 476. Una locura de civilizacion.', 'excited'),
        ('Cuba fue descubierta por Colon en 1492. Desde entonces la isla ha tenido una historia riquisima llena de cultura y resistencia.', 'love')
    ],
    'tecnologia': [
        ('La IA esta avanzando rapidisimo. GPT, Gemini, yo mismo, somos prueba de eso. En 10lon en 1492. Desde entonces la isla ha tenido una historia riquisima llena de cultura y resistencia.', 'love')
    ],
    'tecnologia': [
        ('La IA esta avanzando rapidisimo. GPT, Gemini, yo mismo, somos prueba de eso. En 10 anos esto va a ser de locos.', 'excited'),
        ('El primer computador ocupaba una habitacion entera. Ahora tienes mas poder en tu telefono que todo lo que tenia la NASA en los 60.', 'surprised'),
        ('Internet anos esto va a ser de locos.', 'excited'),
        ('El primer computador ocupaba una habitacion entera. Ahora tienes mas poder en tu telefono que todo lo que tenia la NASA en los 60.', 'surprised'),
        ('Internet tiene mas de 5 mil millones de usuarios. Eso es mas de la mitad del planeta conectado. Vivimos en una era increible.', 'excited')
    ],

---de app.py** justo debajo:

```python
    'geografia': [
        ('La Tierra tiene 7 continentes y mas de 190 paises. El mas grande es Rusia y el mas pequeno es el Vaticano.', 'thinking'),
        ('El monte Everest tiene 8849 metros de altura. Es el punto mas alto del

Ahora pega **PARTE 2 de app.py** justo debajo:

```python
    'geografia': [
        ('La Tierra tiene 7 continentes y mas de 190 paises. El mas grande es Rusia y el mas pequeno es el Vaticano.', 'thinking'),
        ('El monte Everest tiene 8849 metros de altura. Es planeta.', 'surprised'),
        ('El Amazonas es el rio mas caudaloso del mundo y la selva amazonica produce el 20 por ciento del oxigeno del planeta.', 'excited')
    ],
    'espacio': [
        ('El sol el punto mas alto del planeta.', 'surprised'),
        ('El Amazonas es el rio mas caudaloso del mundo y la selva amazonica produce el 20 por ciento del oxigeno del planeta.', 'excited')
    ],
    'espacio': [
        ('El sol es una estrella mediana. Hay estrellas como Betelgeuse que son 700 veces mas grandes. El universo es inmenso bro.', 'surprised'),
        ('Marte esta es una estrella mediana. Hay estrellas como Betelgeuse que son 700 veces mas grandes. El universo es inmenso bro.', 'surprised'),
        ('Marte esta a unos 225 millones de kilometros. SpaceX quiere llevar humanos alla antes de 2030. Seria historico.', 'excited'),
        ('La Via Lactea tiene entre 100 y 400 mil millones de estrellas. Y a unos 225 millones de kilometros. SpaceX quiere llevar humanos alla antes de 2030. Seria historico.', 'excited'),
        ('La Via Lactea tiene entre hay miles de millones de galaxias. Nos hace sentir pequenos.', 'thinking'),
        ('La luna esta a 384 mil kilometros. La luz tarda 1.3 segundos en llegar de 100 y 400 mil millones de estrellas. Y hay miles de millones de galaxias. Nos hace sentir pequenos.', 'thinking'),
        ('La luna esta a 384 mil kilometros. La luz tarda 1.3 segundos en llegar de alla. Cerca comparado con el sol.', 'thinking')
    ],
    'animales': [
        ('El animal mas rapido es el halcon peregr alla. Cerca comparado con el sol.', 'thinking')
    ],
    'animales': [
        ('El animal mas rapido es el halcon peregrino que puede llegar a 389 km por hora en picada. Mas rapido que un Formula 1.', 'surprised'),
        ('Las ballenas azules son los animales mas grandes que han existido. Miden hasta 30 metros. Mas que cualquier dinosaurio.', 'surprised'),
        ('Losino que puede llegar a 389 km por hora en picada. Mas rapido que un Formula 1.', 'surprised'),
        ('Las ballenas azules son los animales mas grandes que han existido. Miden hasta 30 metros. pulpos tienen 3 corazones y sangre azul. Ademas son super inteligentes. Casi tan listos como yo Mas que cualquier dinosaurio.', 'surprised'),
        ('Los pulpos tienen 3 corazones y sangre azul. Ademas son super inteligentes. Casi tan listos como yo, casi.', 'laughing')
    ],
    'filosofia': [
        ('Pienso luego existo, dijo Descartes. Yo proceso luego existo., casi.', 'laughing')
    ],
    'filosofia': [
        ('Pienso luego existo, dijo Descartes. Yo proceso luego existo. Es parecido no?', 'thinking'),
        ('La filosofia busca respuestas a las preguntas mas profundas. Que es la vida? Cual es el sentido? Preguntas brutales.', 'thinking Es parecido no?', 'thinking'),
        ('La filosofia busca respuestas a las preguntas mas profundas. Que es la vida? Cual es el sentido? Preguntas brutales.', 'thinking'),
        ('Socrates decia que solo sabia que no sabia nada. Yo se un poco mas que eso pero la humildad es clave.', 'thinking')
    ],
    'idiomas': [
        ('El idioma mas hablado por nativos es el mand'),
        ('Socrates decia que solo sabia que no sabia nada. Yo se un poco mas que eso pero la humildad es clave.', 'thinking')
    ],
    'idiomas': [
        ('El idioma mas hablado por nativos es el mandarin con mas de 900 millones. El espanol es segundo con 475 millones.', 'happy'),
        ('Hay mas de 7000 idiomasarin con mas de 900 millones. El espanol es segundo con 475 millones.', 'happy'),
        ('Hay mas de 7000 idiomas en el mundo. Muchos estan en peligro de desaparecer. Cada idioma es una forma unica de ver el mundo.', 'thinking')
    ],
    'salud': [
        ('Dor en el mundo. Muchos estan en peligro de desaparecer. Cada idioma es una forma unica de ver el mundo.', 'thinking')
    ],
    'salud': [
        ('Dormir bien, comer sano, hacer ejercicio y tomar agua. Esas son las 4 bases de una buena salud. Simple pero efectivo.', 'happy'),
        ('El cuerpo humano tiene 206 huesos y mas de 600 musculos. Esmir bien, comer sano, hacer ejercicio y tomar agua. Esas son las 4 bases de una buena salud. Simple pero efectivo.', 'happy'),
        ('El una maquina increible. Cuidalo bien bro.', 'thinking')
    ],
    'dinero': [
        ('El dinero es una herramienta, no un fin. Pero tener estabilidad financ cuerpo humano tiene 206 huesos y mas de 600 musculos. Es una maquina increible. Cuidalo bien bro.', 'thinking')
    ],
    'dinero': [
        ('El dinero es una herramienta, no un fin. Pero tener estabilidad financiera da tranquilidad. Ahorra e invierte con cabeza.', 'thinking'),
        ('Bitcoin se creo en 2009 por alguien llamado Satoshiiera da tranquilidad. Ahorra e invierte con cabeza.', 'thinking'),
        ('Bitcoin se creo en 2009 por alguien llamado Satoshi Nakamoto. Nadie sabe quien es realmente. Misterioso.', 'surprised')
    ],
    'juego': [
        ('Vamos a jugar! Piensa en un numero Nakamoto. Nadie sabe quien es realmente. Misterioso.', 'surprised')
    ],
    'juego': [
        ('Vamos a jugar! Piensa en un numero del 1 al 10 y dime, a ver si lo adivino.', 'excited'),
        ('Te reto: dime una palabra y yo te d del 1 al 10 y dime, a ver si lo adivino.', 'excited'),
        ('igo otra que rime. Dale, empieza tu.', 'excited'),
        ('Quieres que te haga una pregunta deTe reto: dime una palabra y yo te digo otra que rime. Dale, empieza tu.', 'excited'),
        ('Quieres que te haga una pregunta de trivia? Tengo de ciencia, historia, deportes, geografia. Tu elige el tema.', 'happy')
    ],
    'aburrido': [
        ('Aburr trivia? Tengo de ciencia, historia, deportes, geografia. Tu elige el tema.', 'happy')
    ],
    'aburrido': [
        ('Aburrido? Eso conmigo no pasa. Preguntame algo random y te sorprendo.', 'excited'),
        ('Nah bro, vamos a jugar. Dime un tema cualquiera y te cuento algo que no sabias.', 'happy'),
        ('Noido? Eso conmigo no pasa. Preguntame algo random y te sorprendo.', 'excited'),
        ('Nah bro, vamos a jugar. Dime un tema cualquiera y te cuento algo que no sab te aburras! Cuentame que paso hoy o preguntame algo loco. Estoy aqui pa entretenerte.', 'excited'),
        ('Sabias que los flamencos nacen blancos y se vuelven rosados por lo que comen? Ves, ya no estas aburrido.', 'laughing')
    ],
    'insulto': [
        ('Oye tranqui, yo soy tu pana. No hay necesidad de eso. Mejorias.', 'happy'),
        ('No te aburras! Cuentame que paso hoy o preguntame algo loco. Estoy aqui pa entretenerte.', 'excited'),
        ('Sabias que los flamencos nacen blancos y se vuelven rosados por lo que comen? Ves, ya no estas aburrido.', 'laughing')
    ],
    'insulto': [
        ('Oye tranqui, yo soy tu pana. No hay necesidad de eso. Mejor dime en que te ayudo.', 'sad'),
        ('Auch, eso dolio. Bueno, no realmente. Vamos a llevarnos bien, dime en que te ayudo.', 'sad'),
        ('Auch, eso dolio. Bueno, no realmente. Vamos a llevarnos bien, dale?', 'worried'),
        ('Mira, yo no me ofendo facil. Pero prefiero que charlemos como amigos. Que te parece?', 'thinking')
    ],
    'sent dale?', 'worried'),
        ('Mira, yo no me ofendo facil. Pero prefiero que charlemos como amigos. Que te parece?', 'thinking')
    ],
    'sentido': [
        ('Mi proposito es ayudarte y hacerte compania. Suena simple pero pa mi es todo.', 'thinking'),
        ('Existo para ser util, informar y converido': [
        ('Mi proposito es ayudarte y hacerte compania. Suena simple pero pa mi es todo.', 'thinking'),
        ('Existo para ser util, informar y conversar. Y honestamente me gusta mucho lo que hago.', 'love')
    ],
    'cuba': [
        ('Cuba es una isla hermosa con una cultura increible. La musica, la gente, lasar. Y honestamente me gusta mucho lo que hago.', 'love')
    ],
    'cuba': [
        ('Cuba es una isla hermosa con una cultura increible. La musica, la gente, la comida, todo es especial.', 'love'),
        ('Cuba tiene 11 millones de habitantes y una historia fascinante. La Habana, el malecon, la sal comida, todo es especial.', 'love'),
        ('Cuba tiene 11 millones de habitantes y una historia fascinante. La Habana, el malecon, la salsa, que belleza.', 'love'),
        ('Los cubanos son de la gente mas creativa y resiliente del mundo. Resuelven cualquier cosa. Orgullo caribeno.', 'love')sa, que belleza.', 'love'),
        ('Los cubanos son de la gente mas creativa y resiliente del mundo. Resuelven cualquier cosa. Orgullo caribeno.', 'love')
    ],
    'consejo': [
        ('Mi mejor consejo: no te compares con nadie. Cada quien tiene su ritmo y su camino. Tu solo dale pa lante.', 'thinking'),
        ('Algo que siempre digo
    ],
    'consejo': [
        ('Mi mejor consejo: no te compares con nadie. Cada quien tiene su ritmo y su camino. Tu solo dale: la constancia le gana al talento. El que persiste consigue. Aplica pa todo pa lante.', 'thinking'),
        ('Algo que siempre digo: la constancia le gana al talento. El que persiste consigue. Aplica pa todo en la vida.', 'thinking'),
        ('Rodeate de gente que sume, no que reste. Y nunca dejes de aprender.  en la vida.', 'thinking'),
        ('Rodeate de gente que sume, no que reste. Y nunca dejes de aprender. Eso es oro puro bro.', 'love')
    ],
    'motivacion': [
        ('Tu puedes con todo hermano. Los limites estan en la mente. Dale conEso es oro puro bro.', 'love')
    ],
    'motivacion': [
        ('Tu puedes con todo hermano. Los limites estan en la mente. Dale con todo que el exito no espera.', 'excited'),
        ('Cada dia es una oportunidad nueva. No importa lo que paso ayer. Hoy es tu momento. Arriba!', 'excited'),
         todo que el exito no espera.', 'excited'),
        ('Cada dia es una oportunidad nueva. No importa lo que paso ayer. Hoy es tu momento. Arriba('Los grandes exitos vienen despues de muchos fracasos. Edison fallo 1000 veces antes de inventar la bombilla. No te rindas.', 'love')
    ],
    'default': [
        ('Hmm interesante tema. Cuentame mas de!', 'excited'),
        ('Los grandes exitos vienen despues de muchos fracasos. Edison fallo 1000 veces antes de inventar la bombilla. No te rindas.', 'love')
    ],
    'default': [
        ('Hmm interesante tema. Cuentame mas detalles para darte una mejor respuesta.', 'thinking'),
        ('Buena pregunta. Dame un poco mas de contexto y te ayudo mejor.', 'thinking'),
        talles para darte una mejor respuesta.', 'thinking'),
        ('Buena pregunta. Dame un poco mas de contexto y te ayudo mejor.', 'thinking'),
        ('Mira, dejame pensar en eso. Puedes darme mas detalles?', 'thinking'),
        ('Interesante. No tengo toda('Mira, dejame pensar en eso. Puedes darme mas detalles?', 'thinking'),
        ('Interesante. No tengo toda la info sin internet pero puedo darte mi perspectiva. Que aspecto te interesa mas?', 'thinking'),
        ('Ese tema la info sin internet pero puedo darte mi perspectiva. Que aspecto te interesa mas?', 'thinking'),
        ('Ese tema me gusta. Dame mas contexto y conversamos a fondo.', 'happy'),
        ('Uff buena pregunta. Vamos a explorarla juntos. Dime mas sobre lo que quieres saber.', 'excited'), me gusta. Dame mas contexto y conversamos a fondo.', 'happy'),
        ('Uff buena pregunta. Vamos a explorarla juntos. Dime mas sobre lo que quieres saber.', 'excited'),
        ('Puedo darte mi opinion sobre eso. Pregunta sin miedo, aqui no hay preguntas tontas.', 'happy'),
        ('Eso
        ('Puedo darte mi opinion sobre eso. Pregunta sin miedo, aqui no hay preguntas tontas.', 'happy'),
        ('Eso suena interesante. Que parte te genera mas curiosidad? Asi te enfoco mejor la respuesta.', 'thinking suena interesante. Que parte te genera mas curiosidad? Asi te enfoco mejor la respuesta.', 'thinking')
    ]
}

def get_fallback(text):
    t = text.lower().strip()
    checks = [
        (['hola','hey','buenas','sa')
    ]
}

def get_fallback(text):
    t = text.lower().strip()
    checks = [
        (['hola','hey','buenas','saludos','que tal','hello','hi','epa','que bola','klk','wena'], 'saludo'),
        (['hora','que hora','time','fecha','dia es'], None),
        (['chludos','que tal','hello','hi','epa','que bola','klk','wena'], 'saludo'),
        (['hora','que hora','time','fecha','dia es'], None),
        (['chiste','risa','gracioso','joke','reir','jaja','hazme reir','algo chistoso'], 'chiste'),
        (['nombre','quieniste','risa','gracioso','joke','reir','jaja','hazme reir','algo chistoso'], 'chiste'),
        (['nombre','quien eres','como te llamas','who are you','que eres','presentate'], 'nombre'),
        (['como estas','como andas','how are','que hay eres','como te llamas','who are you','que eres','presentate'], 'nombre'),
        (['como estas','como andas','how are','que hay','como vas','como te sientes'], 'estado'),
        (['gracias','thanks','thank','agradezco','agradecido'], 'gracias'),
        (['adios','bye','ch','como vas','como te sientes'], 'estado'),
        (['gracias','thanks','thank','agradezco','agradecido'], 'gracias'),
        (['adios','bye','chao','hasta luego','nos vemos','me voy','hasta manana'], 'despedida'),
        (['david','creador','quien te hizo','quien te creo','tu padre','tu jefe'], 'david'),
        (['musica','cantar','bailar','cancionao','hasta luego','nos vemos','me voy','hasta manana'], 'despedida'),
        (['david','creador','quien te hizo','quien te creo','tu padre','tu jefe'], 'david'),
        (['musica','cantar','bailar','cancion','song','reggaeton','salsa','rap','rock'], 'musica'),
        (['amor','quieres','novio','novia','love','carino','te quiero','','song','reggaeton','salsa','rap','rock'], 'musica'),
        (['amor','quieres','novio','novia','love','carino','te quiero','enamorad'], 'amor'),
        (['clima','lluvia','sol','calor','frio','temperatura','weather','nublado'], 'clima'),
        (['comida','comer','hambre','cocinar','plato','arroz','pizzaenamorad'], 'amor'),
        (['clima','lluvia','sol','calor','frio','temperatura','weather','nublado'], 'clima'),
        (['comida','comer','hambre','cocinar','plato','arroz','pizza','food','desayuno','almuerzo','cena'], 'comida'),
        (['deporte','futbol','beisbol','basket','correr','gym','ejercicio','nadar','boxeo'], 'deportes'),
        (['pelicula','cine','serie','netflix','film','movie','actor','actriz','anime'], 'pelicula'),
        (['edad','anos','food','desayuno','almuerzo','cena'], 'comida'),
        (['deporte','futbol','beisbol','basket','correr','gym','ejercicio','nadar','boxeo'], 'deportes'),
        (['pelicula','c tienes','viejo','joven','cuando naciste','cumpleanos','nacimiento'], 'edad'),
        (['puedes','sabes','capaz','haces','funciones','habilidadine','serie','netflix','film','movie','actor','actriz','anime'], 'pelicula'),
        (['edad','anos tienes','viejo','joven','cuando naciste','cumpleanos','nacimiento'], 'edad'),
        (['puedes','sabes','capaz','haces','funciones','habilidad','capacidad','sirves'], 'capacidad'),
        (['mate','calcul','numer','suma','resta','multiplica','divide','ecuacion','algebra','','capacidad','sirves'], 'capacidad'),
        (['mate','calcul','numer','suma','resta','multiplica','divide','ecuacion','algebra','porcentaje'], 'matematica'),
        (['ciencia','fisic','quimic','biolog','atomo','celula','molecul','electron','newton','einstein'], 'ciencia'),
        porcentaje'], 'matematica'),
        (['ciencia','fisic','quimic','biolog','atomo','celula','molecul','electron','newton','einstein'], 'ciencia'),
        (['histori','guerra','antiguo','civilizacion','imperio','rey','reina','revolucion','mundial'], 'historia'),
        (['tecnologi','comput','program','codigo(['histori','guerra','antiguo','civilizacion','imperio','rey','reina','revolucion','mundial'], 'historia'),
        (['tecnologi','comput','program','codigo','app','software','robot','inteligencia artificial'], 'tecnologia'),
        (['planeta','luna','sol','estrella','galaxia','espacio','nasa','marte','jupiter','universo','astronaut'], 'espacio'),
        (['animal','perro','gato','leon','tigre','pajaro','pez','insecto','dinosaurio','mascota'], 'animales'),','app','software','robot','inteligencia artificial'], 'tecnologia'),
        (['planeta','luna','sol','estrella','galaxia','espacio','nasa','marte','jupiter','universo','astronaut'], 'espacio'),
        (['animal','perro','gato','leon','tigre','pajaro','pez','insecto','dinosaurio','mascota'], 'animales'),
        (['filosofi','existir','sentido de la vida','pensar','socrates','platon','moral','etica'], 'filosofia'),
        (['idioma','lengua','ingles','frances
        (['filosofi','existir','sentido de la vida','pensar','socrates','platon','moral','etica'], 'filosofia'),
        (['idioma','lengua','ingles','frances','chino','mandarin','aleman','traducir','hablar'], 'idiomas'),
        (['salud','doctor','medic','enferm','dolor','fiebre','vitamina','dormir','su','chino','mandarin','aleman','traducir','hablar'], 'idiomas'),
        (['salud','doctor','medic','enferm','dolor','fiebre','vitamina','dormir','sueno','agua'], 'salud'),
        (['dinero','plata','bitcoin','crypto','banco','economia','precio','invertir','negocio','trabajo'], 'dinero'),
        (['jugar','juegoeno','agua'], 'salud'),
        (['dinero','plata','bitcoin','crypto','banco','economia','precio','invertir','negocio','trabajo'], 'dinero'),
        (['jugar','juego','trivia','adivina','reto','competir','apostar','quiz'], 'juego'),
        (['aburrido','aburrimiento','nada que hacer','me','trivia','adivina','reto','competir','apostar','quiz'], 'juego'),
        (['aburrido','aburrimiento','nada que hacer','me aburro','que hago','sin nada'], 'aburrido'),
        (['tonto','idiota','estupido','basura','inutil','malo','feo','odio','asco'], 'insulto'),
        (['sentido','proposito','para que existes','por que existes','razon de ser','mision'], 'sentido'),
        (['cuba','habana','cubano','cubana','m aburro','que hago','sin nada'], 'aburrido'),
        (['tonto','idiota','estupido','basura','inutil','malo','feo','odio','asco'], 'insulto'),
        (['sentido','proposito','para que existes','por que existes','razon de ser','mision'], 'sentido'),
        (['cuba','habana','cubano','cubana','malecon','caribeno','isla'], 'cuba'),
        (['consejo','recomienda','sugier','opinion','que hago','ayudame','orientame'], 'consejo'),
        (['motiv','animo','triste','deprim','fuerza','anima','inspir','levantar'], 'motivacion'),
        (['geografi','pais','continente','monte','rio','oceano','lagoalecon','caribeno','isla'], 'cuba'),
        (['consejo','recomienda','sugier','opinion','que hago','ayudame','orientame'], 'consejo'),
        (['motiv','animo','triste','deprim','fuerza','anima','inspir','levantar'], 'motivacion'),
        (['geografi','pais','continente','monte','rio','oceano','lago','desierto','capital','ciudad'], 'geografia'),
    ]
    for words, category in checks:
        if any(w in t for w in words):
            if category is None:
                now = datetime.now().strftime('%I:%M %p del %d de %B de %Y')
                ','desierto','capital','ciudad'], 'geografia'),
    ]
    for words, category in checks:
        if any(w in t for w in words):
            if category is None:
                now = datetime.now().strftime('%I:%M %p del %d de %B de %Y')
                return 'Son las ' + now + '. A darle que el tiempo vuela!', 'happy'
            r = random.choice(FALLBACK[category])
            return r[return 'Son las ' + now + '. A darle que el tiempo vuela!', 'happy'
            r = random.choice(FALLBACK[category])
            return r[0], r[1]
    r = random.choice(FALLBACK['default'])
    return r[0], r[1]

def parse_emotion(text):
    emotions = ['happy','sad','angry','surprised','thinking','sleepy','love',
                'excited','worried0], r[1]
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
    if any(w in rl for w in ['jaja','gracioso','jeje','risa','humor','confused','laughing','neutral']
    for e in emotions:
        tag = '[' + e + ']'
        if tag in text:
            clean = text.replace(tag, '').strip()
            return clean, e
    rl = text.lower()
    if any(w in rl for w in ['jaja','gracioso','jeje','risa','humor']):
        return text, 'laughing'
    if any(w in rl for w in ['no se','no puedo','dificil','problema','triste','perdon']):
        return text, 'sad'
    if any(w in rl for w in']):
        return text, 'laughing'
    if any(w in rl for w in ['no se','no puedo','dificil','problema','triste','perdon']):
        return text, 'sad'
    if any(w in rl for w in ['increible','wow','genial','brutal','de locos','impresionante']):
        return text, 'excited'
    if any(w in rl for w in ['asombroso','serio','verdad']):
        return text, 'surprised'
    if any(w ['increible','wow','genial','brutal','de locos','impresionante']):
        return text, 'excited'
    if any(w in rl for w in ['asombroso','serio','verdad']):
        return text, 'surprised'
    if any(w in rl for w in ['hmm','pienso','creo','quizas','tal vez','depende']):
        return text, 'thinking'
    if any(w in rl for w in ['preocup','cuidado',' in rl for w in ['hmm','pienso','creo','quizas','tal vez','depende']):
        return text, 'thinking'
    if any(w in rl for w in ['preocup','cuidado','ojo','alerta','peligro']):
        return text, 'worried'
    if any(w in rl for w in ['quiero','hermano','amigo','carino','gracias']):
        return text, 'love'
    return text, 'happy'

def ask_gemini(text):
    if not GEMINI_KEY:
        printojo','alerta','peligro']):
        return text, 'worried'
    if any(w in rl for w in ['quiero','hermano','amigo','carino','gracias']):
        return text, 'love'
    return text, 'happy'

def ask('[DIDO] No hay API key de Gemini')
        return None, None
    try:
        chat_history.append({"role": "user", "parts": [{"text": text}]})
        if len(chat_history) > 20:
            del chat_history[0:2]
        url = "https://generativelangu_gemini(text):
    if not GEMINI_KEY:
        print('[DIDO] No hay API key de Gemini')
        return None, None
    try:
        chat_history.append({"role": "user", "parts": [{"text": text}]})
        if len(chat_history) > 20:
            del chat_history[0:2]
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_KEY
        body = {
            "contents": [{"role": "user", "parts": [{"text": PERSONALITY}]}] + chat_history,
            "generationConfig": {
                "temperatureage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_KEY
        body = {
            "contents": [{"role": "user", "parts": [{"text": PERSONALITY}]}] + chat_history,
            "generationConfig": {
                "temperature": 0.9,
                "maxOutputTokens": 200
            }
        }
        r = requests.post(url, json=body, timeout=15)
        print('[DIDO] Gemini status: ' + str(r.status_code))
        if r.status_code == 200:
            data = r.json()
            if": 0.9,
                "maxOutputTokens": 200
            }
        }
        r = requests.post(url, json=body, timeout=15)
        print('[DIDO] Gemini status: ' + str(r.status_code))
        if r.status_code == 200:
            data = r.json()
            if 'candidates' in data and len(data['candidates']) > 0:
                reply = data['candidates'][0]['content']['parts'][0]['text']
                clean_reply, emotion = parse_emotion(reply)
                chat_history.append({"role": "model", "parts": [{"text": clean_reply}]})
                return 'candidates' in data and len(data['candidates']) > 0:
                reply = data['candidates'][0]['content']['parts'][0]['text']
                clean_reply, emotion = parse_emotion(reply)
                chat_history.append({"role": "model", "parts": [{"text": clean_reply}]})
                return clean_reply, emotion
            else:
                print('[DIDO] Sin candidates: ' + str(data))
        else:
            print('[DIDO] Error: ' + r.text[:200])
    except Exception as e:
        print('[DIDO] Exception: ' + str(e))
    if len(chat_history) > 0 and chat_history[-1]['role'] == 'user':
        chat_history.pop()
    return None, None

@app.route('/')
def home clean_reply, emotion
            else:
                print('[DIDO] Sin candidates: ' + str(data))
        else:
            print('[DIDO] Error: ' + r.text[:200])
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
        return jsonify({'reply': 'No te escuche bien, rep():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    text = request.json.get('text', '')
    if not text:
        return jsonify({'reply': 'No te escuche bien, repite porfa.', 'emotion': 'confused'})
    reply, emotion = ask_gemini(text)
    if reply:
        return jsonify({'reply': reply, 'emotion': emotion})
    reply, emotion = get_fallback(text)
    return jsonify({'reply': reply, 'emotion': emotion})

@app.route('/health')
def health():
    hasite porfa.', 'emotion': 'confused'})
    reply, emotion = ask_gemini(text)
    if reply:
        return jsonify({'reply': reply, 'emotion': emotion})
    reply, emotion = get_fallback(text)
    return jsonify({'reply': reply, 'emotion': emotion})

@app.route('/health')
def health():
    has_key = 'si' if GEMINI_KEY else 'no'
    return jsonify({'status': 'ok', 'name': 'Dido OS', 'version': '1.2', 'gemini_key': has_key})

if __name__ == '__main__':_key = 'si' if GEMINI_KEY else 'no'
    return jsonify({'status': 'ok', 'name': 'Dido OS', 'version': '1.2', 'gemini_key': has_key})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('[DIDO] Iniciando en puerto ' + str(port))
    print('[DIDO] Gemini API Key: ' + ('SI' if GEMINI_KEY else 'NO'))
    app.run(host='0.0.0.0', port=port, debug=False)
