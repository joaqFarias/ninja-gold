from django.shortcuts import render, redirect
import random
import time

# Create your views here.
def root(request):
    return redirect('/games')

def index(request):
    if 'oro_actual' not in request.session:
        request.session['oro_actual'] = 0

    if 'resultados' not in request.session.keys():
        request.session['resultados'] = []
    
    if 'cambio_oro' not in request.session.keys():
        request.session['cambio_oro'] = 0

    # parametros iniciales de juego
    modificarParametros('farm', 10, 20, request)
    modificarParametros('cave', 5, 10, request)
    modificarParametros('house', 2, 5, request)
    modificarParametros('casino', 0, 50, request)

    return render(request, 'index.html') 

def farm(request):
    oro_obtenido = actualizar_oro('farm', request)
    actualizar_resultados(oro_obtenido, 'farm', request)
    return render(request, 'index.html') 

def cave(request):
    oro_obtenido = actualizar_oro('cave', request)
    actualizar_resultados(oro_obtenido, 'cave', request)
    return render(request, 'index.html') 

def house(request):
    oro_obtenido = actualizar_oro('house', request)
    actualizar_resultados(oro_obtenido, 'house', request)
    return render(request, 'index.html') 

def casino(request):
    cambio_oro = actualizar_oro_casino('casino', request)
    actualizar_resultados(cambio_oro, 'casino', request)
    return render(request, 'index.html') 

def reset(request):
    if 'oro_actual' in request.session.keys():
        del request.session['oro_actual']
    if 'prob_obtener_oro' in request.session.keys():
        del request.session['prob_obtener_oro']
    if 'resultados' in request.session.keys():
        del request.session['resultados']
    return redirect('/games')


# funciones utiles
def randomMinMaxInt(min=0, max=1) -> int:
    return round((random.random() * (max-min)+min))

def modificarParametros(game: str, min: int, max: int, request) -> None:
    request.session[f'oro_minget_{game}'] = min
    request.session[f'oro_maxget_{game}'] = max

def actualizar_oro(game: str, request) -> None:
    oro_obtenido = randomMinMaxInt(request.session[f'oro_minget_{game}'], request.session[f'oro_maxget_{game}'])
    request.session['oro_actual'] = request.session['oro_actual'] + oro_obtenido
    return oro_obtenido

def actualizar_oro_casino(game: str, request) -> None:
    cambio_oro = randomMinMaxInt(request.session[f'oro_minget_{game}'], request.session[f'oro_maxget_{game}'])
    request.session['prob_obtener_oro'] = 0.5
    if randomMinMaxInt() > request.session['prob_obtener_oro']:
        request.session['oro_actual'] = int(request.session['oro_actual']) + cambio_oro
    else:
        cambio_oro = - cambio_oro
        request.session['oro_actual'] = int(request.session['oro_actual']) + cambio_oro
    return cambio_oro
    

def actualizar_resultados(cambio_oro: int, game: str, request):
    print(cambio_oro)
    if cambio_oro >= 0:
        comentario_resultado = f'Earned {cambio_oro} golds from the {game} ({time.strftime("%c")})'
        positivo = True
    else:
        print('entre')
        comentario_resultado = f'Entered {game} and lost {cambio_oro} golds... Ouch...  ({time.strftime("%c")})'
        positivo = False
    
    request.session['resultados'].append([comentario_resultado, positivo])

