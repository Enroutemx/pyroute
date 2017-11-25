import sys
import time
import os
import traceback

from itertools import cycle
from pyroute.utils import Threaded
from pyroute.errors import *

class Logger(object):

    _threads = []

    def __init__(self):
        self.start()

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
    
    # Decorator to output something because of an errer, this does not work as intended yet. 
    # A debbugger or similar is missing.
    @classmethod
    def on_error(cls, action, message):
        def processed_func(fn):
            def wrapper(*args, **kwargs):
                if action is "log":
                    Logger.__handle_exc(message, fn, *args, **kwargs)
            return wrapper
        return processed_func
    
    # Exception formatter, used by the above decorator.
    @classmethod
    def __handle_exc(message, fn, *args, **kwargs):
        try:
            fn(*args, **kwargs)
        except MethodNotFoundError:
            Logger.failure(message)
        # List custom exceptions here
        except:
            pass

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
    def process(self, message, processed_func, *args, **kwargs):
        IO.process_start()
        IO.use_symbol("[ \\ ],[ | ],[ / ],[ — ]")
        IO.fancy_print(message)
        processed = processed_func(*args, **kwargs)
        IO.process_end()
        return processed

    # Display a message with a custom symbol and optional timeout
    def custom(self, symbol, message, timeout=None):
        IO.use_symbol(symbol)
        IO.static_print(message)
        if timeout is not None:
            IO.wait(timeout)
        IO.new_line()

    # Animated version of the above, takes a comma-separated string
    # of symbols, the message and optionally the timeout and fps
    def custom_animated(self, symbols, message, timeout=None, speed=10):
        IO.process_start()
        IO.use_symbol(symbols)
        IO.fancy_print(message, speed)
        if timeout is not None:
            IO.wait(timeout)
        IO.process_end()

    # Just a separator with an optional label
    def separate(self, label=None, sep='-'):
        IO.new_line()
        IO.draw_separator(label, sep)
        IO.new_line()
        IO.new_line()

    # Display an error
    def error(self, error_message):
        IO.use_symbol("[ ✘ ]")
        IO.static_print(error_message)
        IO.new_line()

    # Display a failure
    @classmethod
    def failure(cls, error):
        IO.use_symbol("[!!!]")
        IO.static_print(error.message)
        IO.last_command_print()
        IO.simple_print(error.location + " ->> ")
        IO.simple_print(error.command)
        IO.new_line()

class IO(object):

    _process_complete = False
    _threads = []
    symbol = []
    symbol_completed = ["[ ✔ ]"]
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

    # Prints the last command executed, for debugging.
    @classmethod
    def last_command_print(cls):
        sys.stdout.write('\n')
        sys.stdout.write("\x1b[4G")
        sys.stdout.write("└─┬─┘         \n")
        sys.stdout.write("\x1b[3C")
        sys.stdout.write("  └────────>  ")
        sys.stdout.flush()

class Timer(object):
    def __init__(self):
        pass

    def start(self):
        Timer.starttime = time.time()

    def stop(self):
        Timer.endtime = time.time()

    def elapsed_time(self):
        return Timer.endtime - Timer.starttime
