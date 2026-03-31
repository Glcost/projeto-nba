


from flask import Flask, render_template, request, flash, redirect
import requests 

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_teste'

def consultar_jogadores(season,team ):
    endpoint = f'https://api.server.nbaapi.com/api/playertotals?season={season}&team={team}&page=1&pageSize=20&isPlayoff=False'
    
    try:
        resposta = requests.get(endpoint, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            return dados.get('data', []) 
    except Exception as e:
        print(f"Erro na requisição: {e}")
    
    return []


def consultar_jogos():
    endpoint = f'https://api.server.nbaapi.com/api/games?isPlayoff=false&page=1&pageSize=50&sortBy=date&ascending=false'
    
    try:
        resposta = requests.get(endpoint, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            return dados.get('data', [])
        
    except Exception as e:
        print(f'Erro na requisição: {e}')        

    return []



def consultar_estasticasplayer(season, playerName):
    endpoint = f'https://api.server.nbaapi.com/api/playertotals?season={season}&page=1&pageSize=15&playerName={playerName}'
    try:
        resposta = requests.get(endpoint, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            return dados.get('data', [])
        
    except Exception as e:
        print(f'Erro na requisição: {e}')        

    return []




# A rota da Página Inicial
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    season = request.form['season']
    team = request.form['team']
    
    if not season or not team:
        flash('Campo precisa estar preenchido!!')
        return redirect('/')
    
    lista_de_jogadores = consultar_jogadores(season,team)
    
    return render_template('index.html', jogadores=lista_de_jogadores, team_code=team)





@app.route('/results', methods = ['GET', 'POST'])
def results():
    
    resultados_jogos = consultar_jogos()
    
    return render_template('results.html', jogos = resultados_jogos)





    
    
    
@app.route('/playerstats', methods=['GET', 'POST'])
def playerstats():
    if request.method == 'GET':
        return render_template('playerstats.html')
    
    season = request.form.get('season')
    playerName_input = request.form.get('playerName')
    
    if not season or not playerName_input:
        flash('Preencha a temporada e o nome do jogador!')
        return redirect('/playerstats')
    
    # Busca os dados na API
    resultado_api = consultar_estasticasplayer(season, playerName_input)
    
    estatisticas_filtradas = []
    
    if resultado_api:
        for p in resultado_api:
            # Compara o nome ignorando maiúsculas/minúsculas
            if playerName_input.lower() in p.get('playerName', '').lower():
                
                # 1. Calcula Pontos por Jogo (PPG)
                jogos = p.get('games', 1) or 1
                p['ppg'] = round(p.get('points', 0) / jogos, 1)
                
                # 2. Calcula Minutes per Game (minutesPg) caso não venha pronto
                p['minutesPg'] = round(p.get('minutesPg', 0) / jogos, 1)

                # 3. Formata as porcentagens para o seu gráfico (0.499 -> 50)
                p['fg_pct'] = round(p.get('fieldPercent', 0) * 100)
                p['tp_pct'] = round(p.get('threePercent', 0) * 100)
                
                # 4. Ajusta a foto (CDN da NBA)
                nomes = p.get('playerName', '').lower().split()
                if len(nomes) >= 2:
                    p['photo_url'] = f"https://nba-players.herokuapp.com/players/{nomes[-1]}/{nomes[0]}"
                else:
                    p['photo_url'] = "https://cdn.nba.com/headshots/nba/latest/1040x760/fallback.png"
                
                estatisticas_filtradas.append(p)
                break # Pega apenas o primeiro jogador que der match
    
    return render_template('playerstats.html', 
                           estatisticas=estatisticas_filtradas, 
                           season=season, 
                           player_name=playerName_input)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# @app.route('/playerstats', methods=['GET', 'POST'])
# def playerstats():
#     if request.method == 'GET':
#         return render_template('playerstats.html')
    
#     season = request.form.get('season')
#     playerName_input = request.form.get('playerName')
    
#     if not season or not playerName_input:
#         flash('Todos os campos precisam estar preenchidos!!')
#         return redirect('/playerstats')
    
#     # Limpa espaços extras do nome
#     playerName_search = ' '.join(playerName_input.split())
    
#     # Busca na API
#     resultado_api = consultar_estasticasplayer(season, playerName_search)
    
#     estatisticas_filtradas = []
    
#     if resultado_api:
#         # 1. Filtramos para garantir que o nome do jogador contenha o que foi digitado (case insensitive)
#         # 2. Damos preferência para o time "TOT" (Total) se o jogador mudou de time no ano
#         for p in resultado_api:
#             if playerName_search.lower() in p.get('playerName', '').lower():
#                 # Calcula PPG (Pontos por jogo)
#                 jogos = p.get('games', 1) or 1
#                 p['ppg'] = round(p.get('points', 0) / jogos, 1)
                
#                 # Formata porcentagens para o gráfico (0.45 -> 45)
#                 p['fg_pct'] = round(p.get('fieldPercent', 0) * 100)
#                 p['tp_pct'] = round(p.get('threePercent', 0) * 100)
                
#                 # Gera URL da foto
#                 nomes = p.get('playerName', '').lower().split()
#                 if len(nomes) >= 2:
#                     p['photo_url'] = f"https://nba-players.herokuapp.com/players/{nomes[-1]}/{nomes[0]}"
#                 else:
#                     p['photo_url'] = "https://cdn.nba.com/headshots/nba/latest/1040x760/fallback.png"
                
#                 estatisticas_filtradas.append(p)
#                 # Paramos no primeiro match certeiro para não misturar jogadores
#                 break 
    
#     return render_template('playerstats.html', 
#                            estatisticas=estatisticas_filtradas, 
#                            season=season, 
#                            player_name=playerName_input)
    
    
    
    
    
    
    
    
    
    
    
    
    
    


# @app.route('/playerstats', methods=['GET', 'POST'])
# def playerstats():
#     if request.method == 'GET':
#         return render_template('playerstats.html')
    
#     season = request.form['season']
#     playerName = request.form['playerName']
    
#     if not season or not playerName:
#         flash('Campo precisa estar preenchido!!')
#         return redirect('/playerstats')
    
    
#     estatisticas_player = consultar_estasticasplayer(season, playerName)
    
#     return render_template('playerstats.html', estatisticas=estatisticas_player, player_name=playerName)



if __name__ == "__main__":
    app.run(debug=True)
    