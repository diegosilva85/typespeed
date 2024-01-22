from tkinter import *
from random import shuffle

# CONSTANTS ------------------------------------------------------------------------------------------------------------
ENTRY_WIDTH = 8
FONT = ("Arial", 16, "normal")
PADDING = 10
TIMER = 60
WORDS_COUNTER = 0
CHARACTER_COUNT = 0
GREEN_COLOR = "#D4E7C5"
MAIN_COLOR = "#F9EFDB"

WORDS_LIST = [
    'the', 'quick', 'brown', 'fox', 'jumped', 'over', 'lazy', 'dog', 'cat', 'deer', 'computer', 'python', 'key',
    'mouse', 'tablet', 'skill', 'challenge', 'question', 'answer', 'version', 'control', 'debug', 'mobile',
    'apple', 'android', 'device', 'knee', 'eye', 'car', 'vector', 'bitmap', 'font', 'palette', 'pixel', 'camel',
    'gradient', 'exception', 'speed', 'text', 'image', 'challenge', 'productivity', 'performance', 'optimization',
    'browser', 'internet', 'while', 'get', 'easy', 'go', 'of', 'under', 'who', 'with', 'without', 'orange', 'grape',
    'red', 'blue', 'yellow', 'green', 'tomato', 'pasta', 'ball', 'east', 'north', 'south', 'west', 'gorilla',
    'service', 'skateboard', 'game', 'mushroom', 'shrimp', 'rice', 'skeleton', 'fifteen', 'hospital', 'zelda',
    'roof', 'tuesday', 'woman', 'volley', 'kid', 'football', 'point', 'score', 'lava', 'earth', 'jupiter', 'banana',
    'juice', 'week', 'surprise', 'yield', 'x-ray', 'coast', 'beach', 'dragon', 'sound', 'video', 'cube', 'triangle',
    'photo', 'eraser', 'root', 'square', 'circle', 'opal', 'connector', 'library', 'product', 'bag', 'lion', 'shield',
    'sword', 'castle', 'spaceship', 'sky', 'country', 'city', 'building', 'airplane', 'legend', 'religion', 'exercise',
    'petal', 'friend', 'speak', 'enter', 'book', 'girl', 'movie', 'saturday', 'dance', 'color', 'chair', 'desktop'
]
CHOSEN_LIST = []

with open('records.txt', 'r') as file:
    record = file.read()


def handle_text(*args):
    global words, WORDS_COUNTER, CHARACTER_COUNT
    entered_text = entry_var.get()  # Gets the typed letter
    current_target_word = CHOSEN_LIST[0][:len(entered_text)]  # Gets the length of the word as the user types
    if entered_text == current_target_word:  # Check if the typing word is correct or wrong
        typing_entry.config(fg='green')  # The text becomes green as the user types, if correct
        if len(entered_text) == len(CHOSEN_LIST[0]):  # Full word completed
            words = words.replace(CHOSEN_LIST[0], '')  # Erase the complete word from the concatenated string
            words_label.config(text=words)  # Update the complete word for the UI
            CHARACTER_COUNT += len(CHOSEN_LIST[0])
            WORDS_COUNTER += 1  # Increment counter of completed words
            del CHOSEN_LIST[0]  # Delete word from the main list of chosen words
            if CHOSEN_LIST:  # Check if there's still words left
                entry_var.set("")  # Clear the entered text for the new word
            else:  # Generate a whole new set of words
                words = concatenate_chosen_words(generate_words())
                words_label.config(text=words)
                entry_var.set("")
    else:
        typing_entry.config(fg='red')  # Text becomes red if the user makes a mistake


def generate_words():
    shuffle(WORDS_LIST)
    for word in WORDS_LIST:
        CHOSEN_LIST.append(word)
        WORDS_LIST.remove(word)
        if len(CHOSEN_LIST) == 30:
            break
    return CHOSEN_LIST


def concatenate_chosen_words(words_list: list) -> str:
    list_to_modify = words_list.copy()
    for i in range(0, 30):
        if i % 7 == 0 and i != 0:
            list_to_modify.insert(i, "\n")
    return '  '.join(list_to_modify)


def timer_function(counter: int):
    global flag_for_timer
    if flag_for_timer:
        entry_var.trace_remove('write', trace_for_timer)
        flag_for_timer = False
    count = counter
    time_counter.config(text=counter)
    timer = window.after(1000, timer_function, count - 1)
    if count == 0:
        window.after_cancel(timer)
        typing_entry.config(state=DISABLED)
        see_results()


def restart():
    global flag_for_timer, trace_for_timer, words,CHARACTER_COUNT, WORDS_COUNTER
    CHARACTER_COUNT = 0
    WORDS_COUNTER = 0
    typing_entry.config(state=NORMAL)
    flag_for_timer = True
    words = concatenate_chosen_words(generate_words())
    words_label.config(text=words)
    trace_for_timer = entry_var.trace_add("write", lambda *args: timer_function(TIMER))


def see_results():
    wpm_value.config(text=str(WORDS_COUNTER))
    cpm_value.config(text=str(CHARACTER_COUNT))
    if CHARACTER_COUNT > int(record):
        best_value.config(text=str(CHARACTER_COUNT))
        with open('records.txt', 'w') as file2:
            file2.write(str(CHARACTER_COUNT))


# SET UP THE WORDS LIST
words = concatenate_chosen_words(generate_words())

# UI INITIALIZATION ----------------------------------------------------------------------------------------------------
window = Tk()
window.title("TypeSpeed")
entry_var = StringVar()
entry_var.trace_add("write", handle_text)
trace_for_timer = entry_var.trace_add("write", lambda *args: timer_function(TIMER))
flag_for_timer = True

best_time_label = Label(window, text="Best CPM", font=FONT, padx=PADDING)
best_time_label.grid(column=0, row=0)

char_per_min_label = Label(window, text="CPM", font=FONT, padx=PADDING)
char_per_min_label.grid(row=0, column=2)

word_per_min_label = Label(window, text="WPM", font=FONT, padx=PADDING)
word_per_min_label.grid(row=0, column=4)

time_lef_label = Label(window, text="Time Left", font=FONT, padx=PADDING)
time_lef_label.grid(row=0, column=6)

# MAIN LABEL -----------------------------------------------------------------------------------------------------------
words_label = Label(window, text=words, font=FONT, width=65, height=8, relief=SOLID,
                    borderwidth=1, bg=MAIN_COLOR)
words_label.grid(row=1, column=0, columnspan=8)

# LABELS FOR THE VALUES ------------------------------------------------------------------------------------------------
best_value = Label(window, width=ENTRY_WIDTH, text=record, font=FONT, relief=SOLID, borderwidth=1)
best_value.grid(row=0, column=1)

cpm_value = Label(window, width=ENTRY_WIDTH, font=FONT, relief=SOLID, borderwidth=1)
cpm_value.grid(row=0, column=3)

wpm_value = Label(window, width=ENTRY_WIDTH, font=FONT, relief=SOLID, borderwidth=1)
wpm_value.grid(row=0, column=5)

time_counter = Label(window, width=ENTRY_WIDTH, font=FONT, relief=SOLID, borderwidth=1)
time_counter.grid(row=0, column=7)

# TEXT ENTRY -----------------------------------------------------------------------------------------------------------
typing_entry = Entry(window, width=25, font=FONT, textvariable=entry_var)
typing_entry.grid(row=2, column=0, columnspan=8)

# RESTART BUTTON -------------------------------------------------------------------------------------------------------
restart_button = Button(window, text="Restart", command=restart, bg=GREEN_COLOR)
restart_button.grid(row=2, column=7)


window.mainloop()
