import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(_name_)
# Permite que o seu site no GitHub Pages converse com este servidor
CORS(app)

# Pega a chave que vamos esconder no Render depois
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/api/analisar', methods=['POST'])
def analisar_produto():
    try:
        dados = request.get_json()
        url_produto = dados.get('url')
        
        if not url_produto:
            return jsonify({"sucesso": False, "erro": "Nenhum link foi enviado."}), 400
            
        # Simulação do texto que a sua inteligência vai ler do link
        dados_da_pagina = f"Verifique o impacto ecológico e a sustentabilidade do produto neste link: {url_produto}"

        # Chamada protegida para a OpenAI
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é o EcoScan, um assistente especialista em análise de sustentabilidade de produtos."},
                {"role": "user", "content": dados_da_pagina}
            ]
        )
        
        return jsonify({
            "sucesso": True,
            "analise": resposta.choices[0].message.content
        }), 200

    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500

if _name_ == '_main_':
    app.run(port=5000, debug=True)
