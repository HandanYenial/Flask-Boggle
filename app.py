from flask import Flask,request,render_template,session,jsonify
from boggle import Boggle
#from boggle file import Boggle class

app=Flask(__name__)
app.config["SECRET_KEY"] = "123so-secret-456"

boggle_game = Boggle() #showing the class Boggle as a variable.

@app.route('/')
def display_the_board():
    """Display the game board"""
    board = boggle_game.make_board()  #get the make_board() function from Boggle class
    session["board"] = board
    highscore = session.get("highscore",0)
    number_of_plays = session.get("number_of_plays",0) 
    #it could be written as nplays = session[nplays], but in here needed to add 0, bcz if it cannot find a number
    #it will give an error, To avoid error session.get used
 
    return render_template("board.html",
                           board = board , 
                           highscore = highscore,
                           number_of_plays = number_of_plays)
    

#there could be a redirect for guess words but in the assignment,
#js will be used because the page should not refresh when the user submits the form, so ajax is used.

@app.route("/check-word")
def check_word(): 
    """Check the word user submits if it's in the dictionary or not"""
    word = request.args["word"] #will read the "word" from the html
    board = session["board"]
    response = boggle_game.check_valid_word(board,word)
    
    return jsonify({"result" : response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update number of plays, update highscore"""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    number_of_plays = session.get("number_of_plays", 0)
    
    session["number_of_plays"] = number_of_plays + 1
    session["highscore"] = max(score,highscore)
    
    return jsonify(brokeRecord = score > highscore)
    

    

    