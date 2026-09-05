import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar   
     
# ---------------- Window Setup ----------------   
root = tk.Tk()
root.title("📚 Library Management System")
root.geometry("950x700")
root.configure(bg="#e3f2fd")

books = []
issued_books = []

# ---------------- Shared Styles ----------------
title_font = ("Helvetica", 26, "bold")
label_font = ("Arial", 12)
button_style = {"font": ("Arial", 12, "bold"), "fg": "white", "width": 18, "cursor": "hand2", "bd": 0, "relief": "flat"}

def show_frame(frame):
    frame.tkraise()

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

home = tk.Frame(root, bg="#e3f2fd")
add_book_page = tk.Frame(root, bg="#c8e6c9")
issue_book_page = tk.Frame(root, bg="#fff9c4")

for frame in (home, add_book_page, issue_book_page):
    frame.grid(row=0, column=0, sticky="nsew")

# ---------------- Calendar Function ----------------
def open_calendar(entry):
    win = tk.Toplevel(root)
    win.title("Select Date")
    win.geometry("300x300")
    cal = Calendar(win, selectmode='day', date_pattern='dd-mm-yyyy')
    cal.pack(pady=20)
    def pick():
        entry.delete(0, tk.END)
        entry.insert(0, cal.get_date())
        win.destroy()
    tk.Button(win, text="Select", command=pick, bg="#4caf50", fg="white", font=("Arial", 11, "bold")).pack(pady=10)

