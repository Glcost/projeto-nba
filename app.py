


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
    
    













if __name__ == "__main__":
    app.run(debug=True)
    