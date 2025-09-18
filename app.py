from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para receber os dados e fazer o diagnóstico
@app.route('/diagnosticar', methods=['POST'])
def diagnosticar():
    # Pega os dados enviados pelo front-end
    dados = request.get_json()
    faturamento_bruto = float(dados.get('faturamento_bruto'))
    cmv = float(dados.get('cmv'))
    descontos = float(dados.get('descontos'))
    despesas = float(dados.get('despesas'))

    # Realiza os cálculos
    faturamento_liquido = faturamento_bruto - descontos
    lucro_bruto = faturamento_liquido - cmv
    lucro_liquido = lucro_bruto - despesas

    # Evita divisão por zero
    if faturamento_liquido > 0:
        margem_bruta = (lucro_bruto / faturamento_liquido) * 100
        margem_liquida = (lucro_liquido / faturamento_liquido) * 100
    else:
        margem_bruta = 0
        margem_liquida = 0
    
    # Gera o relatório de diagnóstico
    diagnostico = {
        'faturamento_liquido': faturamento_liquido,
        'lucro_bruto': lucro_bruto,
        'lucro_liquido': lucro_liquido,
        'margem_bruta': margem_bruta,
        'margem_liquida': margem_liquida,
        'sugestoes': []
    }

    if margem_liquida < 10:
        diagnostico['sugestoes'].append('A margem de lucro líquida está baixa. Sugere-se revisar as despesas operacionais ou a política de preços.')
    if (descontos / faturamento_bruto) > 0.15:
        diagnostico['sugestoes'].append('A taxa de descontos concedidos é alta. Isso pode estar reduzindo significativamente seu faturamento. Avalie a eficácia das promoções.')
    if (cmv / faturamento_liquido) > 0.7:
        diagnostico['sugestoes'].append('O custo de mercadoria vendida (CMV) é elevado. Negocie melhores preços com seus fornecedores ou ajuste o preço de venda.')

    # Retorna o diagnóstico como JSON
    return jsonify(diagnostico)

if __name__ == '__main__':
    app.run(debug=True)