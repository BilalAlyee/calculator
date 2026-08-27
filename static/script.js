// State - supports unlimited calculations
const state = {
    display: document.getElementById('display'),
    currentInput: '',
    lastResult: null,
    history: [],
    locale: navigator.language || 'en-US',
    maxInputLength: 10000  // Allow very long expressions
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    updateDisplay();
});

// Toggle history panel on mobile
function toggleHistory() {
    const panel = document.getElementById('historyPanel');
    panel.classList.toggle('show');
}

// Load history from localStorage
function loadHistory() {
    const saved = localStorage.getItem('calcHistory');
    if (saved) {
        state.history = JSON.parse(saved);
        displayHistory();
    }
}

// Input functions
function appendNumber(num) {
    if (state.currentInput.length < state.maxInputLength) {
        state.currentInput += num;
        updateDisplay();
    }
}

function appendOperator(op) {
    if (state.currentInput === '' && state.lastResult !== null) {
        state.currentInput = String(state.lastResult);
    }
    if (state.currentInput !== '' && !endsWithOperator()) {
        state.currentInput += op;
        updateDisplay();
    }
}

function appendFunction(func) {
    if (state.currentInput.length < state.maxInputLength - 5) {
        if (func === 'fact') {
            state.currentInput += '!';
        } else {
            state.currentInput += func + '(';
        }
        updateDisplay();
    }
}

function appendValue(value) {
    state.currentInput += (value === 'pi' ? 'pi' : 'e');
    updateDisplay();
}

function appendDecimal(dot) {
    if (state.currentInput === '' || endsWithOperator()) {
        state.currentInput += '0.';
    } else if (!getCurrentNumber().includes('.')) {
        state.currentInput += dot;
    }
    updateDisplay();
}

function appendOpenParen(paren) {
    state.currentInput += paren;
    updateDisplay();
}

function appendCloseParen(paren) {
    state.currentInput += paren;
    updateDisplay();
}

function clearDisplay() {
    state.currentInput = '';
    state.lastResult = null;
    updateDisplay();
}

function deleteCharacter() {
    state.currentInput = state.currentInput.slice(0, -1);
    updateDisplay();
}

function getCurrentNumber() {
    const lastOpIndex = Math.max(
        state.currentInput.lastIndexOf('+'),
        state.currentInput.lastIndexOf('-'),
        state.currentInput.lastIndexOf('*'),
        state.currentInput.lastIndexOf('/'),
        state.currentInput.lastIndexOf('^')
    );
    return state.currentInput.substring(lastOpIndex + 1);
}

function endsWithOperator() {
    return /[+\-*/^÷×−]$/.test(state.currentInput);
}

function updateDisplay() {
    state.display.value = state.currentInput || '0';
}

// Calculate
function calculate() {
    if (state.currentInput === '') return;
    
    const angleMode = document.querySelector('input[name="angle_mode"]:checked').value;
    const originalExpression = state.currentInput;
    
    // Convert to Python syntax
    let expression = state.currentInput
        .replace(/\^/g, '**')
        .replace(/÷/g, '/')
        .replace(/×/g, '*')
        .replace(/−/g, '-')
        .replace(/(\d)\!/g, 'fact($1)')  // n! to fact(n)
        .replace(/\)\!/g, ')!');  // )! to )!

    fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expression, angle_mode: angleMode })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            state.display.value = 'Error';
            state.currentInput = '';
        } else {
            state.lastResult = data.result;
            
            // Add to history
            state.history.unshift({
                expression: originalExpression,
                result: data.result,
                timestamp: new Date().toLocaleTimeString(state.locale)
            });
            
            if (state.history.length > 50) state.history.pop();
            localStorage.setItem('calcHistory', JSON.stringify(state.history));
            displayHistory();
            
            state.currentInput = String(data.result);
            updateDisplay();
        }
    })
    .catch(() => {
        state.display.value = 'Error';
        state.currentInput = '';
    });
}

// History
function displayHistory() {
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = state.history.map(item => `
        <div class="history-item" onclick="selectHistory(${state.history.indexOf(item)})">
            <div class="history-expression">${item.expression}</div>
            <div class="history-result">= ${item.result}</div>
        </div>
    `).join('');
}

function selectHistory(index) {
    const item = state.history[index];
    state.currentInput = String(item.result);
    state.lastResult = item.result;
    updateDisplay();
}

function clearHistory() {
    if (confirm('Clear all history?')) {
        state.history = [];
        localStorage.removeItem('calcHistory');
        displayHistory();
    }
}

// Keyboard
document.addEventListener('keydown', e => {
    if (e.key === 'Enter') calculate();
    else if (e.key === 'Escape') clearDisplay();
    else if (e.key === 'Backspace') deleteCharacter();
    else if (/^[0-9]$/.test(e.key)) appendNumber(e.key);
    else if (['+', '-', '*', '/'].includes(e.key)) appendOperator(e.key);
    else if (e.key === '^') appendOperator('^');
    else if (e.key === '.') appendDecimal('.');
    else if (e.key === '(') appendOpenParen('(');
    else if (e.key === ')') appendCloseParen(')');
    else if (e.key === '%') appendOperator('mod');
    else if (e.key === '!') appendFunction('fact');
});
