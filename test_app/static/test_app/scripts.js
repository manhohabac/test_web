// scripts.js

document.addEventListener("DOMContentLoaded", function() {
    const showAnswerButton = document.getElementById('show-answer-button');
    const checkAnswerButton = document.getElementById('check-answer-button');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    const loadButton = document.getElementById('load-button');
    const csvIndexInput = document.getElementById('csv-index');
    const answerEntry = document.getElementById('answer-entry');
    const resultLabel = document.getElementById('result-label');
    const flashcardCanvas = document.getElementById('flashcard-canvas');
    const ctx = flashcardCanvas.getContext('2d');

    let flashcards = [];
    let currentCardIndex = 0;
    let userScore = 0;

    function displayCard() {
        const card = flashcards[currentCardIndex];
        ctx.clearRect(0, 0, flashcardCanvas.width, flashcardCanvas.height);
        ctx.font = "20px Times New Roman";
        ctx.textAlign = "center";
        ctx.fillText(card.question, flashcardCanvas.width / 2, flashcardCanvas.height / 2);
        resultLabel.textContent = '';
        answerEntry.value = '';
    }

    function flipCard() {
        const card = flashcards[currentCardIndex];
        ctx.clearRect(0, 0, flashcardCanvas.width, flashcardCanvas.height);
        ctx.font = "20px Times New Roman";
        ctx.textAlign = "center";
        if (card.side_up === 'Q') {
            ctx.fillText(card.answer, flashcardCanvas.width / 2, flashcardCanvas.height / 2);
            card.side_up = 'A';
        } else {
            ctx.fillText(card.question, flashcardCanvas.width / 2, flashcardCanvas.height / 2);
            card.side_up = 'Q';
        }
    }

    function displayScore() {
        const scoreDisplay = document.getElementById('score');
        scoreDisplay.textContent = userScore;
    }

//    function checkAnswer() {
//        const userAnswer = answerEntry.value.trim().toLowerCase();
//        const correctAnswer = flashcards[currentCardIndex].answer.trim().toLowerCase();
//        if (userAnswer === correctAnswer) {
//            resultLabel.textContent = 'Correct!';
//            resultLabel.style.color = 'green';
//            userScore += 100;
//            displayScore();
//        } else {
//            resultLabel.textContent = `Incorrect! The answer is: ${flashcards[currentCardIndex].answer}`;
//            resultLabel.style.color = 'red';
//        }
//    }

    function nextCard() {
        currentCardIndex = (currentCardIndex + 1) % flashcards.length;
        displayCard();
    }

    function prevCard() {
        currentCardIndex = (currentCardIndex - 1 + flashcards.length) % flashcards.length;
        displayCard();
    }

    function loadFlashcards(index) {
        fetch(`/static/test_app/data_csv/file${index}.csv`)
            .then(response => response.text())
            .then(data => {
                flashcards = [];
                let rows = data.split('\n');
                for (let i = 1; i < rows.length; i++) { // Bỏ qua dòng tiêu đề
                    let cols = rows[i].split(',');
                    if (cols.length >= 2) {
                        flashcards.push({
                            question: cols[0],
                            answer: cols[1],
                            side_up: "Q"
                        });
                    }
                }
                currentCardIndex = 0;
                displayCard();
            });
    }

    loadButton.addEventListener('click', () => {
        const csvIndex = csvIndexInput.value;
        if (csvIndex) {
            loadFlashcards(csvIndex);
        }
    });

    showAnswerButton.addEventListener('click', flipCard);
    checkAnswerButton.addEventListener('click', checkAnswer);
    nextButton.addEventListener('click', nextCard);
    prevButton.addEventListener('click', prevCard);
});