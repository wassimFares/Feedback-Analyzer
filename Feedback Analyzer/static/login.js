const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const signUpForm = document.getElementById('sign-up-form');
const signInForm = document.getElementById('sign-in-form');



signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

signUpForm.addEventListener('submit', async (event) => {
	event.preventDefault();
	let name = signUpForm.elements['name'].value;
	let email = validateEmail(signUpForm.elements['email'].value);
	if (email == false) {
		alert('Invalid email');
		return;
	}
	let password = signUpForm.elements['password'].value;
	const formData = new FormData();
	formData.append('name', name);
	formData.append('email', email);
	formData.append('password', password);

	try {
		const response = await fetch('/signup', {
			method: 'POST',
			body: formData
		});

		if (response.ok) {
			console.log('User created');
			window.location.href = '/home';
		} else {
			console.error('User creation failed');
		}
	}
	catch (error) {
		console.error('Error submitting form:', error);
	}
});

function validateEmail(email) {
    const regex = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
    if (regex.test(email)) {
        return email;
    } else {
        return false;
    }
}