import sys
import time
import os
import inspect
import linecache

from itertools import cycle
from pyroute.utils import Threaded
from pyroute.utils import Utils
from pyroute.errors import *

class Logger(object):

    _threads = []

    def __init__(self, config):
        self.config = config
        self.start()
        IO.start(self.config)

    def start(self):
        pass

    @classmethod
    def start_tracing(cls):
        """
        This will keep track of each case and possible errors.
        For now it does nothing.
        """
        sys.settrace(Logger.__tracer)

    @classmethod
    def __tracer(cls, frame, event, arg):
        pass

    @classmethod
    @Threaded(_threads)
    def count_time(cls):
        #Start a threaded timer
        Logger.time_counter = Timer()
        Logger.time_counter.start()
    
    @classmethod
    def elapsed_time(cls):
        # Return the elapsed time and stops the timer.
        Logger.time_counter.stop()
        return Logger.time_counter.elapsed_time()
    
    # Decorator to output and optionally do something because of an error. 
    @classmethod
    def on_error(cls, message=None, action=None):
        def processed_func(fn):
            def wrapper(*args, **kwargs):
                if message is not None:
                    Logger.error(message)
                    error_shown = True
                if action is not None:
                    action()
                if error_shown is True:
                    # Clean up
                    return
                raise
            return wrapper
        return processed_func
    
    # Decorator to display an animation while a function is running
    # Two IO methods, process_start and process_end, are the delimiters
    # of each process, taking care of the wrapped function clean-up, and
    # making sure the Logger is updated accordingly
    @classmethod
    def process_display(cls, message):
        def proccessed_fn(fn):
            def wrapper(*args, **kwargs):
                IO.process_start()
                IO.use_symbol("[ \\ ],[ | ],[ / ],[ — ]")
                IO.fancy_print(message)
                fn(*args, **kwargs)
                IO.process_end()
            return wrapper
        return proccessed_fn
                
    # Non-decorator version of the above
    def process(self, color, message, processed_func, *args, **kwargs):
        IO.set_color(color)
        IO.process_start()
        IO.use_symbol("[ \\ ],[ | ],[ / ],[ — ]")
        IO.fancy_print(message)
        processed = processed_func(*args, **kwargs)
        IO.process_end()
        return processed
        IO.set_color("RESET")

    # Display a message with a custom symbol and optional timeout
    def custom(self, symbol, message, color, timeout=None):
        IO.set_color(color)
        IO.use_symbol(symbol)
        IO.static_print(message)
        IO.set_color("RESET")
        if timeout is not None:
            IO.wait(timeout)
        IO.new_line()

    # Animated version of the above, takes a comma-separated string
    # of symbols, the message and optionally the timeout and fps
    def custom_animated(self, symbols, message, color, timeout=None, speed=10):
        IO.set_color(color)
        IO.process_start()
        IO.use_symbol(symbols)
        IO.fancy_print(message, speed)
        if timeout is not None:
            IO.wait(timeout)
        IO.process_end()
        IO.set_color("RESET")

    # Just a separator with an optional label
    def separate(self, color, label=None, sep='-'):
        IO.set_color(color)
        IO.new_line()
        IO.draw_separator(label, sep)
        IO.new_line()
        IO.new_line()
        IO.set_color("RESET")

    # Display a warning
    @classmethod
    def warning(cls, warning_message):
        IO.set_style_color("warning")
        IO.use_symbol("[-!-]")
        IO.static_print(warning_message)
        IO.new_line()
        IO.set_color("RESET")
        
    # Display an error
    @classmethod
    def error(cls, error_message):
        IO.set_style_color("error")
        IO.use_symbol("[ ✘ ]")
        IO.static_print(error_message)
        IO.new_line()

    # Display a failure
    @classmethod
    def failure(cls, failure_message):
        IO.set_style_color("failure")
        IO.use_symbol("[!!!]")
        IO.static_print(failure_message)
        IO.new_line()
        IO.set_color("RESET")

    @classmethod
    def show_error_location(cls, line, filename, line_span=5):
        min_line = line - line_span if line > line_span else 1
        max_line = line + line_span + 1
        source = []
        for l in range(min_line, max_line):
            source_line = linecache.getline(filename, l)
            if source_line == "": continue
            if l == line:
                source.append("{0}  >>>\t{1}".format(l, source_line))
            else:
                source.append("{0}\t{1}".format(l, source_line))
        IO.show_code(source)
             
