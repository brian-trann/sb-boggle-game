from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        ''' Sets up every test'''
        self.client = app.test_client()
        app.config['TESTING']= True

    def test_start(self):
        '''Make sure that POST request is made, on /start '''
        with self.client as client:
            res = client.post('/start')
            self.assertEqual(res.status_code, 302)
            board_size = len(session['board'])
            self.assertEqual(board_size, 5)

    def test_boggle(self):
        '''Create a session transaction; test boggle view '''
        with self.client as client:
            with client.session_transaction() as session:
                session['board']= [['C', 'S', 'V', 'K', 'X'], ['H', 'E', 'R', 'U', 'Z'], ['Y', 'V', 'L', 'L', 'G'], ['M', 'S', 'Q', 'U', 'U'], ['M', 'C', 'A', 'A', 'E']]
            res = client.get('/boggle')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIsNone(session.get('high_score'))
            self.assertIsNone(session.get('num_plays'))
            self.assertIn('<td class="0-0">', html)
            self.assertEqual(len(session.get('board')),5)
    
    def test_guess_real_word(self):
        '''Checks guess route (GET request). Returns JSON. Check valid word'''
        with self.client as client:
            with client.session_transaction() as session:
                session['board']= [['C', 'S', 'V', 'K', 'X'], ['H', 'E', 'R', 'U', 'Z'], ['Y', 'V', 'L', 'L', 'G'], ['M', 'S', 'Q', 'U', 'U'], ['M', 'C', 'A', 'A', 'E']]

            res= client.get('/guess?guess=her')
            self.assertEqual(res.status_code,200)
            self.assertEqual(res.json['result'],'ok')

    def test_guess_not_on_board_word(self):
        '''Checks guess route (GET request). Returns JSON. Check valid word'''
        with self.client as client:
            with client.session_transaction() as session:
                session['board']= [['C', 'S', 'V', 'K', 'X'], ['H', 'E', 'R', 'U', 'Z'], ['Y', 'V', 'L', 'L', 'G'], ['M', 'S', 'Q', 'U', 'U'], ['M', 'C', 'A', 'A', 'E']]

            res= client.get('/guess?guess=test')
            self.assertEqual(res.status_code,200)
            self.assertEqual(res.json['result'],'not-on-board')


    def test_guess_not_word(self):
        '''Checks guess route (GET request). Returns JSON. Check invalid word'''
        with self.client as client:
            with client.session_transaction() as session:
                session['board']= [['C', 'S', 'V', 'K', 'X'], ['H', 'E', 'R', 'U', 'Z'], ['Y', 'V', 'L', 'L', 'G'], ['M', 'S', 'Q', 'U', 'U'], ['M', 'C', 'A', 'A', 'E']]

            res= client.get('/guess?guess=notawordzzzz')
            self.assertEqual(res.status_code,200)
            self.assertEqual(res.json['result'],'not-word')

    def test_score(self):
        '''Checks score (POST) request.'''
        with self.client as client:
            with client.session_transaction() as session:
                session['board']= [['C', 'S', 'V', 'K', 'X'], ['H', 'E', 'R', 'U', 'Z'], ['Y', 'V', 'L', 'L', 'G'], ['M', 'S', 'Q', 'U', 'U'], ['M', 'C', 'A', 'A', 'E']]
        
                
        res = client.post('/score',json={"score":"0"})
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.json['high_score'],0)

        res2 = client.post('/score',json={"score":"10"})
        self.assertEqual(res2.status_code,200)
        self.assertEqual(res2.json['high_score'],10)
        

    def test_session_high_score(self):
        '''Checks session high score '''
        with self.client as client:
            with client.session_transaction() as test_session:
                test_session['board']= [['C', 'S', 'V', 'K', 'X'], ['H', 'E', 'R', 'U', 'Z'], ['Y', 'V', 'L', 'L', 'G'], ['M', 'S', 'Q', 'U', 'U'], ['M', 'C', 'A', 'A', 'E']]
                test_session['high_score']=10
            res= client.get('/boggle')
            self.assertEqual(res.status_code,200)
            self.assertEqual(session['high_score'],10)
    

            
        