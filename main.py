import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):  # Function to start, refresh and clear the screen when it has to
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to start!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0): # Function to display the text that has to be written and the text that we're typing
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}") # Words per minute display

    for i, char in enumerate(current):  # We make sure if the character that we're typing is the correct one
        correct_char = target[i] # If it is...
        color = curses.color_pair(1)  # ... then it's green (line 63)
        if char != correct_char:  # Else...
            color = curses.color_pair(2)  # ... it's red (line 64)

        stdscr.addstr(0, i, char, color) # Display the letters in the screen

def load_text():  # Load personalized text to the program
    with open("test_text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip() # It randomly chooses the line we're gonna work with

def wpm_test(stdscr): # Function to calculate the words per minute
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:

        time_elapsed = max(time.time() - start_time, 1)

        # formula to calculate the wpm
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        # Constantly shows the actualized wpm in the moment
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # We make sure we have the same sentence as the target_text so we stop the timer
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        # Because of the stdscr.nodelay(True) instruction, in case we don't enter a key, the program would stop, but doing this we get rid of it
        try:
            key = stdscr.getkey()
        except:
            continue  # so it continues

        if ord(key) == 27:       # Escape key  (ASCII)
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr): # main function which calls all the others function to start

    #initializing and storing the colors that we'll use
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)

        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

# Wrapper makes everything work well according to the curses module/library
wrapper(main)
