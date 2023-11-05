function validateLowercase(inputElement) {
    // Get the user's input
    const inputValue = inputElement.value;

    // Convert the input to lowercase
    const lowercaseValue = inputValue.toLowerCase();

    // Check if the input matches the lowercase version; if not, update the input field
    if (inputValue !== lowercaseValue) {
        inputElement.value = lowercaseValue;
    }
}