# ---------------- HOME PAGE (Enhanced Design) ----------------
# Background gradient effect with Canvas
canvas = tk.Canvas(home, width=950, height=700, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Gradient background manually drawn
for i in range(0, 700):
    r = 179 + i // 10
    g = 229
    b = 252
    color = f"#{r:02x}{g:02x}{b:02x}"
    canvas.create_line(0, i, 950, i, fill=color)

# Decorative Title Box
canvas.create_rectangle(120, 80, 830, 200, fill="#1976d2", outline="")
canvas.create_text(475, 140, text="📘 LIBRARY MANAGEMENT SYSTEM", fill="white", font=("Helvetica", 26, "bold"))

# Subtitle glow effect
canvas.create_text(475, 190, text="Manage • Organize • Issue with Ease", fill="#e3f2fd", font=("Arial", 14, "italic"))

# Buttons container
button_frame = tk.Frame(home, bg="#e3f2fd")
button_frame.place(relx=0.5, rely=0.65, anchor="center")

def make_button(text, bg, hover, cmd):
    btn = tk.Button(button_frame, text=text, bg=bg, activebackground=hover, **button_style, command=cmd)
    btn.pack(pady=15, ipadx=10, ipady=5, fill="x")
    # Hover effect
    def on_enter(e): btn.config(bg=hover)
    def on_leave(e): btn.config(bg=bg)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

make_button("➕ Add / Manage Books", "#42a5f5", "#64b5f6", lambda: show_frame(add_book_page))
make_button("📖 Issue Book", "#66bb6a", "#81c784", lambda: show_frame(issue_book_page))
make_button("❌ Exit", "#ef5350", "#e57373", root.destroy)

# Footer text
canvas.create_text(475, 670, text="Developed by Kumari Muskan 💫", fill="#0d47a1", font=("Arial", 10, "italic"))

# ---------------- ADD / MANAGE BOOKS PAGE ----------------
tk.Label(add_book_page, text="📚 Book Management", bg="#c8e6c9", fg="#1b5e20", font=title_font).pack(pady=20)

form = tk.Frame(add_book_page, bg="#c8e6c9")
form.pack()

tk.Label(form, text="Book ID:", bg="#c8e6c9", font=label_font).grid(row=0, column=0, padx=10, pady=10)
book_id = tk.Entry(form, bg="white")
book_id.grid(row=0, column=1, padx=10, pady=10)

tk.Label(form, text="Title:", bg="#c8e6c9", font=label_font).grid(row=1, column=0, padx=10, pady=10)
book_title = tk.Entry(form, bg="white")
book_title.grid(row=1, column=1, padx=10, pady=10)

tk.Label(form, text="Author:", bg="#c8e6c9", font=label_font).grid(row=2, column=0, padx=10, pady=10)
book_author = tk.Entry(form, bg="white")
book_author.grid(row=2, column=1, padx=10, pady=10)

def add_book():
    bid, title, author = book_id.get(), book_title.get(), book_author.get()
    if not (bid and title and author):
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return
    for b in books:
        if b["id"] == bid:
            messagebox.showerror("Duplicate", "Book ID already exists!")
            return
    books.append({"id": bid, "title": title, "author": author})
    messagebox.showinfo("Success", f"Book '{title}' added successfully!")
    show_books()
    book_id.delete(0, tk.END)
    book_title.delete(0, tk.END)
    book_author.delete(0, tk.END)

def delete_book():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Please select a book to delete.")
        return
    item = tree.item(selected)
    bid = item["values"][0]
    for b in books:
        if b["id"] == bid:
            books.remove(b)
            break
    show_books()
    messagebox.showinfo("Deleted", "Book deleted successfully!")

def show_books():
    for i in tree.get_children():
        tree.delete(i)
    for b in books:
        tree.insert("", "end", values=(b["id"], b["title"], b["author"]))

tk.Button(form, text="Add", bg="#43a047", activebackground="#66bb6a", **button_style, command=add_book).grid(row=3, column=0, pady=10)
tk.Button(form, text="Delete", bg="#e53935", activebackground="#ef5350", **button_style, command=delete_book).grid(row=3, column=1, pady=10)
tk.Button(form, text="← Back", bg="#78909c", activebackground="#90a4ae", **button_style, command=lambda: show_frame(home)).grid(row=3, column=2, pady=10)

tree = ttk.Treeview(add_book_page, columns=("ID", "Title", "Author"), show="headings", height=10)
tree.heading("ID", text="Book ID")
tree.heading("Title", text="Book Title")
tree.heading("Author", text="Author")
tree.pack(fill="x", padx=40, pady=20)

# ---------------- ISSUE BOOK PAGE ----------------
tk.Label(issue_book_page, text="📖 Issue Book", bg="#fff9c4", fg="#f57f17", font=title_font).pack(pady=20)
issue_frame = tk.Frame(issue_book_page, bg="#fff9c4")
issue_frame.pack()

tk.Label(issue_frame, text="Student Name:", bg="#fff9c4", font=label_font).grid(row=0, column=0, padx=10, pady=10)
student_name = tk.Entry(issue_frame, bg="white")
student_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(issue_frame, text="Book ID:", bg="#fff9c4", font=label_font).grid(row=1, column=0, padx=10, pady=10)
book_id_entry = tk.Entry(issue_frame, bg="white")
book_id_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(issue_frame, text="Issue Date:", bg="#fff9c4", font=label_font).grid(row=2, column=0, padx=10, pady=10)
issue_date = tk.Entry(issue_frame, bg="white")
issue_date.grid(row=2, column=1, padx=10, pady=10)
tk.Button(issue_frame, text="📅", command=lambda: open_calendar(issue_date)).grid(row=2, column=2)

tk.Label(issue_frame, text="Return Date:", bg="#fff9c4", font=label_font).grid(row=3, column=0, padx=10, pady=10)
return_date = tk.Entry(issue_frame, bg="white")
return_date.grid(row=3, column=1, padx=10, pady=10)
tk.Button(issue_frame, text="📅", command=lambda: open_calendar(return_date)).grid(row=3, column=2)

def issue_book():
    name, bid, idate, rdate = student_name.get(), book_id_entry.get(), issue_date.get(), return_date.get()
    if not (name and bid and idate and rdate):
        messagebox.showwarning("Input Error", "Please fill all details!")
        return
    for b in books:
        if b["id"] == bid:
            issued_books.append({"student": name, "book_id": bid, "title": b["title"], "issue_date": idate, "return_date": rdate})
            messagebox.showinfo("Issued", f"Book '{b['title']}' issued to {name}")
            show_issued_books()
            return
    messagebox.showerror("Not Found", "Book ID not found!")

def show_issued_books():
    for i in issue_tree.get_children():
        issue_tree.delete(i)
    for item in issued_books:
        issue_tree.insert("", "end", values=(item["student"], item["book_id"], item["title"], item["issue_date"], item["return_date"]))

tk.Button(issue_frame, text="Issue", bg="#fbc02d", activebackground="#fdd835", **button_style, command=issue_book).grid(row=4, column=1, pady=15)
tk.Button(issue_frame, text="← Back", bg="#78909c", activebackground="#90a4ae", **button_style, command=lambda: show_frame(home)).grid(row=4, column=2, pady=15)

issue_tree = ttk.Treeview(issue_book_page, columns=("Student", "BookID", "Title", "Issue", "Return"), show="headings", height=9)
for col in ("Student", "BookID", "Title", "Issue", "Return"):
    issue_tree.heading(col, text=col)
issue_tree.pack(fill="x", padx=40, pady=20)

# ---------------- Start ----------------
show_frame(home)
root.mainloop()
