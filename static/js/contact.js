const form = document.querySelector('.contact');
const submitBtn = document.querySelector('#submit');

submitBtn.addEventListener('click', (e) => {
  e.preventDefault();
  const name = form.querySelector('#name').value;
  const email = form.querySelector('#email').value;
  const phone = form.querySelector('#phone').value;
  const message = form.querySelector('#message').value;

  // Do something with the form data, like send it to a server
});
