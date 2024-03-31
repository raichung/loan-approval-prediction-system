const loanRequestForm = document.querySelector('.loan-request-form');
const submitBtn = document.querySelector('input[type="submit"]');

submitBtn.addEventListener('click', (event) => {
    event.preventDefault();

    const formFields = [...loanRequestForm.elements].filter(field => field.tagName === 'INPUT' || field.tagName === 'SELECT' || field.tagName === 'TEXTAREA');

    let formIsValid = true;

    formFields.forEach(field => {
        if (!field.value) {
            formIsValid = false;
            field.style.border = '1px solid red';
        } else {
            field.style.border = '1px solid lightgray';
        }

        if (field.type === 'number' && field.value < 0) {
            formIsValid = false;
            field.style.border = '1px solid red';
        }
    });

    if (!formIsValid) {
        return;
    }

    const formData = new FormData(loanRequestForm);
    const data = {};

    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }

    console.log('Form data:', data);
    loanRequestForm.reset();
});
