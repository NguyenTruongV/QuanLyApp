import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

# Tạo hoặc kết nối cơ sở dữ liệu SQLite
conn = sqlite3.connect("employee.db")
cursor = conn.cursor()

# Tạo bảng nếu chưa tồn tại
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    department TEXT NOT NULL
)
""")
conn.commit()


def add_employee():
    name = name_entry.get()
    age = age_entry.get()
    department = dept_entry.get()

    if name and age and department:
        cursor.execute("INSERT INTO employees (name, age, department) VALUES (?, ?, ?)", (name, age, department))
        conn.commit()
        messagebox.showinfo("Thành công", "Đã thêm sinh viên!")
        clear_entries()
        load_employees()
    else:
        messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin!")


def delete_employee():
    try:
        selected_item = tree.focus()
        employee_id = tree.item(selected_item)['values'][0]
        cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        conn.commit()
        messagebox.showinfo("Thành công", "Đã xóa sinh viên!")
        load_employees()
    except IndexError:
        messagebox.showwarning("Lỗi", "Vui lòng chọn một sinh viên để xóa!")


def update_employee():
    try:
        selected_item = tree.focus()
        employee_id = tree.item(selected_item)['values'][0]
        name = name_entry.get()
        age = age_entry.get()
        department = dept_entry.get()

        if name and age and department:
            cursor.execute("UPDATE employees SET name = ?, age = ?, department = ? WHERE id = ?",
                           (name, age, department, employee_id))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin sinh viên!")
            clear_entries()
            load_employees()
        else:
            messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin!")
    except IndexError:
        messagebox.showwarning("Lỗi", "Vui lòng chọn một sinh viên để cập nhật!")


def load_employees():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM employees")
    for employee in cursor.fetchall():
        tree.insert("", "end", values=employee)

# Hàm xóa dữ liệu trong ô nhập
def clear_entries():
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    dept_entry.delete(0, END)

# Tạo giao diện bằng Tkinter
root = Tk()
root.title("Quản lý sinh viên")
# root.geometry("600x400")

# Các ô nhập dữ liệu
frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="Tên:").grid(row=0, column=0, padx=5, pady=5)
name_entry = Entry(frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

Label(frame, text="Tuổi:").grid(row=1, column=0, padx=5, pady=5)
age_entry = Entry(frame)
age_entry.grid(row=1, column=1, padx=5, pady=5)

Label(frame, text="Khoa").grid(row=2, column=0, padx=5, pady=5)
dept_entry = Entry(frame)
dept_entry.grid(row=2, column=1, padx=5, pady=5)

# Các nút chức năng
btn_frame = Frame(root)
btn_frame.pack(pady=10)

Button(btn_frame, text="Thêm", command=add_employee).grid(row=0, column=0, padx=10)
Button(btn_frame, text="Xóa", command=delete_employee).grid(row=0, column=1, padx=10)
Button(btn_frame, text="Cập nhật", command=update_employee).grid(row=0, column=2, padx=10)

# Hiển thị danh sách nhân viên
tree = ttk.Treeview(root, columns=("ID", "Tên", "Tuổi", "Khoa"), show="headings", height=10)
tree.pack(pady=20)

tree.heading("ID", text="ID")
tree.heading("Tên", text="Tên")
tree.heading("Tuổi", text="Tuổi")
tree.heading("Khoa", text="Khoa")

tree.column("ID", width=50, anchor=CENTER)
tree.column("Tên", width=150)
tree.column("Tuổi", width=50, anchor=CENTER)
tree.column("Khoa", width=150)

# Tải dữ liệu lên bảng khi khởi chạy
load_employees()

root.mainloop()
