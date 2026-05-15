from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

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
    game_data = GAMES.get(game_id)
    if not game_data:
        return "Jogo não encontrado", 404

    # Se o jogo tiver classificação, validamos a idade
    if game_data['age_rating'] > 0:
        user_dob_str = request.form.get('dob')

        if not user_dob_str or user_dob_str == 'none':
            flash('Por favor, informe sua data de nascimento.')
            return redirect(url_for('game', game_id=game_id))

        try:
            dob = datetime.strptime(user_dob_str, '%Y-%m-%d')
            hoje = datetime.today()
            user_age = hoje.year - dob.year - ((hoje.month, hoje.day) < (dob.month, dob.day))

            if user_age < game_data['age_rating']:
                flash(f'Atenção: Este jogo requer {game_data["age_rating"]} anos. Você tem {user_age} anos.')
                return redirect(url_for('game', game_id=game_id))
        except ValueError:
            flash('Data inválida.')
            return redirect(url_for('game', game_id=game_id))

    # Adição ao carrinho (Fluxo comum para ambos os casos)
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(game_data)
    session.modified = True
    flash(f'"{game_data["name"]}" adicionado ao carrinho!')

    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    """Visualização do Carrinho"""
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

@app.route('/checkout')
def checkout():
    """
    Limpa o carrinho da sessão e redireciona para a página inicial 
    com uma mensagem de sucesso.
    """
    # Remove a chave 'cart' da sessão se ela existir
    session.pop('cart', None)

    # Adicionamos uma mensagem para o usuário saber que deu certo
    flash('Compra realizada com sucesso! Os jogos foram adicionados à sua biblioteca.')

    # Redireciona de volta para a loja (página inicial)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)