class IO(object):
    
    # Dictionary with the ansi codes for terminal color
    # "BRG" stands for bright color
    # "BG" stands for background color
    color = {
        "BLACK": '\u001b[30m',
        "RED": '\u001b[31m',
        "GREEN": '\u001b[32m',
        "ORANGE": '\u001b[33m',
        "BLUE": '\u001b[34m',
        "MAGENTA": '\u001b[35m',
        "CYAN": '\u001b[36m',
        "GREY": '\u001b[37m',
        "BRG_BLACK": '\u001b[30;1m',
        "BRG_RED": '\u001b[31;1m',
        "BRG_GREEN": '\u001b[32;1m',
        "BRG_YELLOW": '\u001b[33;1m',
        "BRG_BLUE": '\u001b[34;1m',
        "BRG_MAGENTA": '\u001b[35;1m',
        "BRG_CYAN": '\u001b[36;1m',
        "BRG_WHITE": '\u001b[37;1m',
        "BG_BLACK": '\u001b[40m',
        "BG_RED": '\u001b[41m',
        "BG_GREEN": '\u001b[42m',
        "BG_YELLOW": '\u001b[43m',
        "BG_BLUE": '\u001b[44m',
        "BG_MAGENTA": '\u001b[45m',
        "BG_CYAN": '\u001b[46m',
        "BG_WHITE": '\u001b[47m',
        "BG_BRG_BLACK": '\u001b[40;1m',
        "BG_BRG_RED": '\u001b[41;1m',
        "BG_BRG_GREEN": '\u001b[42;1m',
        "BG_BRG_YELLOW": '\u001b[43;1m',
        "BG_BRG_BLUE": '\u001b[44;1m',
        "BG_BRG_MAGENTA": '\u001b[45;1m',
        "BG_BRG_CYAN": '\u001b[46;1m',
        "BG_BRG_GREY": '\u001b[47;1m',
        "BOLD": '\u001b[1m',
        "UNDERLINE": '\u001b[4m',
        "RESET": '\u001b[0m',
    }
    _process_complete = False
    _threads = []
    symbol = []
    symbol_completed = ["[ ✔ ]"]
    color_config = ""
    style = []

    @classmethod
    def start(cls, config):
        cls.color_config = config._colors["color"].upper()
        cls.style = config._colors

    @classmethod
    def process_start(cls):
        IO._process_complete = False
        # If a resource queue is implemented, it will be prepared here

    # Update the symbols for a process, and wrap up all IO threads. 
    # The symbol is hard-coded, but should be any symbol to indicate
    # a process status
    @classmethod
    def process_end(cls):
        IO._process_complete = True
        sys.stdout.write("\x1b[7\x1b[9G\x1b[1K\x1b[5D{0}\x1b[8".format(IO.symbol_completed[0]))
        sys.stdout.flush()
        sys.stdout.write('\n')
        sys.stdout.flush()
        Threaded.wrap_up(IO._threads)

    @classmethod
    def wait(cls, timeout):
        time.sleep(timeout)

    @classmethod
    def use_symbol(cls, new_symbol):
        IO.symbol = new_symbol.split(',')

    # Draws a separator line with an optional centered label and separator character
    @classmethod
    def draw_separator(cls, label=None, sep='-'):
        # Get the current terminal width (1). Replace with subprocess.
        width = int(os.popen('stty size', 'r').read().split()[1])
        if label is None: 
            sys.stdout.write(sep * width)
        else:
            label = "{0:^{n}}".format(label, n=(len(label)+12))
            sys.stdout.write(sep * ((width - len(label)) // 2))
            sys.stdout.write(label)
            sys.stdout.write(sep * ((width - len(label)) // 2))
        sys.stdout.flush()

    # Just add a '\n' to the buffer. Some threaded methods use this. 
    @classmethod
    def new_line(cls):
        sys.stdout.write('\n')
        sys.stdout.flush()

    # Print an animation, threaded so any other process continues without issues.
    @classmethod
    @Threaded(_threads)
    def fancy_print(cls, message, fps=10):
        seconds = (len(IO.symbol) / fps) / len(IO.symbol)
        for s in cycle(IO.symbol):
            if IO._process_complete:
                break
            sys.stdout.write("\x1b[4G\x1b[2K{0}\x1b[2C".format(s))
            sys.stdout.write(message)
            sys.stdout.flush()
            time.sleep(seconds)

    # Like the above but non-animated.
    @classmethod
    def static_print(cls, message):
        sys.stdout.write("\x1b[4G\x1b[2K{0}\x1b[2C".format(IO.symbol[0]))
        sys.stdout.write(message)
        sys.stdout.flush()

    # Like the above but without symbols
    @classmethod
    def simple_print(cls, text):
        sys.stdout.write(text)
        sys.stdout.flush()

    @classmethod
    def show_code(cls, list_of_str):
        length = len(max(list_of_str, key=len)) * 2 - 1
        IO.last_command_print()
        for line in list_of_str:
            IO.move_cursor_to_c(6)
            sys.stdout.write('│')
            IO.move_cursor_forward(1)
            sys.stdout.write(line)
        IO.move_cursor_to_c(6)
        sys.stdout.write('└' + '─' * length + '\n')
        sys.stdout.flush()
        
    
    # Prints the last command executed, for debugging.
    @classmethod
    def last_command_print(cls):
        IO.move_cursor_to_c(4)
        sys.stdout.write("──┬──\n")
        IO.move_cursor_to_c(4)
        sys.stdout.write("  │  \n")
        sys.stdout.flush()

    @classmethod
    def move_cursor_to_c(cls, n):
        sys.stdout.write("\x1b[{}G".format(n))

    @classmethod
    def move_cursor_forward(cls, n):
        sys.stdout.write("\x1b[{}C".format(n))
        
    @classmethod
    def move_cursor_backward(cls, n):
        sys.stdout.write("\x1b[{}D".format(n))
        
    @classmethod
    def reset_cursor(cls):
        sys.stdout.write("\x1b[u")

    @classmethod
    def set_color(cls, color):
        if cls.color_config == "ON":
            sys.stdout.write(IO.color[color.upper()])
        else:
            pass

    @classmethod
    def set_style_color(cls, style):
        if cls.color_config == "ON":
            sys.stdout.write(IO.color[IO.style[style].upper()])
        else:
            pass

class Timer(object):
    def __init__(self):
        pass

    def start(self):
        Timer.starttime = time.time()

    def stop(self):
        Timer.endtime = time.time()

    def elapsed_time(self):
        return Timer.endtime - Timer.starttime

def _handle_exc(exc_type, exc_value, exc_traceb):
    """
    Overrides Python's error handling for Pyroute Exceptions, and only Pyroute 
    Exceptions (including Modules)
    """
    exc_message = str(exc_value) if str(exc_value) != "" else str(exc_type.__name__)
    exc_traceinfo = inspect.getinnerframes(exc_traceb)[-2]
    if issubclass(exc_type, KeyboardInterrupt):
        Logger.warning("Aborted!")
        return
    if issubclass(exc_type, PyrouteException):
        Logger.error(exc_message)
        Logger.show_error_location(exc_traceinfo.lineno, exc_traceinfo.filename)
        return
    if issubclass(exc_type, Exception):
        Logger.failure(exc_message)
        #IO.draw_separator(label=" Python's Traceback ")
        IO.new_line()
        #sys.__excepthook__(exc_type, exc_value, exc_traceb)
        #IO.draw_separator()
        #IO.new_line()
        return

sys.excepthook = _handle_exc
