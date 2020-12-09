let div01content01 = document.getElementById("div01");
div01content01.innerHTML = "Connected to script";

let data = [
    ["11", "21", "31", "41", "51", "13", "23", "33", "43", "53", "12", "52"],
    ["12", "22", "32", "42", "52", "21", "51", "53"],
    ["11", "12", "13", "23", "33", "32", "31", "41", "51", "52", "53"],
    ["13", "23", "33", "43", "53", "11", "12", "32", "51", "52"],
    ["13", "23", "33", "43", "53", "11", "21", "31", "32"],
    ["13", "12", "11", "21", "31", "32", "33", "43", "53", "52", "51"],
    ["11", "21", "31", "41", "51", "12", "13", "32", "33", "43", "53", "52"],
    ["13", "23", "33", "43", "53", "11", "12"],
    ["13", "23", "33", "43", "53", "11", "21", "31", "41", "51", "12", "32", "52"],
    ["11", "21", "31", "23", "51", "12", "13", "32", "33", "43", "53", "52"],
]

function generateRandomColor() {
    return '#' + Math.floor(Math.random() * 16777215).toString(16);
}

function changeColor() {
    let animationContainer = document.getElementById("animationContainer")
    animationContainer.style.backgroundColor = generateRandomColor();
}

function getTime() {
    let currentTime = new Date().toLocaleTimeString('en-BE', {
        hour: "numeric",
        minute: "numeric",
        second: "numeric"
    });
    return currentTime.split(":").join("")
}

function draw(input) {
    if (input.length === 4) {
        if (input[0] === "1") {
            let pixelToDraw = document.getElementById(input.substring(1));
            pixelToDraw.style.backgroundColor = "green";
        }
        else {
            let pixelToDraw = document.getElementById(input.substring(1));
            pixelToDraw.style.backgroundColor = "white";
        }

    } 
    else {
        console.log("Error: wrong input format in draw(): " + input)
    }
}

function clear() {
    for (let a = 1; a <= 6; a++) {
        for (let b = 1; b <= 5; b++) {
            for (let c = 1; c <= 3; c++) {
                draw("0" + `${a}` + `${b}` + `${c}`)
            }
        }
    }
}

function display() {
    clear()
    let timeToDisplay = getTime()
    for (let a = 1; a <= 6; a++) {
        for(let b = 0; b < data[timeToDisplay[a - 1]].length; b++) {
            draw("1" + `${a}` + `${data[timeToDisplay[a - 1]][b]}`)

        }
    }
}

setInterval(changeColor, 1000)
setInterval(display, 1000)

