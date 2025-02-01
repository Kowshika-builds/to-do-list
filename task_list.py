import sqlite3

def connect_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """
    )
    conn.commit()
    return conn, cursor

def add_task(name, cursor, conn, task_list):
    cursor.execute("INSERT INTO tasks (name) VALUES (?)", (name,))
    conn.commit()
    task_list.append(name)
    print(f"Task '{name}' added successfully.")

def remove_task(task_id, cursor, conn, task_list):
    cursor.execute("SELECT name FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        task_list.remove(task[0])
        print(f"task with ID {task_id} removed successfully.")
    else:
        print("task not found.")

def list_tasks(cursor, task_list):
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    if tasks:
        print("\ntasks in Database:")
        for task in tasks:
            print(f"ID: {task[0]}, Name: {task[1]}")
    else:
        print("\nNo tasks found.")
    print("\ntasks in List:")
    print(task_list)

def main():
    conn, cursor = connect_db()
    task_list = []
    while True:
        print("\nMenu:")
        print("1. Add task")
        print("2. Remove task")
        print("3. List tasks")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter task name: ")
            add_task(name, cursor, conn, task_list)
        elif choice == "2":
            task_id = input("Enter task ID to remove: ")
            remove_task(task_id, cursor, conn, task_list)
        elif choice == "3":
            list_tasks(cursor, task_list)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
    conn.close()

if __name__ == "__main__":
    main()
