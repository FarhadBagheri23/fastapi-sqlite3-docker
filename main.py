from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3


class TodoCreate(BaseModel):
    title : str
    description : str | None = None
    is_done : bool


class Todo(TodoCreate):
    id : int


def create_connection():
    connection = sqlite3.connect('todos.db')
    return connection


def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    is_done BOOL NOT NULL)
    """)
    connection.commit()
    connection.close()


def create_todo(todo: TodoCreate):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO todos(title, description, is_done) VALUES (?, ?, ?)", (todo.title, todo.description, todo.is_done))
    connection.commit()
    connection.close()

app = FastAPI()

@app.post('/createTodo/')
def create_todo_endpoint(todo: TodoCreate):
    todo_id = create_todo(todo)
    return {"id":todo_id, **todo.dict()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)