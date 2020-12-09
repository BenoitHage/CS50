let div01content01 = document.getElementById("div01");
div01content01.innerHTML = "Connected to script";

let arrayToDo = [];
let div02delButton;
let div02textnode;
let div02node;
let div02content01;

function div02display() {
    div02content01 = document.getElementById("div02list");
    div02content01.innerHTML = "";

    for (let a = 0; a < arrayToDo.length; a++) {
        div02node = document.createElement("li");
        div02textnode = document.createTextNode(arrayToDo[a]);

        div02delButton = document.createElement("input");
        div02delButton.type = "button";
        div02delButton.value = "x";
        div02delButton.id = arrayToDo[a]
        div02delButton.addEventListener('click', div02removeFromList);

        div02node.appendChild(div02textnode);
        div02node.appendChild(div02delButton);
        document.getElementById("div02list").appendChild(div02node);
    }
}

function div02addToList() {
    let div02toAdd = document.getElementById("div02inputText").value;
    let div02clear = document.getElementById("div02inputText");

    if (arrayToDo.length === 0) {
        arrayToDo.push(div02toAdd);
        div02display()
        return;
    }

    for (let a = 0; a < arrayToDo.length; a++) {
        if (arrayToDo[a] === div02toAdd) {
            div02clear.value = "";
            alert("Already present")
            div02display()
            return;
        }
    }

    arrayToDo.push(div02toAdd)
    div02display()
}

function div02removeFromList() {
    for (let a = 0; a < arrayToDo.length; a++) {
        if (this.id === arrayToDo[a]) {
            arrayToDo.splice(a, 1);
        }
    }

    div02display();
}

div02display()
