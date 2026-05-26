import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Universitydbproject"
    )

    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected successfully to MySQL Server version", db_info)

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database:", record)
        cursor.close()
except Error as e:
    print("Error while connecting to MySQL:", e)
finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
class UniversityDatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("University Database System")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f0f0f0")

        self.connection = None
        self.current_table = None
        self.connect_to_database()

        # Create interface
        self.create_widgets()

    def connect_to_database(self):
        """Connect to database"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="universitydbproject"
            )
            if self.connection.is_connected():
                print(f"Connected to MySQL Server version: {self.connection.server_info}")
        except Error as e:
            messagebox.showerror("Connection Error", f"Error connecting to database:\n{e}")

    def create_widgets(self):
        """Create interface elements"""
        # Main title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="🎓 University Database Management System",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)

        # Button frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0", pady=15)
        button_frame.pack()

        buttons_info = [
            ("📋 View Tables", self.view_all_data, "#3498db"),
            ("➕ Add Data", self.add_data, "#27ae60"),
            ("🔍 Search", self.search_data, "#f39c12"),
            ("✏️ Update", self.update_data, "#e67e22"),
            ("🗑️ Delete", self.delete_data, "#e74c3c"),
        ]

        for text, command, color in buttons_info:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 10, "bold"),
                bg=color,
                fg="white",
                width=14,
                height=2,
                relief=tk.RAISED,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=8)

        # Table frame
        table_frame = tk.Frame(self.root, bg="#f0f0f0")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        # Treeview for display
        self.tree = ttk.Treeview(
            table_frame,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode='browse',
            height=15
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Style Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        # Status Bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#ecf0f1",
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def view_all_data(self):
        """View all data from a specific table"""
        if not self.connection or not self.connection.is_connected():
            messagebox.showerror("Error", "Not connected to database")
            return

        # Window to select table
        table_window = tk.Toplevel(self.root)
        table_window.title("Select Table")
        table_window.geometry("350x250")
        table_window.configure(bg="#ecf0f1")

        tk.Label(
            table_window,
            text="Select table to view contents:",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1"
        ).pack(pady=20)

        # Get table names
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()

        table_var = tk.StringVar()
        table_combo = ttk.Combobox(
            table_window,
            textvariable=table_var,
            values=tables,
            width=30,
            font=("Arial", 11),
            state="readonly"
        )
        table_combo.pack(pady=10)
        if tables:
            table_combo.current(0)

        def show_table():
            table_name = table_var.get()
            if table_name:
                self.current_table = table_name
                self.display_table_data(table_name)
                table_window.destroy()

        tk.Button(
            table_window,
            text="✓ View",
            command=show_table,
            bg="#27ae60",
            fg="white",
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(pady=20)

    def display_table_data(self, table_name):
        """Display table data"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()

            # Clear old data
            self.tree.delete(*self.tree.get_children())

            # Setup columns
            self.tree['columns'] = columns
            self.tree['show'] = 'headings'

            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor=tk.CENTER)

            # Add data
            for row in rows:
                self.tree.insert('', tk.END, values=row)

            self.status_bar.config(text=f"Displaying {len(rows)} records from {table_name}")

        except Error as e:
            messagebox.showerror("Error", f"Error fetching data:\n{e}")

    def add_data(self):
        """Add new data"""
        if not self.connection or not self.connection.is_connected():
            messagebox.showerror("Error", "Not connected to database")
            return

        # Window to select table
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Data")
        add_window.geometry("400x250")
        add_window.configure(bg="#ecf0f1")

        tk.Label(
            add_window,
            text="Select table to add new data:",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1"
        ).pack(pady=20)

        # Get table names
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()

        table_var = tk.StringVar()
        table_combo = ttk.Combobox(
            add_window,
            textvariable=table_var,
            values=tables,
            width=30,
            font=("Arial", 11),
            state="readonly"
        )
        table_combo.pack(pady=10)
        if tables:
            table_combo.current(0)

        def open_add_form():
            table_name = table_var.get()
            if table_name:
                add_window.destroy()
                self.show_add_form(table_name)

        tk.Button(
            add_window,
            text="✓ Continue",
            command=open_add_form,
            bg="#27ae60",
            fg="white",
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(pady=20)

    def show_add_form(self, table_name):
        """Show add data form"""
        try:
            # Get table columns
            cursor = self.connection.cursor()
            cursor.execute(f"DESCRIBE {table_name}")
            columns_info = cursor.fetchall()
            cursor.close()

            # Form window
            form_window = tk.Toplevel(self.root)
            form_window.title(f"Add New Data - {table_name}")
            form_window.geometry("500x600")
            form_window.configure(bg="#ecf0f1")

            # Form title
            tk.Label(
                form_window,
                text=f"Add new record to {table_name}",
                font=("Arial", 14, "bold"),
                bg="#2c3e50",
                fg="white",
                pady=15
            ).pack(fill=tk.X)

            # Fields frame
            canvas = tk.Canvas(form_window, bg="#ecf0f1")
            scrollbar = ttk.Scrollbar(form_window, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            entries = {}

            for col_info in columns_info:
                col_name = col_info[0]
                col_type = col_info[1]
                is_nullable = col_info[2]
                key_type = col_info[3]

                # Skip auto increment columns
                if 'auto_increment' in str(col_info).lower():
                    continue

                frame = tk.Frame(scrollable_frame, bg="#ecf0f1", pady=8)
                frame.pack(fill=tk.X, padx=20)

                label_text = f"{col_name}:"
                if key_type == "PRI":
                    label_text += " (Primary Key)"
                if is_nullable == "NO":
                    label_text += " *"

                tk.Label(
                    frame,
                    text=label_text,
                    font=("Arial", 10),
                    bg="#ecf0f1",
                    anchor="w",
                    width=20
                ).pack(side=tk.LEFT)

                entry = tk.Entry(frame, font=("Arial", 10), width=30)
                entry.pack(side=tk.LEFT, padx=10)
                entries[col_name] = entry

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

            # Save and Cancel buttons
            button_frame = tk.Frame(form_window, bg="#ecf0f1", pady=15)
            button_frame.pack(fill=tk.X)

            def save_data():
                try:
                    values = {}
                    for col_name, entry in entries.items():
                        value = entry.get().strip()
                        values[col_name] = value if value else None

                    columns = ", ".join(values.keys())
                    placeholders = ", ".join(["%s"] * len(values))
                    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

                    cursor = self.connection.cursor()
                    cursor.execute(query, list(values.values()))
                    self.connection.commit()
                    cursor.close()

                    messagebox.showinfo("Success", "Data added successfully! ✓")
                    form_window.destroy()

                    # Update display if table is shown
                    if self.current_table == table_name:
                        self.display_table_data(table_name)

                except Error as e:
                    messagebox.showerror("Error", f"Error adding data:\n{e}")

            tk.Button(
                button_frame,
                text="💾 Save",
                command=save_data,
                bg="#27ae60",
                fg="white",
                width=15,
                height=2,
                font=("Arial", 11, "bold"),
                cursor="hand2"
            ).pack(side=tk.LEFT, padx=20)

            tk.Button(
                button_frame,
                text="✖ Cancel",
                command=form_window.destroy,
                bg="#e74c3c",
                fg="white",
                width=15,
                height=2,
                font=("Arial", 11, "bold"),
                cursor="hand2"
            ).pack(side=tk.LEFT, padx=20)

        except Error as e:
            messagebox.showerror("Error", f"Error displaying form:\n{e}")

    def search_data(self):
        """Search data"""
        if not self.connection or not self.connection.is_connected():
            messagebox.showerror("Error", "Not connected to database")
            return

        if not self.current_table:
            messagebox.showwarning("Warning", "Please select a table first from 'View Tables'")
            return

        # Search window
        search_window = tk.Toplevel(self.root)
        search_window.title(f"Search in {self.current_table}")
        search_window.geometry("500x300")
        search_window.configure(bg="#ecf0f1")

        tk.Label(
            search_window,
            text=f"Search in {self.current_table}",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=15
        ).pack(fill=tk.X)

        # Get table columns
        cursor = self.connection.cursor()
        cursor.execute(f"DESCRIBE {self.current_table}")
        columns = [col[0] for col in cursor.fetchall()]
        cursor.close()

        # Select column
        frame1 = tk.Frame(search_window, bg="#ecf0f1", pady=15)
        frame1.pack(fill=tk.X, padx=30)

        tk.Label(frame1, text="Column:", font=("Arial", 11), bg="#ecf0f1", width=15, anchor="w").pack(side=tk.LEFT)

        column_var = tk.StringVar()
        column_combo = ttk.Combobox(
            frame1,
            textvariable=column_var,
            values=columns,
            width=25,
            font=("Arial", 10),
            state="readonly"
        )
        column_combo.pack(side=tk.LEFT, padx=10)
        if columns:
            column_combo.current(0)

        # Search value
        frame2 = tk.Frame(search_window, bg="#ecf0f1", pady=10)
        frame2.pack(fill=tk.X, padx=30)

        tk.Label(frame2, text="Value:", font=("Arial", 11), bg="#ecf0f1", width=15, anchor="w").pack(side=tk.LEFT)

        search_entry = tk.Entry(frame2, font=("Arial", 10), width=27)
        search_entry.pack(side=tk.LEFT, padx=10)

        def perform_search():
            column = column_var.get()
            value = search_entry.get().strip()

            if not column or not value:
                messagebox.showwarning("Warning", "Please select column and enter search value")
                return

            try:
                cursor = self.connection.cursor()
                query = f"SELECT * FROM {self.current_table} WHERE {column} LIKE %s"
                cursor.execute(query, (f"%{value}%",))
                rows = cursor.fetchall()
                columns_info = [desc[0] for desc in cursor.description]
                cursor.close()

                # Clear old data
                self.tree.delete(*self.tree.get_children())

                # Setup columns
                self.tree['columns'] = columns_info
                self.tree['show'] = 'headings'

                for col in columns_info:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=120, anchor=tk.CENTER)

                # Add search results
                for row in rows:
                    self.tree.insert('', tk.END, values=row)

                self.status_bar.config(text=f"Search results: {len(rows)} records")
                search_window.destroy()

                if len(rows) == 0:
                    messagebox.showinfo("Search Results", "No matching results found")

            except Error as e:
                messagebox.showerror("Error", f"Search error:\n{e}")

        # Buttons
        button_frame = tk.Frame(search_window, bg="#ecf0f1", pady=20)
        button_frame.pack()

        tk.Button(
            button_frame,
            text="🔍 Search",
            command=perform_search,
            bg="#f39c12",
            fg="white",
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="✖ Cancel",
            command=search_window.destroy,
            bg="#95a5a6",
            fg="white",
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)

    def update_data(self):
        """Update data"""
        if not self.connection or not self.connection.is_connected():
            messagebox.showerror("Error", "Not connected to database")
            return

        if not self.current_table:
            messagebox.showwarning("Warning", "Please select a table first from 'View Tables'")
            return

        # Get selected row
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to update")
            return

        values = self.tree.item(selected_item[0])['values']
        columns = self.tree['columns']

        # Get columns info
        cursor = self.connection.cursor()
        cursor.execute(f"DESCRIBE {self.current_table}")
        columns_info = cursor.fetchall()
        cursor.close()

        # Update window
        update_window = tk.Toplevel(self.root)
        update_window.title(f"Update Record - {self.current_table}")
        update_window.geometry("500x600")
        update_window.configure(bg="#ecf0f1")

        tk.Label(
            update_window,
            text=f"Update record in {self.current_table}",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=15
        ).pack(fill=tk.X)

        # Fields frame
        canvas = tk.Canvas(update_window, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(update_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        entries = {}
        primary_key = None
        primary_key_value = None

        for i, col_info in enumerate(columns_info):
            col_name = col_info[0]
            key_type = col_info[3]

            # Save primary key
            if key_type == "PRI":
                primary_key = col_name
                primary_key_value = values[i]

            frame = tk.Frame(scrollable_frame, bg="#ecf0f1", pady=8)
            frame.pack(fill=tk.X, padx=20)

            label_text = f"{col_name}:"
            if key_type == "PRI":
                label_text += " (Primary Key)"

            tk.Label(
                frame,
                text=label_text,
                font=("Arial", 10),
                bg="#ecf0f1",
                anchor="w",
                width=20
            ).pack(side=tk.LEFT)

            entry = tk.Entry(frame, font=("Arial", 10), width=30)
            entry.insert(0, str(values[i]) if i < len(values) else "")

            # Disable primary key
            if key_type == "PRI":
                entry.config(state="readonly")

            entry.pack(side=tk.LEFT, padx=10)
            entries[col_name] = entry

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        # Buttons
        button_frame = tk.Frame(update_window, bg="#ecf0f1", pady=15)
        button_frame.pack(fill=tk.X)

        def save_update():
            if not primary_key:
                messagebox.showerror("Error", "Primary key not found for table")
                return

            try:
                updates = []
                values_list = []

                for col_name, entry in entries.items():
                    if col_name != primary_key:
                        value = entry.get().strip()
                        updates.append(f"{col_name} = %s")
                        values_list.append(value if value else None)

                values_list.append(primary_key_value)

                query = f"UPDATE {self.current_table} SET {', '.join(updates)} WHERE {primary_key} = %s"

                cursor = self.connection.cursor()
                cursor.execute(query, values_list)
                self.connection.commit()
                cursor.close()

                messagebox.showinfo("Success", "Data updated successfully! ✓")
                update_window.destroy()

                # Update display
                self.display_table_data(self.current_table)

            except Error as e:
                messagebox.showerror("Error", f"Error updating data:\n{e}")

        tk.Button(
            button_frame,
            text="💾 Save Update",
            command=save_update,
            bg="#e67e22",
            fg="white",
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=20)

        tk.Button(
            button_frame,
            text="✖ Cancel",
            command=update_window.destroy,
            bg="#95a5a6",
            fg="white",
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=20)

    def delete_data(self):
        """Delete data"""
        if not self.connection or not self.connection.is_connected():
            messagebox.showerror("Error", "Not connected to database")
            return

        if not self.current_table:
            messagebox.showwarning("Warning", "Please select a table first from 'View Tables'")
            return

        # Get selected row
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return

        values = self.tree.item(selected_item[0])['values']
        columns = self.tree['columns']

        # Get primary key
        cursor = self.connection.cursor()
        cursor.execute(f"DESCRIBE {self.current_table}")
        columns_info = cursor.fetchall()
        cursor.close()

        primary_key = None
        primary_key_value = None

        for i, col_info in enumerate(columns_info):
            if col_info[3] == "PRI":
                primary_key = col_info[0]
                primary_key_value = values[i]
                break

        if not primary_key:
            messagebox.showerror("Error", "Primary key not found for table")
            return

        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this record?\n\n{primary_key} = {primary_key_value}\n\nThis action cannot be undone!"
        )

        if not confirm:
            return

        try:
            query = f"DELETE FROM {self.current_table} WHERE {primary_key} = %s"
            cursor = self.connection.cursor()
            cursor.execute(query, (primary_key_value,))
            self.connection.commit()
            cursor.close()

            messagebox.showinfo("Success", "Record deleted successfully! ✓")

            # Update display
            self.display_table_data(self.current_table)

        except Error as e:
            messagebox.showerror("Error", f"Error deleting data:\n{e}")

    def __del__(self):
        """Close connection when program ends"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")
if __name__ == "__main__":
    root = tk.Tk()
    app = UniversityDatabaseGUI(root)
    root.mainloop()