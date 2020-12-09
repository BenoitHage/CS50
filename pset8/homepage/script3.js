let div01content01 = document.getElementById("div01");
div01content01.innerHTML = "Connected to script";

let calcScreen1 = document.getElementById("calcScreen1")
let calcScreen2 = document.getElementById("calcScreen2")

let currentInput = "";
let lastInput = "";

function keyPress(id) {
    currentInput += id
    calcScreen2.innerHTML = currentInput;
}

function compute(input) {
    let currentOperation = eval(input);
    lastInput = currentInput;
    calcScreen1.innerHTML = currentOperation;
    calcScreen2.innerHTML = currentOperation;
    currentInput = currentOperation;
}

function erase() {
    calcScreen1.innerHTML = "";
    calcScreen2.innerHTML = "";
    currentInput = "";
}