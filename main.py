from tkinter import *
import math


PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 0.1
SHORT_BREAK_MIN = 0.1
LONG_BREAK_MIN = 0.1
reps = 0
timer = None
current_time = 0


def reset_timer():
    global timer, reps, current_time
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00", fill="white")
    title_label.config(text="Pomodoro Timer", fg=GREEN)
    check_marks.config(text="")
    canvas.itemconfig(cat_image, image=cat_start)
    reps = 0
    current_time = 0


def start_timer():
    global reps, current_time
    if not(current_time > 0):
        reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if current_time > 0:
        if reps % 4 == 0:
            title_label.config(text="  Long Break  ", fg=RED)
            canvas.itemconfig(cat_image, image=cat_sleep)
            canvas.itemconfig(timer_text, fill=RED)
        elif reps % 2 == 0:
            title_label.config(text=" Short Break  ", fg=PINK)
            canvas.itemconfig(cat_image, image=cat_relaxing)
            canvas.itemconfig(timer_text, fill=PINK)
        else:
            title_label.config(text=" Time To Work ", fg=GREEN)
            canvas.itemconfig(cat_image, image=cat_studying)
            canvas.itemconfig(timer_text, fill=GREEN)
        count_down(current_time)
    elif reps % 4 == 0:
        count_down(long_break_sec)
        title_label.config(text="  Long Break  ", fg=RED)
        canvas.itemconfig(cat_image, image=cat_sleep)
        canvas.itemconfig(timer_text, fill=RED)

    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text=" Short Break  ", fg=PINK)
        canvas.itemconfig(cat_image, image=cat_relaxing)
        canvas.itemconfig(timer_text, fill=PINK)
    else:
        count_down(work_sec)
        title_label.config(text=" Time To Work ", fg=GREEN)
        canvas.itemconfig(cat_image, image=cat_studying)
        canvas.itemconfig(timer_text, fill=GREEN)


def pause_timer():
    global current_time
    window.after_cancel(timer)
    title_label.config(text="    Paused    ", fg=RED)
    canvas.itemconfig(cat_image, image=cat_pause)
    canvas.itemconfig(timer_text, fill=RED)


def count_down(count):
    global current_time
    current_time = count

    count_min = math.floor(count / 60)
    count_sec = math.trunc(count % 60)

    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✓"
        check_marks.config(text=marks)


window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = Label(text="Pomodoro Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=500, height=500, bg=YELLOW, highlightthickness=0)

cat_start = PhotoImage(file="peach-goma.png")
cat_start = cat_start.zoom(25)
cat_start = cat_start.subsample(20)

cat_studying = PhotoImage(file="peach-cat-study.png")
cat_studying = cat_studying.zoom(25)
cat_studying = cat_studying.subsample(32)

cat_relaxing = PhotoImage(file="peach-goma-relaxing.png")
cat_relaxing = cat_relaxing.zoom(25)
cat_relaxing = cat_relaxing.subsample(40)

cat_sleep = PhotoImage(file="peach-goma-sleep.png")
cat_sleep = cat_sleep.zoom(25)
cat_sleep = cat_sleep.subsample(25)

cat_pause = PhotoImage(file="peach-goma-pause.png")
cat_pause = cat_pause.zoom(25)
cat_pause = cat_pause.subsample(40)

cat_image = canvas.create_image(250, 250, image=cat_start)
timer_text = canvas.create_text(250, 80, text="00:00", fill="white", font=(FONT_NAME, 45, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

pause_button = Button(text="Pause", highlightthickness=0, command=pause_timer)
pause_button.grid(column=1, row=2)

check_marks = Label(text="✓", fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

window.mainloop()


