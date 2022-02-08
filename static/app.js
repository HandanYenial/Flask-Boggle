class BoggleGame {
    /* make a new game at this DOM id */
  
    constructor(boardId, secs = 60) {
      this.secs = secs; // game length
      this.showTimer();
  
      this.score = 0;
      this.words = new Set();
      this.board = $("#" + boardId); //same as document.getElementById(boardId), # is for id
  
      // every 1000 msec, "tick"
      this.timer = setInterval(this.tick.bind(this), 1000); 
      //the timer is set to 120sec, it will tick in every 1 sec
  
      $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    } // add-word is the class for the input.
  
    /* show word in list of words */
  
    showWord(word) {
      $(".words", this.board).append($("<li>", { text: word }));
    } //words is the class for the ul where the  meaningful words will be shown
  
    /* show score in html */
  
    showScore() {
      $(".score", this.board).text(this.score);
    } // Score: <b class="score">0</b> class for the score
  
    /* show a status message */
  
    showMessage(msg, cls) {
      $(".msg", this.board)
        .text(msg)
        .removeClass()
        .addClass(`msg ${cls}`);
    }
  
    /* handle submission of word: if unique and valid, score & show */
  
    async handleSubmit(evt) {
      evt.preventDefault();
      const $word = $(".word", this.board);
  
      let word = $word.val();
      if (!word) return; 
      //if word is empty:if the user didn't submit any word then return nothing
  
      if (this.words.has(word)) {
        this.showMessage(`Already found ${word}`, "err");
        return;
      } //if the user enters the same word then show Already found..
  
      // check server for validity
      const res = await axios.get("/check-word", { params: { word: word }});
      if (res.data.result === "not-word") {
        this.showMessage(`${word} is not a valid English word`, "err");
      } else if (res.data.result === "not-on-board") {
        this.showMessage(`${word} is not a valid word on this board`, "err");
      } else {
        this.showWord(word);
        this.score += word.length;
        this.showScore();
        this.words.add(word);
        this.showMessage(`Added: ${word}`, "ok");
      }
  
      $word.val("").focus();
    }
  
    /* Update timer in DOM */
  
    showTimer() {
      $(".timer", this.board).text(this.secs);
    }
  
    /* Tick: handle a second passing in game */
  
    async tick() {
      this.secs -= 1;
      this.showTimer();
  
      if (this.secs === 0) {
        clearInterval(this.timer);
        await this.scoreGame();
      }
    }
  
    /* end of game: score and update message. */
  
    async scoreGame() {
      $(".add-word", this.board).hide();
      const res = await axios.post("/post-score", { score: this.score });
      if (res.data.brokeRecord) {
        this.showMessage(`New record: ${this.score}`, "ok");
      } else {
        this.showMessage(`Final score: ${this.score}`, "ok");
      }
    }
  }

  
  
