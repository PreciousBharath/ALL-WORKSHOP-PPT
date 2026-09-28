// Day 17 - DOM Manipulation and Event Handling

// ===== 1. DOM SELECTION =====

function selectDOMElements() {
    // getElementById
    const para = document.getElementById('target-paragraph');
    console.log("getElementById:", para);

    // getElementsByClassName
    const boxes = document.getElementsByClassName('box');
    console.log("getElementsByClassName:", boxes);

    // querySelector (CSS selector - returns first match)
    const firstBox = document.querySelector('.box');
    console.log("querySelector:", firstBox);

    // querySelectorAll (CSS selector - returns all matches)
    const allBoxes = document.querySelectorAll('.box');
    console.log("querySelectorAll:", allBoxes);

    alert('Check console for selection examples!');
}

// ===== 2. MODIFY ELEMENTS =====

function changeText() {
    const box = document.getElementById('modify-box');
    box.textContent = 'Text has been changed!';
}

function changeHTML() {
    const box = document.getElementById('modify-box');
    box.innerHTML = '<strong>HTML has been changed!</strong> <em>This is now HTML content</em>';
}

function toggleClass() {
    const box = document.getElementById('modify-box');
    box.classList.toggle('highlight');
}

function changeAttributes() {
    const para = document.getElementById('target-paragraph');
    para.setAttribute('title', 'New title attribute');
    para.setAttribute('data-custom', 'custom value');
    console.log("Attributes changed!");
}

// ===== 3. CREATE ELEMENTS =====

function addItem() {
    const input = document.getElementById('item-input');
    const itemText = input.value.trim();

    if (itemText === '') {
        alert('Please enter an item!');
        return;
    }

    // Create new list item
    const li = document.createElement('li');
    
    // Create delete button
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.className = 'delete-btn';
    deleteBtn.onclick = function() {
        li.remove();
    };

    // Add text and button to list item
    li.textContent = itemText;
    li.appendChild(deleteBtn);

    // Add to list
    const list = document.getElementById('list-items');
    list.appendChild(li);

    // Clear input
    input.value = '';
    input.focus();
}

// ===== 4. EVENT HANDLING =====

// Get elements
const clickBtn = document.getElementById('click-btn');
const inputField = document.getElementById('input-field');
const slider = document.getElementById('slider');
const sliderValue = document.getElementById('slider-value');
const eventLog = document.getElementById('event-log');

// Click event
clickBtn.addEventListener('click', function() {
    alert('Button clicked!');
    logEvent('Button clicked');
});

// Input event
inputField.addEventListener('input', function(event) {
    console.log("Current input value:", event.target.value);
    logEvent(`Typed: ${event.target.value}`);
});

// Change event (slider)
slider.addEventListener('input', function(event) {
    sliderValue.textContent = event.target.value;
    logEvent(`Slider moved to: ${event.target.value}`);
});

// ===== 5. MOUSE EVENTS =====

const mouseBox = document.getElementById('mouse-box');

mouseBox.addEventListener('mouseenter', function() {
    this.style.backgroundColor = '#4fc3f7';
    this.textContent = 'Mouse entered!';
    logEvent('Mouse entered');
});

mouseBox.addEventListener('mouseleave', function() {
    this.style.backgroundColor = '#e3f2fd';
    this.textContent = 'Mouse over me!';
    logEvent('Mouse left');
});

mouseBox.addEventListener('mousemove', function(event) {
    // Get position relative to the box
    const x = event.offsetX;
    const y = event.offsetY;
    this.textContent = `Position: ${x}, ${y}`;
});

// ===== 6. EVENT DELEGATION =====

const buttonContainer = document.getElementById('button-container');
const colorBox = document.getElementById('color-box');

buttonContainer.addEventListener('click', function(event) {
    if (event.target.classList.contains('color-btn')) {
        const color = event.target.dataset.color;
        colorBox.style.backgroundColor = color;
        logEvent(`Color changed to: ${color}`);
    }
});

// ===== HELPER FUNCTION =====

function logEvent(message) {
    const log = document.getElementById('event-log');
    const li = document.createElement('li');
    const time = new Date().toLocaleTimeString();
    li.textContent = `[${time}] ${message}`;
    log.appendChild(li);
    
    // Keep only last 10 events
    while (log.children.length > 11) {
        log.children[1].remove();
    }
}

// ===== ADDITIONAL EXAMPLES =====

// Keyboard events
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        // Handle Enter key press
    }
});

// Form submission
document.addEventListener('submit', function(event) {
    // event.preventDefault(); // Prevent default form submission
});

// Window events
window.addEventListener('resize', function() {
    console.log('Window resized!');
});

window.addEventListener('scroll', function() {
    // Handle scroll events
});

console.log("All event handlers initialized!");
