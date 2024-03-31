const form = document.querySelector("#login-form");

form.addEventListener("submit", function (event) {
  event.preventDefault();

  const username = document.querySelector("#username").value;
  const password = document.querySelector("#password").value;

  if (!username || !password) {
    alert("Please enter a username and password.");
    return;
  }

  // Submit the form data to the server or perform any other actions
});
