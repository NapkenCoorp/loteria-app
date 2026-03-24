from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# 🌐 HOME
@app.route("/")
def home():
    return render_template("index.html")


# 🔄 MAPA
MAPA = {
    "mega": "mega-sena",
    "quina": "quina",
    "loto": "lotofacil",
    "lotomania": "lotomania",
    "dupla": "dupla-sena",
    "time": "timemania",
    "dia": "dia-de-sorte",
    "sete": "mais-milionaria"
}


# 🔧 FUNÇÃO SEGURA
def buscar(tipo):

    if tipo not in MAPA:
        return {"erro": "Loteria inválida"}

    api = MAPA[tipo]

    # 🔥 LISTA DE APIS (ORDEM DE TENTATIVA)
    urls = [
        f"https://loteriascaixa-api.herokuapp.com/api/{api}/latest",
        f"https://brasilapi.com.br/api/loterias/v1/{api}"
    ]

    for url in urls:
        try:
            r = requests.get(url, timeout=8)

            if r.status_code != 200:
                continue

            if not r.text.strip():
                continue

            data = r.json()

            # 🧠 DETECTA QUAL API RESPONDEU

            # API 1 (heroku)
            if "dezenas" in data:
                return {
                    "concurso": data.get("concurso"),
                    "data": data.get("data"),
                    "numeros": " - ".join(data.get("dezenas", [])),
                    "status": "Acumulou" if data.get("acumulou") else "Não acumulou",
                    "local": data.get("local", ""),
                    "ganhadores": data.get("premiacoes", [{}])[0].get("ganhadores", 0),
                    "proximo_premio": data.get("valorEstimadoProximoConcurso", 0),
                    "premios": [
                        {
                            "descricaoFaixa": p.get("descricao"),
                            "numeroDeGanhadores": p.get("ganhadores"),
                            "valorPremio": p.get("valorPremio")
                        }
                        for p in data.get("premiacoes", [])
                    ]
                }

            # API 2 (brasilapi)
            if "numeros" in data:
                return {
                    "concurso": data.get("concurso"),
                    "data": data.get("data"),
                    "numeros": " - ".join(data.get("numeros", [])),
                    "status": data.get("acumulado") and "Acumulou" or "Não acumulou",
                    "local": "",
                    "ganhadores": 0,
                    "proximo_premio": data.get("valorEstimadoProximoConcurso", 0),
                    "premios": []
                }

        except:
            continue

    return {"erro": "Todas APIs falharam"}


# 🎰 ROTA
@app.route("/<tipo>")
def rota(tipo):
    return jsonify(buscar(tipo))


# ▶️ RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
