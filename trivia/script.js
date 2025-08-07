const buttons = document.querySelectorAll('.choice');
const feedback1 = document.getElementById('feedback1');

buttons.forEach(button => {
    button.addEventListener('click', () => {
                // Reset button colors
        buttons.forEach(btn => btn.style.backgroundColor = '');

        if (button.classList.contains('correct')) {
            button.style.backgroundColor = 'green';
            feedback1.textContent = 'Correct!';
        } else {
            button.style.backgroundColor = 'red';
            feedback1.textContent = 'Incorrect';
            }
        });
    });

        // PART 2: Free-response logic
const input = document.getElementById('free-response');
const checkBtn = document.getElementById('check-answer');
const feedback2 = document.getElementById('feedback2');

checkBtn.addEventListener('click', () => {
    const answer = input.value.trim().toLowerCase();

    if (answer === 'william shakespeare' || answer === 'shakespeare') {
        input.style.backgroundColor = 'lightgreen';
        feedback2.textContent = 'Correct!';
         } 
    else {
        input.style.backgroundColor = '#f08080';
        feedback2.textContent = 'Incorrect';
        }
    });