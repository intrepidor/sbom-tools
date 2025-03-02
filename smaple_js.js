// JavaScript Template

// Function to add two numbers
function add(a, b) {
    return a + b;
}

// Function to subtract two numbers
function subtract(a, b) {
    return a - b;       
}

// Function to multiply two numbers                     
function multiply(a, b) {   
    return a * b;
}

// Function to divide two numbe rs
function divide(a, b) {
    if (b === 0) {
        throw new Error("Division by zero is not allowed.");
    }
    return a / b;
}

// Example usage
const num1 = 10;
const num2 = 5;

console.log(`Add: ${add(num1, num2)}`);
console.log(`Subtract: ${subtract(num1, num2)}`);
console.log(`Multiply: ${multiply(num1, num2)}`);
console.log(`Divide: ${divide(num1, num2)}`);

for (let idx = 0; idx < something.length; idx++) {
    const myelement = something[idx];
    console.log(myelement);
}
