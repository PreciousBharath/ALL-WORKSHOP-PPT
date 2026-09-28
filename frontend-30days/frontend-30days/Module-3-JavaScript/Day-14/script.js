// Day 14 - JavaScript Basics: Variables, Data Types, Operators

// ===== VARIABLES =====
// Three ways to declare variables: var, let, const

// var - Function scoped (avoid in modern code)
var oldVariable = "This is var";

// let - Block scoped (preferred)
let firstName = "John";
let age = 25;

// const - Block scoped, cannot be reassigned
const PI = 3.14159;
const country = "USA";

console.log("First Name:", firstName);
console.log("Age:", age);
console.log("PI:", PI);

// ===== DATA TYPES =====

// String
let name = "John Doe";
console.log("Type of name:", typeof name);

// Number
let score = 95.5;
console.log("Type of score:", typeof score);

// Boolean
let isStudent = true;
console.log("Type of isStudent:", typeof isStudent);

// Undefined
let uninitialized;
console.log("Type of uninitialized:", typeof uninitialized);

// Null
let empty = null;
console.log("Type of empty:", typeof empty);

// Object
let person = {
    name: "John",
    age: 25,
    city: "New York"
};
console.log("Person object:", person);

// Array
let colors = ["red", "green", "blue"];
console.log("Colors array:", colors);

// ===== OPERATORS =====

// Arithmetic Operators
let a = 10;
let b = 3;

console.log("\n===== ARITHMETIC OPERATORS =====");
console.log("Addition: 10 + 3 =", a + b);
console.log("Subtraction: 10 - 3 =", a - b);
console.log("Multiplication: 10 * 3 =", a * b);
console.log("Division: 10 / 3 =", a / b);
console.log("Modulus: 10 % 3 =", a % b);
console.log("Exponentiation: 2 ** 3 =", 2 ** 3);

// Assignment Operators
console.log("\n===== ASSIGNMENT OPERATORS =====");
let x = 5;
console.log("x =", x);
x += 3;  // x = x + 3
console.log("After x += 3:", x);
x -= 2;  // x = x - 2
console.log("After x -= 2:", x);
x *= 2;  // x = x * 2
console.log("After x *= 2:", x);

// Comparison Operators
console.log("\n===== COMPARISON OPERATORS =====");
console.log("5 == '5':", 5 == '5');      // true (loose equality)
console.log("5 === '5':", 5 === '5');    // false (strict equality)
console.log("5 !== '5':", 5 !== '5');    // true (strict not equal)
console.log("10 > 5:", 10 > 5);
console.log("10 < 5:", 10 < 5);
console.log("10 >= 10:", 10 >= 10);
console.log("10 <= 5:", 10 <= 5);

// Logical Operators
console.log("\n===== LOGICAL OPERATORS =====");
let isSummer = true;
let isWeekend = false;

console.log("true && false:", true && false);     // AND operator
console.log("true || false:", true || false);     // OR operator
console.log("!true:", !true);                    // NOT operator

console.log("isSummer && isWeekend:", isSummer && isWeekend);
console.log("isSummer || isWeekend:", isSummer || isWeekend);

// String Concatenation & Interpolation
console.log("\n===== STRING OPERATIONS =====");
let greeting = "Hello";
let name2 = "Alice";

// Concatenation
console.log("Concatenation: " + greeting + " " + name2);

// Template literals (modern way)
console.log(`Template literal: ${greeting} ${name2}`);
console.log(`The sum of 5 + 3 is: ${5 + 3}`);

// ===== PRACTICE EXERCISE =====
console.log("\n===== PRACTICE EXERCISE =====");

// Create variables
let student_name = "Bob";
let student_age = 20;
let gpa = 3.75;
let is_honors = true;

// Calculate birth year (assuming current year is 2024)
let current_year = 2024;
let birth_year = current_year - student_age;

// Display information
console.log(`Student: ${student_name}`);
console.log(`Age: ${student_age}`);
console.log(`GPA: ${gpa}`);
console.log(`Birth Year: ${birth_year}`);
console.log(`Honors Student: ${is_honors}`);
console.log(`Is honors and GPA > 3.5: ${is_honors && (gpa > 3.5)}`);
