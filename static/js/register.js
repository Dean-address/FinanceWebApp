const usernameField = document.querySelector('#usernameField')
const emailField = document.querySelector('#emailField')
const passField = document.querySelector('#passwordField')
const feedbackArea = document.querySelector('.invalid_feedback')
const emailFeedBackArea = document.querySelector('.emailFeedBackArea')
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput')
const emailSuccessOutput = document.querySelector('.emailSuccessOutput')
const showPasswordToggle = document.querySelector('.showPasswordToggle')
const submitBtn = document.querySelector('.submit-btn')

const validateInput = (field, successOutput, feedbackArea, endpoint, fieldName) => {
	const inputVal = field.value.trim(); // Trim whitespace

	// Show loading message
	successOutput.textContent = `Checking ${inputVal}`;
	successOutput.style.display = 'block';

	// Reset styles and messages
	field.classList.remove('is-invalid');
	feedbackArea.style.display = 'none';

	// Proceed only if input has value
	if (inputVal.length > 0) {
		fetch(endpoint, {
			method: 'POST',
			body: JSON.stringify({ [fieldName]: inputVal }), // Dynamic field name

		})
			.then(res => res.json())
			.then(data => {
				successOutput.style.display = 'none';

				// Show error message if present
				if (data[`${fieldName}_error`]) {
					submitBtn.disabled = true
					field.classList.add('is-invalid');
					feedbackArea.innerHTML = `<p>${data[`${fieldName}_error`]}</p>`;
					feedbackArea.style.display = 'block';
				} else {
					submitBtn.removeAttribute('disabled')


				}
			})
			.catch(error => console.error('Error:', error)); // Handle fetch errors
	} else {
		successOutput.style.display = 'none';
	}
};
const handleToggleInput = function (e) {
	if (showPasswordToggle.textContent === 'SHOW') {
		showPasswordToggle.textContent = 'HIDE'
		passField.setAttribute("type", 'text')
	} else {
		showPasswordToggle.textContent = 'SHOW'
		passField.setAttribute("type", 'password')
	}
}
emailField.addEventListener('keyup', () => {
	validateInput(
		emailField,
		emailSuccessOutput,
		emailFeedBackArea,
		'/authentication/validate_email/',
		'email'
	);
});

usernameField.addEventListener('keyup', () => {
	validateInput(
		usernameField,
		usernameSuccessOutput,
		feedbackArea,
		'/authentication/validate_username/',
		'username'
	);
});


showPasswordToggle.addEventListener('click', handleToggleInput)