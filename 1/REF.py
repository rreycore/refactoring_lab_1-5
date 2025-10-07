from tkinter import *
from tkinter import messagebox

# Функция для добавления заметки
def add_notes():
    today = date_entry.get()
    notes_title = notes_title_entry.get()
    notes = notes_entry.get("1.0", "end-1c")
    
    if len(today) <= 0 or len(notes_title) <= 0 or len(notes) <= 0:
        messagebox.showerror(message="ENTER REQUIRED DETAILS")
    else:
        # Открываем файл для добавления заметки
        with open("notes.txt", "a", encoding="utf-8") as file:
            file.write(f"{today} | {notes_title} | {notes}\n")
        messagebox.showinfo(message="Note added")

# Функция для отображения всех заметок
def view_notes():
    date = date_entry.get()
    notes_title = notes_title_entry.get()
    
    try:
        with open("notes.txt", "r", encoding="utf-8") as file:
            notes = file.readlines()
        
        matching_notes = []
        for note in notes:
            # Проверяем, есть ли символ " | ", чтобы избежать ошибки распаковки
            parts = note.strip().split(" | ")
            if len(parts) == 3:
                note_date, note_title, note_text = parts
                if (len(date) == 0 or date == note_date) and (len(notes_title) == 0 or notes_title == note_title):
                    matching_notes.append(note)
        
        if matching_notes:
            for note in matching_notes:
                note_date, note_title, note_text = note.split(" | ")
                messagebox.showinfo(message=f"Date: {note_date}\nTitle: {note_title}\nNotes: {note_text}")
        else:
            messagebox.showerror(message="No note found")
    except FileNotFoundError:
        messagebox.showerror(message="No notes file found")

# Функция для удаления заметок
def delete_notes():
    date = date_entry.get()
    notes_title = notes_title_entry.get()
    
    try:
        with open("notes.txt", "r", encoding="utf-8") as file:
            notes = file.readlines()

        new_notes = []
        for note in notes:
            parts = note.strip().split(" | ")
            if len(parts) == 3:
                note_date, note_title, note_text = parts
                if not (date == note_date and notes_title == note_title):
                    new_notes.append(note)

        if len(new_notes) == len(notes):
            messagebox.showerror(message="No matching notes to delete")
        else:
            with open("notes.txt", "w", encoding="utf-8") as file:
                file.writelines(new_notes)
            messagebox.showinfo(message="Note(s) Deleted")
    except FileNotFoundError:
        messagebox.showerror(message="No notes file found")

# Функция для обновления заметки
def update_notes():
    today = date_entry.get()
    notes_title = notes_title_entry.get()
    notes = notes_entry.get("1.0", "end-1c")
    
    if len(today) <= 0 or len(notes_title) <= 0 or len(notes) <= 0:
        messagebox.showerror(message="ENTER REQUIRED DETAILS")
    else:
        try:
            with open("notes.txt", "r", encoding="utf-8") as file:
                notes_list = file.readlines()

            new_notes = []
            updated = False
            for note in notes_list:
                parts = note.strip().split(" | ")
                if len(parts) == 3:
                    note_date, note_title, note_text = parts
                    if date == note_date and notes_title == note_title:
                        new_notes.append(f"{today} | {notes_title} | {notes}\n")
                        updated = True
                    else:
                        new_notes.append(note)

            if updated:
                with open("notes.txt", "w", encoding="utf-8") as file:
                    file.writelines(new_notes)
                messagebox.showinfo(message="Note Updated")
            else:
                messagebox.showerror(message="No matching note found to update")
        except FileNotFoundError:
            messagebox.showerror(message="No notes file found")

# Создание графического интерфейса
window = Tk()
window.geometry("500x300")
window.title("Pin Your Note -TechVidvan")

title_label = Label(window, text="Pin Your Note -TechVidvan").pack()

# Ввод данных
date_label = Label(window, text="Date:").place(x=10, y=20)
date_entry = Entry(window, width=20)
date_entry.place(x=50, y=20)

notes_title_label = Label(window, text="Notes title:").place(x=10, y=50)
notes_title_entry = Entry(window, width=30)
notes_title_entry.place(x=80, y=50)

notes_label = Label(window, text="Notes:").place(x=10, y=90)
notes_entry = Text(window, width=50, height=5)
notes_entry.place(x=60, y=90)

# Кнопки для взаимодействия с заметками
button1 = Button(window, text='Add Notes', bg='Turquoise', fg='Red', command=add_notes).place(x=10, y=190)
button2 = Button(window, text='View Notes', bg='Turquoise', fg='Red', command=view_notes).place(x=110, y=190)
button3 = Button(window, text='Delete Notes', bg='Turquoise', fg='Red', command=delete_notes).place(x=210, y=190)
button4 = Button(window, text='Update Notes', bg='Turquoise', fg='Red', command=update_notes).place(x=320, y=190)

# Закрытие программы
window.mainloop()
