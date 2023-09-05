import tkinter as tk
from tkinter import filedialog
import pandas as pd
from database import SessionLocal, engine
from models import Base, SKU_EXL
from sqlalchemy.orm import Session
from rich import print as rprint
import traceback
from tkinter import ttk
from pydantic import BaseModel
from typing import List

class SKUEXL(BaseModel):
    SKU_Code: str
    LOT_No: str
    Serial_No: str

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database initialization
db = next(get_db())

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        entry_filename.delete(0, tk.END)
        entry_filename.insert(0, file_path)

def load_data_and_display():
    Base.metadata.create_all(bind=engine)

    file_path = entry_filename.get()

    if file_path:
        try:
            df = pd.read_excel(file_path)

            insert_data_into_db(df, db)
            result_label.config(text="Data loaded successfully.", fg="green")

            # Display data in the Treeview widget
            display_database_data()
        except Exception as e:
            result_label.config(text=f"Error loading data: {str(e)}", fg="red")
            traceback.print_exc()
    else:
        result_label.config(text="Please select an Excel file and enter a table name.", fg="red")

def insert_data_into_db(df: pd.DataFrame, db: Session) -> None:
    for _, row in df.iterrows():
        if db.query(SKU_EXL).filter(SKU_EXL.SKU_Code == row.SKU_Code).first():
            rprint(f"[red]Duplicate SKU_Code: {row.SKU_Code}[/red]")
            continue
        data = SKU_EXL(
            SKU_Code=row.SKU_Code,
            LOT_No=row.LOT_No,
            Serial_No=row.Serial_No,
        )

        db.add(data)
        db.commit()

def display_database_data():
    data = db.query(SKU_EXL).all()

    # Clear the Treeview widget
    for item in tree.get_children():
        tree.delete(item)

    # Insert data rows
    for item in data:
        res = SKUEXL(SKU_Code=item.SKU_Code, LOT_No=item.LOT_No, Serial_No=item.Serial_No)
        tree.insert("", "end", values=(res.SKU_Code, res.LOT_No, res.Serial_No))

    # Calculate the number of rows and adjust the table size
    num_rows = len(data)
    tree['height'] = min(num_rows, 20)  # Show at most 20 rows, adjust as needed

# Filtering function
def filter_data(event):
    filter_text = entry_filter.get().strip().lower()
    filtered_data = []
    for item in db.query(SKU_EXL).all():
        if (filter_text in item.SKU_Code.lower() or
            filter_text in item.LOT_No.lower() or
            filter_text in item.Serial_No.lower()):
            filtered_data.append(item)

    # Clear the Treeview widget
    for item in tree.get_children():
        tree.delete(item)

    # Insert filtered data rows
    for item in filtered_data:
        res = SKUEXL(SKU_Code=item.SKU_Code, LOT_No=item.LOT_No, Serial_No=item.Serial_No)
        tree.insert("", "end", values=(res.SKU_Code, res.LOT_No, res.Serial_No))

    # Calculate the number of rows and adjust the table size
    num_rows = len(filtered_data)
    tree['height'] = min(num_rows, 20)  # Show at most 20 rows, adjust as needed


# Create the main window
root = tk.Tk()
root.title("Excel Data Loader")
root.state("zoomed")

# Styling
root.configure(bg="#f2f2f2")

# Add padding and spacing
padding_frame = tk.Frame(root, bg="#f2f2f2")
padding_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Larger font size
font_style = ("Helvetica", 14)

# Label and Entry for the file name
label_filename = tk.Label(padding_frame, text="Select an Excel file:", bg="#f2f2f2", font=font_style)
label_filename.pack(pady=(0, 10))
entry_filename = tk.Entry(padding_frame, width=40, font=font_style)
entry_filename.pack(pady=(0, 10))
browse_button = tk.Button(padding_frame, text="Browse", command=browse_file, bg="#4caf50", fg="white", font=font_style)
browse_button.pack(pady=(0, 10))

# Button to load data and display
load_button = tk.Button(padding_frame, text="Load Data", command=load_data_and_display, bg="#2196f3", fg="white", font=font_style)
load_button.pack(pady=(0, 20))

# Filter Entry
entry_filter = tk.Entry(padding_frame, width=40, font=font_style)
entry_filter.pack(pady=(0, 10))
entry_filter.bind("<KeyRelease>", filter_data)
# filter_button = tk.Button(padding_frame, text="Search", command=filter_data, bg="#2196f3", fg="white", font=font_style)
# filter_button.pack(pady=(0, 20))

# Result Label
result_label = tk.Label(padding_frame, text="", bg="#f2f2f2", font=font_style)
result_label.pack()

style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 14))  # Set heading font size
style.configure("Treeview", font=(None, 12), rowheight=25)
style.configure("Treeview.Cell", borderwidth=1, relief="solid")
# Create a Treeview widget to display the data in a table
tree = ttk.Treeview(padding_frame, show="headings", style="Treeview")
tree["columns"] = ("SKU_Code", "LOT_No", "Serial_No")

for column in ("SKU_Code", "LOT_No", "Serial_No"):
    tree.heading(column, text=column)

tree.pack(fill="both")

# Run the Tkinter main loop
root.mainloop()
