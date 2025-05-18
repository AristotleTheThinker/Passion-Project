const container = document.querySelector('.container')
const guess_button = document.querySelector('.guess_button')
const clear_button = document.querySelector('.clear_button')
const erase_checkbox = document.querySelector('.erase')
var pixels = []
var image = []

var draw = false;
var guessing = false;
var erase = false;

function populate() {
    for (let r = 0; r < 28; r++) {
        var row = []
        for(let c = 0; c < 28; c++){
            const div = document.createElement('div')
            div.classList.add('pixel')
            div.addEventListener('mouseover',function(){
                if(!draw) return
                if(guessing) return
                if (erase) div.style.backgroundColor = '#000000'
                else div.style.backgroundColor = '#ffffff'
            })
            div.addEventListener('click',function(){
                if(guessing) return
                if (erase) div.style.backgroundColor = '#000000'
                else div.style.backgroundColor = '#ffffff'
            })
            row.push(div)
            container.appendChild(div)
        }
        pixels.push(row)
    }
}

function guess(){
    image = []
    for(let r = 0; r < pixels.length; r++){
        var row = []
        for (let c = 0; c < pixels[r].length; c++) {
            const pixel = pixels[r][c];
            var value = 0;
            if(pixel.style.backgroundColor == "rgb(255, 255, 255)"){
                value = 255;
            }else{
                value = 0;
            }
            row.push(value)
        }
        image.push(row)
    }
    callPythonFunction(image)
}

function clear(){
    for(let r = 0; r < pixels.length; r++){
        for(let c = 0; c < pixels[r].length; c++){
            pixels[r][c].style.backgroundColor = "#000000"
        }
    }
}

window.addEventListener("mousedown", function(){
    draw = true
})

window.addEventListener("mouseup", function(){
    draw = false
})

guess_button.addEventListener('click', function(){
    guess();
})

clear_button.addEventListener('click', function(){
    clear()
})

erase_checkbox.addEventListener('click', function(){
    erase = erase_checkbox.checked
})

populate()

// Example function to call your Python endpoint
function callPythonFunction(arg) {
    fetch('http://localhost:5000/call-python', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ arg: arg })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Python response:", data.message);
    })
    .catch(error => console.error('Error:', error));
}

