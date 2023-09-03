
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from database import SessionLocal, engine
from models import Base  # Import the Base class from models
from sqlalchemy.orm import Session
from rich import print as rprint
import traceback
import importlib

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

def load_data():
    Base.metadata.create_all(bind=engine)

    file_path = entry_filename.get()
    table_name = entry_tablename.get()
    
    if file_path and table_name:
        try:
            df = pd.read_excel(file_path)
            # duplicate_emails = df[df.duplicated(subset=["Email"], keep=False)]
            # print(duplicate_emails)
            
            insert_data_into_db(df, db, table_name)
            result_label.config(text="Data loaded successfully.", fg="green")
        except Exception as e:
            result_label.config(text=f"Error loading data: {e}", fg="red")
            traceback.print_exc()
    else:
        result_label.config(text="Please select an Excel file and enter a table name.", fg="red")

def insert_data_into_db(df: pd.DataFrame, db: Session, table_name: str) -> None:
    models = importlib.import_module("models")
    table_class = getattr(models, table_name, None)
    print(table_class)
    if table_class is None:
        result_label.config(text=f"Table '{table_name}' not found in models.", fg="red")
        return

    for _, row in df.iterrows():
        if db.query(table_class).filter(table_class.SKU_Code == row.SKU_Code).first():
            rprint(f"[red]Duplicate SKU_Code: {row.SKU_Code}[/red]")
            continue
        data = table_class(
            SKU_Code=row.SKU_Code,
            LOT_No=row.LOT_No,
            Serial_No=row.Serial_No,
        )

        db.add(data)
        db.commit()

# Create the main window
root = tk.Tk()
root.title("Excel Data Loader")

# Styling
root.geometry("500x300")
root.configure(bg="#f2f2f2")

# Label and Entry for the file name
label_filename = tk.Label(root, text="Select an Excel file:", bg="#f2f2f2")
label_filename.pack()
entry_filename = tk.Entry(root, width=40)
entry_filename.pack()
browse_button = tk.Button(root, text="Browse", command=browse_file, bg="#4caf50", fg="white")
browse_button.pack()

# Label and Entry for the table name
label_tablename = tk.Label(root, text="Table Name:", bg="#f2f2f2")
label_tablename.pack()
entry_tablename = tk.Entry(root, width=40)
entry_tablename.pack()

# Button to load data
load_button = tk.Button(root, text="Load Data", command=load_data, bg="#2196f3", fg="white")
load_button.pack()

# Result Label
result_label = tk.Label(root, text="", bg="#f2f2f2")
result_label.pack()



# Run the Tkinter main loop
root.mainloop()
