from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
# Chave secreta necessária para usar sessões no Flask
app.secret_key = 'chave_secreta_super_segura'

# Simulando um Banco de Dados na memória
GAMES = {
    '1': {'id': '1', 'name': 'Aventura Épica', 'price': 150.00, 'age_rating': 10,
          'description': 'Explore masmorras e derrote monstros.'},
    '2': {'id': '2', 'name': 'Sobrevivência Sombria', 'price': 90.00, 'age_rating': 18,
          'description': 'Jogo de terror com zumbis.'},
    '3': {'id': '3', 'name': 'Corrida Divertida', 'price': 45.00, 'age_rating': 0,
          'description': 'Corridas para toda a família.'}
}


@app.route('/')
def index():
    """Passo 1: O sistema apresenta a página principal, com recomendações de jogos."""
    return render_template('index.html', games=GAMES)


@app.route('/game/<game_id>')
def game(game_id):
    """Passos 2 e 3: O sistema apresenta a página do jogo na loja virtual."""
    game_data = GAMES.get(game_id)
    if not game_data:
        return "Jogo não encontrado", 404
    return render_template('game.html', game=game_data)


@app.route('/add_to_cart/<game_id>', methods=['POST'])
def add_to_cart(game_id):
    """Passos 4 e 5: Verificação de idade [RN2] e adição ao carrinho."""
    game_data = GAMES.get(game_id)
    if not game_data:
        return "Jogo não encontrado", 404

    # Passo 4: Validação da idade
    user_age_str = request.form.get('age')

    if not user_age_str or not user_age_str.isdigit():
        flash('Por favor, informe uma idade válida.')
        return redirect(url_for('game', game_id=game_id))

    user_age = int(user_age_str)

    if user_age < game_data['age_rating']:
        flash(f'Atenção: Você não possui a idade mínima ({game_data["age_rating"]} anos) para comprar este jogo.')
        return redirect(url_for('game', game_id=game_id))

    # Passo 5: Adiciona o jogo ao carrinho
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(game_data)
    session.modified = True
    flash(f'"{game_data["name"]}" adicionado ao carrinho com sucesso!')

    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    """Visualização do Carrinho"""
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)


if __name__ == '__main__':
    app.run(debug=True)