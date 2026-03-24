from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# 🌐 HOME
@app.route("/")
def home():
    return render_template("index.html")


# 🔄 MAPEAMENTO DAS LOTERIAS
MAPA_API = {
    "mega": "mega-sena",
    "quina": "quina",
    "loto": "lotofacil",
    "lotomania": "lotomania",
    "dupla": "dupla-sena",
    "time": "timemania",
    "dia": "dia-de-sorte",
    "sete": "mais-milionaria"
}


# 🔧 FUNÇÃO PRINCIPAL (API ALTERNATIVA)
def buscar(tipo):
    try:
        if tipo not in MAPA_API:
            return {"erro": "Loteria inválida"}

        url = f"https://loteriascaixa-api.herokuapp.com/api/{MAPA_API[tipo]}/latest"

        r = requests.get(url, timeout=10)
        data = r.json()

        dezenas = data.get("dezenas", [])

        # 🔥 MONTA PADRÃO PRO SEU HTML
        resultado = {
            "concurso": data.get("concurso"),
            "data": data.get("data"),
            "numeros": " - ".join(dezenas),
            "status": "Acumulou" if data.get("acumulou") else "Não acumulou",
            "local": data.get("local", "Não informado"),
            "ganhadores": data.get("premiacoes", [{}])[0].get("ganhadores", 0),
            "proximo_premio": data.get("valorEstimadoProximoConcurso", 0),
            "premios": []
        }

        # 🎯 FORMATA PREMIOS (PADRÃO QUE VOCÊ QUER)
        for p in data.get("premiacoes", []):
            resultado["premios"].append({
                "descricaoFaixa": p.get("descricao"),
                "numeroDeGanhadores": p.get("ganhadores"),
                "valorPremio": p.get("valorPremio")
            })

        return resultado

    except Exception as e:
        return {"erro": str(e)}


# 🎰 ROTAS
@app.route("/<tipo>")
def rota(tipo):
    return jsonify(buscar(tipo))


# ▶️ RODAR
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
