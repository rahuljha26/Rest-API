import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests

# Set your API base URL
API_URL = "http://127.0.0.1:5000/users"

# ---------- Functions ----------

def add_user():
    name = name_entry.get()
    email = email_entry.get()
    if not name or not email:
        messagebox.showwarning("Input Error", "Please enter both name and email.")
        return
    try:
        response = requests.post(API_URL, json={"name": name, "email": email})
        if response.status_code == 201:
            messagebox.showinfo("Success", "User added successfully.")
            view_users()
        else:
            try:
                error = response.json().get("error", "Something went wrong")
            except Exception:
                error = f"Something went wrong: {response.text}"
            messagebox.showerror("Error", error)
    except Exception as e:
        messagebox.showerror("Error", f"Could not connect to API: {e}")

def view_users():
    try:
        response = requests.get(API_URL)
        output_box.delete(1.0, tk.END)
        if response.status_code == 200:
            try:
                users = response.json()
                # Users can be a dict or a list; handle both
                if isinstance(users, dict):
                    for uid, user in users.items():
                        output_box.insert(tk.END, f"ID: {uid} | Name: {user['name']} | Email: {user['email']}\n")
                elif isinstance(users, list):
                    for user in users:
                        output_box.insert(tk.END, f"ID: {user.get('id', '')} | Name: {user.get('name', '')} | Email: {user.get('email', '')}\n")
                else:
                    output_box.insert(tk.END, "No users found.\n")
            except Exception as e:
                output_box.insert(tk.END, f"Error parsing user data: {e}\n")
        else:
            messagebox.showerror("Error", f"Could not retrieve users. Status: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not connect to API: {e}")

def update_user():
    uid = id_entry.get()
    name = name_entry.get()
    email = email_entry.get()
    if not uid:
        messagebox.showwarning("Input Error", "User ID required for update.")
        return

    data = {}
    if name: data["name"] = name
    if email: data["email"] = email

    try:
        response = requests.put(f"{API_URL}/{uid}", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Updated", "User updated successfully.")
            view_users()
        else:
            try:
                error = response.json().get("error", "Update failed")
            except Exception:
                error = f"Update failed: {response.text}"
            messagebox.showerror("Error", error)
    except Exception as e:
        messagebox.showerror("Error", f"Could not connect to API: {e}")

def delete_user():
    uid = id_entry.get()
    if not uid:
        messagebox.showwarning("Input Error", "User ID required to delete.")
        return

    try:
        response = requests.delete(f"{API_URL}/{uid}")
        if response.status_code == 200:
            messagebox.showinfo("Deleted", f"User {uid} deleted.")
            view_users()
        else:
            try:
                error = response.json().get("error", "Delete failed")
            except Exception:
                error = f"Delete failed: {response.text}"
            messagebox.showerror("Error", error)
    except Exception as e:
        messagebox.showerror("Error", f"Could not connect to API: {e}")

# ---------- UI Setup ----------

root = tk.Tk()
root.title("User Manager API Client")
root.geometry("500x550")

tk.Label(root, text="User ID:").pack()
id_entry = tk.Entry(root)
id_entry.pack()

tk.Label(root, text="Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Email:").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Button(root, text="Add User", command=add_user).pack(pady=5)
tk.Button(root, text="Update User", command=update_user).pack(pady=5)
tk.Button(root, text="Delete User", command=delete_user).pack(pady=5)
tk.Button(root, text="View All Users", command=view_users).pack(pady=5)

output_box = scrolledtext.ScrolledText(root, width=60, height=15)
output_box.pack(pady=10)

root.mainloop()