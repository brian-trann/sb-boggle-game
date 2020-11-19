class Boggle {
	constructor(time = 60) {
		this.score = 0;
		this.msg = '';
		this.guessed = new Set();
		this.time = time;
		this.timer = setInterval(this.tick.bind(this), 1000);
		$('.boggle-form').on('submit', this.handleGuess.bind(this));
	}
	/**
     * Function to update boggle instance time remaining
     */
	tick() {
		this.time -= 1;
		this.updateTimeLeft();
		if (this.time === 0) {
			clearInterval(this.timer);
		}
	}

	/**
     * Update the DOM to display accurate time left
     */
	async updateTimeLeft() {
		if (this.time !== 0) {
			$('.time').empty().append(this.time);
		} else {
			const currHighScore = await this.handleFinalScore();
			this.handleGameOver(currHighScore);
		}
	}
	/**
     * Handle game over in the DOM
     */
	handleGameOver(currHighScore) {
		$('.time').empty().append('0 -- Game Over!');
		$('#user-guess').prop('disabled', true);
		$('.boggle-form button').prop('disabled', true);
		$('.high-score').empty().append(currHighScore);
		if (this.score < currHighScore) {
			this.msg = 'Try again!';
		} else if (this.score === currHighScore) {
			this.msg = 'Tied With High Score! ';
		} else {
			this.msg = 'New High Score!';
		}
		$('.message').empty().append(this.msg);
		this.resetGame();
	}
	/**
     * Add button to start over!
     * 
     */
	resetGame() {
		const $resetButton = $('<button>').attr('type', 'submit').text('Reset Boggle!');
		const $resetForm = $('<form>').attr('action', '/start').attr('method', 'POST').addClass('reset');
		$resetForm.append($resetButton);
		$('.reset').empty().append($resetForm);
	}

	/**
     * Function to handle the user's guess
     */

	async handleGuess(event) {
		event.preventDefault();
		const userGuess = $('#user-guess').val();
		const lowerGuess = userGuess.toLowerCase();
		$('#user-guess').val('');

		// guess needs to be sent to server
		const res = await this.postData(lowerGuess);

		this.updateGuess(lowerGuess, res);
	}

	/**
     * Update DOM for every guess
     */
	updateGuess(lowerGuess, res) {
		if (res === 'not-on-board') {
			this.msg = `Not on the board!`;
		} else if (res === 'ok') {
			if (this.guessed.has(lowerGuess)) {
				this.msg = `Already guessed!`;
			} else {
				this.guessed.add(lowerGuess);
				this.msg = `Great!`;
				this.score += lowerGuess.length;
			}
		} else {
			this.msg = `Not a word`;
		}
		//Update DOM with a msg for every guess, update score for every guess
		$('.message').empty().append(this.msg);
		$('.score').empty().append(this.score);
	}
	/**
     * Async function to send POST request
     */
	async postData(guess) {
		const response = await fetch(`/guess?guess=${guess}`);
		const data = await response.json();

		return data.result;
	}
	/**
     * Make Post request; recieve json for current high_score
     */

	async handleFinalScore() {
		const scoreBody = `{ \
            "score": "${this.score}"\
        }`;
		const response = await fetch('/score', {
			method  : 'POST',
			headers : {
				'Content-Type' : 'application/json'
			},
			body    : scoreBody
		});
		const res = await response.json();

		return res.high_score;
	}
}
/**
 * Wait for DOM to load, Create new boggle!
 */
$(function() {
	let newBoggle = null;

	// Start Game
	newBoggle = new Boggle();
});
