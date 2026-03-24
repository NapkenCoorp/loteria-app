from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# 🔗 APIs OFICIAIS
urls = {
    "mega": "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena",
    "quina": "https://servicebus2.caixa.gov.br/portaldeloterias/api/quina",
    "lotofacil": "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil",
    "lotomania": "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotomania",
    "dupla": "https://servicebus2.caixa.gov.br/portaldeloterias/api/duplasena",
    "timemania": "https://servicebus2.caixa.gov.br/portaldeloterias/api/timemania",
    "diadesorte": "https://servicebus2.caixa.gov.br/portaldeloterias/api/diadesorte",
    "supersete": "https://servicebus2.caixa.gov.br/portaldeloterias/api/supersete"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

# 🔧 FUNÇÃO PADRÃO
def pegar_dados(tipo):
    url = urls.get(tipo)

    try:
        r = requests.get(url, headers=headers)
        data = r.json()

        # 🎰 NÚMEROS
        numeros = " - ".join(data.get("listaDezenas", []))

        # 📊 PRÊMIOS DINÂMICOS
        premios = []
        total_ganhadores = 0

        for p in data.get("listaRateioPremio", []):
            faixa = p.get("descricaoFaixa", "")
            ganhadores = p.get("numeroDeGanhadores", 0)
            valor = p.get("valorPremio", 0)

            total_ganhadores += ganhadores

            premios.append({
                "acertos": faixa,
                "ganhadores": ganhadores,
                "valor": f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            })

        return {
            "concurso": data.get("numero", "N/A"),
            "data": data.get("dataApuracao", "N/A"),
            "numeros": numeros,
            "status": "Acumulou" if data.get("acumulado") else "Não acumulou",
            "premios": premios,
            "total_ganhadores": total_ganhadores
        }

    except Exception as e:
        return {
            "erro": str(e),
            "numeros": "",
            "premios": []
        }

# 🌐 ROTAS
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<tipo>")
def api(tipo):
    return jsonify(pegar_dados(tipo))

# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)