
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from database import SessionLocal, engine
from models import Base, SKU_EXL  # Import the Base class from models
from sqlalchemy.orm import Session
from rich import print as rprint
import traceback
from tkinter import ttk

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
    
    if file_path:
        try:
            df = pd.read_excel(file_path)
            
            insert_data_into_db(df, db)
            result_label.config(text="Data loaded successfully.", fg="green")
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

    # Convert the data to a list of dictionaries
    data_dicts = [item.__dict__ for item in data]

    top = tk.Toplevel(root)
    top.title("Database Data")

    # Create a Treeview widget to display the data in a table
    tree = ttk.Treeview(top)
    tree["columns"] = list(data_dicts[0].keys())

    for column in list(data[0].__dict__.keys()):
        tree.heading(column, text=column)

    # Insert data rows
    for item in data:
        tree.insert("", "end", values=list(item.__dict__.values()))

    tree.pack()


# Create the main window
root = tk.Tk()
root.title("Excel Data Loader")

# Full-screen geometry
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

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

# Button to load data
load_button = tk.Button(padding_frame, text="Load Data", command=load_data, bg="#2196f3", fg="white", font=font_style)
load_button.pack(pady=(0, 20))

# Button to display data
display_button = tk.Button(padding_frame, text="Display Data", command=display_database_data, bg="#ff9800", fg="white", font=font_style)
display_button.pack(pady=(0, 20))

# Result Label
result_label = tk.Label(padding_frame, text="", bg="#f2f2f2", font=font_style)
result_label.pack()

# Run the Tkinter main loop
root.mainloop()