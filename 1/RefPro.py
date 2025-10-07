import psycopg2
from tkinter import *
from tkinter import messagebox

class NoteStorageDB:
    """Класс для работы с заметками в базе данных PostgreSQL."""

    DB_NAME = "notes_db"  
    DB_USER = "your_username"  
    DB_PASSWORD = "your_password"  
    DB_HOST = "localhost"  
    DB_PORT = "5432"  

    def __init__(self):
        """Устанавливаем соединение с базой данных."""
        self.conn = psycopg2.connect(
            dbname=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Создаём таблицу для заметок, если она не существует."""
        create_table_query = """
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                date TEXT NOT NULL,
                title TEXT NOT NULL,
                text TEXT NOT NULL
            )
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def add_note(self, date_, title_, text_):
        """Добавляет заметку в базу данных."""
        insert_query = "INSERT INTO notes (date, title, text) VALUES (%s, %s, %s)"
        self.cursor.execute(insert_query, (date_, title_, text_))
        self.conn.commit()

    def get_notes_by_filters(self, date_=None, title_=None):
        """Возвращает заметки по фильтрам (по дате и/или заголовку)."""
        base_query = "SELECT date, title, text FROM notes WHERE 1=1"
        params = []

        if date_:
            base_query += " AND date = %s"
            params.append(date_)
        
        if title_:
            base_query += " AND title = %s"
            params.append(title_)

        self.cursor.execute(base_query, tuple(params))
        return self.cursor.fetchall()

    def delete_notes(self, date_=None, title_=None):
        """Удаляет заметки, которые соответствуют фильтрам (по дате и/или заголовку)."""
        delete_query = "DELETE FROM notes WHERE 1=1"
        params = []

        if date_:
            delete_query += " AND date = %s"
            params.append(date_)
        
        if title_:
            delete_query += " AND title = %s"
            params.append(title_)

        self.cursor.execute(delete_query, tuple(params))
        deleted_count = self.cursor.rowcount
        self.conn.commit()
        return deleted_count

    def update_note(self, old_date, old_title, new_date, new_title, new_text):
        """Обновляет заметку, соответствующую старым данным (дата и заголовок)."""
        update_query = """
            UPDATE notes
            SET date = %s, title = %s, text = %s
            WHERE date = %s AND title = %s
        """
        self.cursor.execute(update_query, (new_date, new_title, new_text, old_date, old_title))
        updated_count = self.cursor.rowcount
        self.conn.commit()
        return updated_count > 0

    def close(self):
        """Закрытие соединения с базой данных."""
        self.cursor.close()
        self.conn.close()

# Функция для подключения к базе данных
def connect_to_db():
    try:
        return NoteStorageDB()
    except Exception as e:
        messagebox.showerror(message=f"Error: Unable to connect to the database\n{e}")
        return None

# Функции для взаимодействия с базой данных через Tkinter

def add_notes():
    today = date_entry.get()
    notes_title = notes_title_entry.get()
    notes = notes_entry.get("1.0", "end-1c")
    
    if len(today) <= 0 or len(notes_title) <= 0 or len(notes) <= 0:
        messagebox.showerror(message="ENTER REQUIRED DETAILS")
    else:
        storage = connect_to_db()
        if storage:
            storage.add_note(today, notes_title, notes)
            messagebox.showinfo(message="Note added")
            storage.close()

def view_notes():
    date_ = date_entry.get()
    title_ = notes_title_entry.get()

    storage = connect_to_db()
    if storage:
        notes = storage.get_notes_by_filters(date_, title_)
        if notes:
            for note in notes:
                messagebox.showinfo(message=f"Date: {note[0]}\nTitle: {note[1]}\nNotes: {note[2]}")
        else:
            messagebox.showerror(message="No note found")
        storage.close()

def delete_notes():
    date_ = date_entry.get()
    title_ = notes_title_entry.get()

    storage = connect_to_db()
    if storage:
        deleted_count = storage.delete_notes(date_, title_)
        if deleted_count > 0:
            messagebox.showinfo(message="Note(s) Deleted")
        else:
            messagebox.showerror(message="No matching notes to delete")
        storage.close()

def update_notes():
    today = date_entry.get()
    notes_title = notes_title_entry.get()
    notes = notes_entry.get("1.0", "end-1c")

    if len(today) <= 0 or len(notes_title) <= 0 or len(notes) <= 0:
        messagebox.showerror(message="ENTER REQUIRED DETAILS")
    else:
        storage = connect_to_db()
        if storage:
            updated = storage.update_note(today, notes_title, today, notes_title, notes)
            if updated:
                messagebox.showinfo(message="Note Updated")
            else:
                messagebox.showerror(message="No matching note found to update")
            storage.close()

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
