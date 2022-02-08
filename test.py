from html.entities import html5
from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        
    #the test for the first route is:    
    #@app.route('/')
    # def display_the_board():
    #"""Display the game board"""
    #board = boggle_game.make_board()  #get the make_board() function from Boggle class
    #session["board"] = board
    #highscore = session.get("highscore",0)
    #number_of_plays = session.get("number_of_plays",0) 
    #return render_template("board.html",
                          # board = board , 
                          # highscore = highscore,
                          # number_of_plays = number_of_plays)
                          
    
    
        
    def test_display_the_board(self):
        with self.client:   #same as: with app.test_client() as client:
            response=self.client.get("/")
            self.assertIn('board' , session) #is the board in session
            self.assertIsNone(session.get('highscore'))  
            self.assertIsNone(session.get('number_of_plays'))
            #All Python functions return something. If you don't specify a return value,
            #None is returned. So if your goal really is to make sure that something doesn't return a value,
            self.assertIn(b'<p> High Score :', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)
            
   
#@app.route("/check-word")
# def check_word(): 
    #"""Check the word user submits if it's in the dictionary or not"""
    # word = request.args["word"] #will read the "word" from the html
    #board = session["board"]
    #response = boggle_game.check_valid_word(board,word)
    #return jsonify({"result" : response})

    # test if the word is valid by modifying the board in the session
    
    def test_check_word_valid(self):
        with self.client as client:
            with client.session_transaction() as session:
                session['board']=[
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]
                                 ]
            response = self.client.get('/check-word?word=cat')
            self.assertEqual(response.json['result'], 'ok') 
            #assertEqual(firstValue,secondValue, message)
            # return jsonify({"result" : response}) in app.py
            
  #session_transaction() : When used in combination with a with statement this opens a session 
  #transaction. This can be used to modify the session that the test client uses. 
  #Once the with block is left the session is stored back.Internally this is implemented by 
  #going through a temporary test request context and since session handling could depend
  #on request variables this function accepts the same arguments  
    
    def test_check_word_invalid(self):
        """Test if word is in the dictionary"""
        
        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')
        
    def test_word_on_board(self):
        """Test if word is on the board"""
        self.client.get('/')
        response=self.client.get('/check-word?word=sjkhkjdhhfkfhhfhks')
        self.assertEqual(response.json['result'] , 'not-word')
        
            

            
            
    
            
            

