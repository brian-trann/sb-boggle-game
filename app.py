from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session,jsonify
# from flask_debugtoolbar import DebugToolbarExtension

BOARD = 'board'

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
# debug = DebugToolbarExtension(app)


boggle_game = Boggle()

@app.route('/')
def route_index():
    '''Show homepage'''
    
    return render_template('index.html')

@app.route('/start',methods=["POST"])
def start_boggle():
    '''Start (new) boggle game, save boggle to session'''
    session[BOARD] =[]
    board = boggle_game.make_board()
    session[BOARD] = board
    return redirect('/boggle')

@app.route('/boggle')
def boggle_view():
    '''Boggle game view, Pass through board to front end using jinja Loop through board to display elements'''
    board = session[BOARD]
    return render_template('boggle.html',board=board)

@app.route('/guess')
def check_guess():
    '''Check every user guess with check_valid_word. Return JSON response '''
    user_guess = request.args['guess']
    board = session[BOARD]
    response = boggle_game.check_valid_word(board,user_guess)
    
    return jsonify({'result':response})

    
@app.route('/score', methods=['POST'])
def post_score():
    '''Log session:num_plays, Update new high score, if higher'''
    score = int(request.json['score'])
    high_score= session.get('high_score',0)
    num_plays = session.get('num_plays',0)

    session['num_plays'] = num_plays + 1
    session['high_score'] = max(high_score,score)
    return jsonify({'high_score':max(high_score,score)})