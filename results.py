from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# 🔥 CONFIG PADRÃO (CAIXA)
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://servicebus2.caixa.gov.br/portaldeloterias/api"

# 🔄 MAPEAMENTO DAS LOTERIAS
ROTAS = {
    "mega": "megasena",
    "quina": "quina",
    "loto": "lotofacil",
    "lotomania": "lotomania",
    "dupla": "duplasena",
    "time": "timemania",
    "dia": "diadesorte",
    "sete": "maismilionaria"
}

# 🌐 HOME
@app.route("/")
def home():
    return render_template("index.html")


# 🔧 FUNÇÃO GENÉRICA
def buscar(loteria):

    try:
        url = f"{BASE_URL}/{loteria}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()

        dezenas = data.get("listaDezenas", [])

        resultado = {
            "concurso": data.get("numero"),
            "data": data.get("dataApuracao"),
            "numeros": " - ".join(dezenas),
            "status": "Acumulou" if data.get("acumulado") else "Não acumulou",
            "local": data.get("nomeMunicipioUFSorteio"),
            "ganhadores": data.get("quantidadeGanhadores"),
            "proximo_premio": data.get("valorEstimadoProximoConcurso", 0),
            "premios": data.get("listaRateioPremio", [])
        }

        return resultado

    except Exception as e:
        return {"erro": str(e)}


# 🎰 ROTAS AUTOMÁTICAS
@app.route("/<tipo>")
def rota(tipo):

    if tipo not in ROTAS:
        return jsonify({"erro": "Loteria inválida"})

    dados = buscar(ROTAS[tipo])
    return jsonify(dados)


# ▶️ RODAR LOCAL / RENDER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
