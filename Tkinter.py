import tkinter as tk
from tkinter import ttk
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Criar tabela de tarefas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL
    )
''')

# Commit e fechar conexão
conn.commit()
conn.close()

def connect_db():
    return sqlite3.connect('tasks.db')

def create_task(title, description, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)', (title, description, status))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY status, id DESC')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(task_id, title, description, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET title = ?, description = ?, status = ?
        WHERE id = ?
    ''', (title, description, status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def update_task_list():
    tasks = get_all_tasks()
    task_list.delete(*task_list.get_children())
    for task in tasks:
        task_list.insert('', 'end', values=task)

def on_add_task():
    title = entry_title.get()
    description = entry_description.get()
    status = combo_status.get()

    if title and status:
        create_task(title, description, status)
        update_task_list()
        entry_title.delete(0, 'end')
        entry_description.delete(0, 'end')

def on_delete_task():
    selected_task = task_list.selection()
    if selected_task:
        task_id = selected_task[0]
        delete_task(task_id)
        update_task_list()

# Criar janela principal
root = tk.Tk()
root.title("Gerenciador de Tarefas")

# Criar widgets
label_title = tk.Label(root, text="Título:")
entry_title = tk.Entry(root)

label_description = tk.Label(root, text="Descrição:")
entry_description = tk.Entry(root)

label_status = tk.Label(root, text="Status:")
status_options = ["Pendente", "Em Progresso", "Concluída"]
combo_status = ttk.Combobox(root, values=status_options)

button_add = tk.Button(root, text="Adicionar Tarefa", command=on_add_task)
button_delete = tk.Button(root, text="Excluir Tarefa", command=on_delete_task)

columns = ('ID', 'Título', 'Descrição', 'Status')
task_list = ttk.Treeview(root, columns=columns, show='headings')

# Configurar cabeçalhos da tabela
for col in columns:
    task_list.heading(col, text=col)
    task_list.column(col, anchor='center')

# Carregar dados
update_task_list()

# Posicionar widgets na grade
label_title.grid(row=0, column=0, sticky='w', padx=5, pady=5)
entry_title.grid(row=0, column=1, padx=5, pady=5)

label_description.grid(row=1, column=0, sticky='w', padx=5, pady=5)
entry_description.grid(row=1, column=1, padx=5, pady=5)

label_status.grid(row=2, column=0, sticky='w', padx=5, pady=5)
combo_status.grid(row=2, column=1, padx=5, pady=5)

button_add.grid(row=3, column=0, columnspan=2, pady=10)
button_delete.grid(row=4, column=0, columnspan=2, pady=10)

task_list.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Iniciar loop principal
root.mainloop()