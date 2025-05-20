const container = document.querySelector('.container')
const guess_button = document.querySelector('.guess_button')
const clear_button = document.querySelector('.clear_button')
const erase_checkbox = document.querySelector('.erase')
const dropdown = document.querySelector('#model_selector')
const guessP = document.querySelector('#guess')
const analysisP = document.querySelector(".analysisP")

const API_BASE = window.location.hostname.includes("127.0.0.1")
  ? "http://localhost:5000"
  : "https://passion-project-0z09.onrender.com";

var pixels = []
var image = []

var draw = false;
var guessing = false;
var erase = false;

//Grayscale brush affect
function brush(r, c){
    for(let row = Math.max(r-1, 0); row < Math.min(r+2,28); row++){
        for(let col = Math.max(c-1, 0); col < Math.min(c+2, 28); col++){
            if(!(row == r && col == c)){
                values = getRGBValues(pixels[row][col].style.backgroundColor)
                pixels[row][col].style.backgroundColor = "rgb(" + Math.min(values[0] + 63,255) + "," + Math.min(values[1] + 63,255) + "," + Math.min(values[2] + 63,255) + ")"
            }
        }
    }
}

//Sets up grid
function populate() {
    //populates it with pixels
    for (let r = 0; r < 28; r++) {
        var row = []
        for(let c = 0; c < 28; c++){
            const div = document.createElement('div')
            div.classList.add('pixel')
            div.style.backgroundColor = "#000000"
            div.dataset.row = r
            div.dataset.col = c
            row.push(div)
            container.appendChild(div)
        }
        pixels.push(row)
    }

    //adds event listeners for every pixel
    for(let r = 0; r < pixels.length; r++){
        for(let c = 0; c < pixels[r].length; c++){
            let div = pixels[r][c]
            div.addEventListener('mouseover',function(){
                if(!draw) return //no mouseclick
                if(guessing) return //
                if (erase){ //Erasing
                    div.style.backgroundColor = '#000000'
                }else{//Draw
                    div.style.backgroundColor = '#ffffff'
                    brush(r, c)
                }
            })
            div.addEventListener('click',function(){
                if(guessing) return
                if (erase) div.style.backgroundColor = '#000000'
                else div.style.backgroundColor = '#ffffff'
            })
        }
    }
}

function populateDropdown(arr){
    for(let i = 0; i < arr.length; i++){
        const option = document.createElement('option')
        option.value = arr[i];
        option.innerHTML = arr[i];
        dropdown.appendChild(option)
    }
}

function populateAnalysis(arr){
    analysisP.innerHTML = arr
}

//Helper function to get rgb values as array from string
function getRGBValues(rgbString) {
    const values = rgbString.substring(4, rgbString.length - 1).split(',').map(Number);
    return values;
}

//Gets image values and sends request for network
function guess(){
    image = []
    for(let r = 0; r < pixels.length; r++){
        var row = []
        for (let c = 0; c < pixels[r].length; c++) {
            const pixel = pixels[r][c];
            var value = 0;
            value = getRGBValues(pixel.style.backgroundColor)[0]
            row.push(value)
        }
        image.push(row)
    }//Gets the image as 2D array filled with [0,255] values
    callNetwork(image)//Calls the python
    guessP.innerHTML = "Guessing"
}

function showGuess(letter){
    guessP.innerHTML = letter
}

//clears the canvas
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

dropdown.addEventListener('click', function(){
    getAnalysis(dropdown.value)
})

populate()
getFiles()
getAnalysis(dropdown.value)

// Example function to call your Python endpoint
function callNetwork(arg) {
    fetch(`${API_BASE}/call-network`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ arg: arg , model: dropdown.value})
    })
    .then(response => response.json())
    .then(data => {
        showGuess(data.message);
    })
    .catch(error => console.error('Error:', error));
}

// Example function to call your Python endpoint
function getFiles() {
    fetch(`${API_BASE}/call-files`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ arg: "" })
    })
    .then(response => response.json())
    .then(data => {
        populateDropdown(data.message);
    })
    .catch(error => console.error('Error:', error));
}

// Example function to call your Python endpoint
function getAnalysis(arg) {
    fetch(`${API_BASE}/call-analysis`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ arg: arg })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        populateAnalysis(data.message);
    })
    .catch(error => console.error('Error:', error));
}
