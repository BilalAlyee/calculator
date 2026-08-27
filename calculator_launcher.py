import sys

try:
    from calculator_ui import Calculator
    GUI_AVAILABLE = True
except Exception as e:
    print('GUI is not available (Kivy missing or failed to launch):', e)
    GUI_AVAILABLE = False

from calculator_math import evaluate_expression


def run_cli():
    angle_mode = 'deg'
    print('Welcome to the Calculator CLI!')
    print('You can type math expressions and commands manually.')
    print('Fallback console calculator running.')
    print('Type expressions (or QUIT/EXIT).')
    print('Use MODE DEG or MODE RAD to switch angle mode.')
    while True:
        try:
            expr = input('calc> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nExiting.')
            break

        if not expr:
            continue
        lower = expr.lower()
        if lower in ('quit', 'exit'):
            print('Exiting.')
            break
        if lower.startswith('mode '):
            mode = lower.split(' ', 1)[1]
            if mode in ('deg', 'rad'):
                angle_mode = mode
                print('Angle mode set to', angle_mode)
            else:
                print('Mode must be DEG or RAD')
            continue

        try:
            result = evaluate_expression(expr, angle_mode=angle_mode)
            print(result)
        except Exception as err:
            print('Error:', err)


def print_usage():
    print('Usage: calculator_launcher.py [--gui | --cli]')
    print('  --gui : attempt to run Kivy GUI (requires kivy installed)')
    print('  --cli : run console mode regardless of GUI availability')
    print('  no args: GUI if available, else CLI fallback')

if __name__ == '__main__':
    args = sys.argv[1:]
    force_mode = None
    if len(args) > 1:
        print_usage()
        sys.exit(1)
    if len(args) == 1:
        if args[0] == '--gui':
            force_mode = 'gui'
        elif args[0] == '--cli':
            force_mode = 'cli'
        elif args[0] in ('-h', '--help'):
            print_usage(); sys.exit(0)
        else:
            print('Unknown argument:', args[0])
            print_usage(); sys.exit(1)

    if force_mode == 'cli':
        run_cli()
    elif force_mode == 'gui':
        if not GUI_AVAILABLE:
            print('GUI is not available (kivy missing). Use --cli for console mode.')
            sys.exit(1)
        Calculator().run()
    else:
        if GUI_AVAILABLE:
            try:
                Calculator().run()
            except Exception as e:
                print('Failed to run GUI, falling back to CLI:', e)
                run_cli()
        else:
            run_cli()
