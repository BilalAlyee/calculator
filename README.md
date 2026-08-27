# 🧮 Scientific Calculator Web App

A professional, responsive scientific calculator web application built with Flask, HTML5, CSS3, and vanilla JavaScript. Features a modern UI and full scientific computing capabilities.

## ✨ Features

- **Scientific Functions**: Trigonometric, logarithmic, exponential, hyperbolic functions
- **Advanced Operations**: Factorials, roots (square & cube), modulo, power operations
- **Multiple Modes**: Degree/Radian angle mode support
- **Calculation History**: Persistent history with localStorage, scrollable panel
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **International Support**: Automatic locale-based number formatting
- **Keyboard Support**: Full keyboard input (Enter to calculate, Escape to clear, etc.)
- **Professional UI**: Clean, modern gradient design with color-coded buttons

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/BilalAlyee/calculator.git
cd calculator
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## 📦 Project Structure

```
calculator/
├── app.py                 # Flask backend server
├── calculator_math.py     # Mathematical functions & safe evaluation
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration (Render, Heroku)
├── runtime.txt           # Python version specification
├── templates/
│   └── index.html        # Main HTML interface
├── static/
│   ├── style.css         # Professional styling
│   └── script.js         # Calculator logic & interactions
└── README.md             # Documentation
```

## 🔧 Supported Functions

### Trigonometric
- `sin()`, `cos()`, `tan()`
- `asin()`, `acos()`, `atan()`

### Hyperbolic
- `sinh()`, `cosh()`, `tanh()`

### Logarithmic & Exponential
- `log()` - Base 10
- `ln()` - Natural logarithm
- `exp()` - e^x

### Other Functions
- `sqrt()` - Square root
- `cbrt()` - Cube root
- `abs()` - Absolute value
- `fact()` or `n!` - Factorial
- `mod` - Modulo operation
- `()` - Parentheses for grouping

### Constants
- `pi` - π (Pi)
- `e` - Euler's number

## 🎮 Usage

### Mouse/Touch
- Click buttons to input numbers and operations
- Click `=` to calculate
- Click `C` to clear
- Click history items to reuse previous results

### Keyboard
- `0-9` - Number input
- `+ - * /` - Operations
- `^` - Power operation
- `.` - Decimal point
- `Enter` - Calculate
- `Escape` - Clear display
- `Backspace` - Delete last character
- `%` - Modulo
- `!` - Factorial
- `( )` - Parentheses

## 🌐 Deployment

### Render.com (Recommended - Free)
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service from GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Deploy!

### Local Development
```bash
python app.py
```

### Production
```bash
gunicorn app:app
```

## 📝 Examples

```
5! + sqrt(16)          → 29
sin(90)                → 1 (DEG mode)
log(100)               → 2
2^10                   → 1024
abs(-42)               → 42
10 mod 3               → 1
(3 + 4) * 2            → 14
```

## 🛠️ Technology Stack

- **Backend**: Python 3.14, Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: Browser LocalStorage (history)
- **Deployment**: Render, Heroku compatible

## 📊 Browser Support

- Chrome/Edge (Latest)
- Firefox (Latest)
- Safari (Latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🔒 Security

- Safe expression evaluation using restricted `eval()` environment
- No external vulnerabilities
- CSRF protection via Flask
- Input validation on all calculations

## 📱 Responsive Breakpoints

- **Desktop**: 1024px+ (side-by-side layout)
- **Tablet**: 768px - 1023px (stacked layout)
- **Mobile**: < 768px (mobile-optimized with collapsible history)

## 🐛 Bug Reports

Found an issue? Open an issue on GitHub!

## 📄 License

MIT License - Feel free to use for personal and commercial projects.

## 👨‍💻 Author

Bilal Alyee

---

**Live Demo**: Visit the calculator app online after deployment 

Enjoy calculating! 🧮✨
