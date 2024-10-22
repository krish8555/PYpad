import tkinter as tk
from tkinter import ttk, filedialog
import os

def text_editor():
    def open_file():
        filepath = filedialog.askopenfilename(
            filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
        )
        if not filepath:
            return
        create_tab(filepath)

    def save_file():
        current_tab = tab_control.select()
        txt_edit = tab_control.nametowidget(current_tab).txt_edit
        filepath = tab_control.tab(current_tab, 'text')

        if os.path.isfile(filepath):  # File already has a path
            with open(filepath, 'w') as output_file:
                text = txt_edit.get(1.0, tk.END)
                output_file.write(text)
        else:  # File doesn't have a path, use "Save As..." behavior
            filepath = filedialog.asksaveasfilename(
                defaultextension='txt',
                filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],
            )
            if not filepath:  # User canceled the save dialog
                return
            with open(filepath, 'w') as output_file:
                text = txt_edit.get(1.0, tk.END)
                output_file.write(text)
            tab_control.tab(current_tab, text=os.path.basename(filepath))  # Update tab name
            tab_control.tab(current_tab, text=filepath)  # Update the internal filepath reference

    def create_tab(filepath=None):
        frame = tk.Frame(tab_control)
        txt_edit = tk.Text(frame, bg="black", fg="green", insertbackground="green")
        txt_edit.pack(expand=1, fill='both')
        txt_edit.bind('<KeyRelease>', lambda e: update_status(txt_edit))
        frame.txt_edit = txt_edit
        tab_name = os.path.basename(filepath) if filepath else "Untitled"
        tab_control.add(frame, text=tab_name)
        tab_control.select(frame)

        if filepath:
            with open(filepath, 'r') as input_file:
                text = input_file.read()
                txt_edit.insert(tk.END, text)

        # Update the status bar for the new tab
        update_status(txt_edit)

    def close_tab():
        current_tab = tab_control.select()
        if current_tab:
            tab_control.forget(current_tab)

    def open_directory():
        directory = filedialog.askdirectory()
        if directory:
            dir_view.delete(0, tk.END)
            for filename in os.listdir(directory):
                full_path = os.path.join(directory, filename)
                if os.path.isfile(full_path):
                    dir_view.insert(tk.END, filename)
            dir_view.current_directory = directory

    def on_file_select(event):
        selection = event.widget.curselection()
        if selection:
            filename = event.widget.get(selection[0])
            directory = dir_view.current_directory
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                create_tab(filepath)

    def update_status(txt_edit):
        content = txt_edit.get(1.0, tk.END).strip()
        lines = content.splitlines()
        line_count = len(lines)
        word_count = sum(len(line.split()) for line in lines)
        status_var.set(f"Lines: {line_count} | Words: {word_count}")

    window = tk.Tk()
    window.title('Text Editor')
    window.geometry('1000x600')
    window.rowconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)

    # Set the icon
    window.iconbitmap('icon.ico')

    # Frame for the directory view and buttons
    fr_directory = tk.Frame(window, relief=tk.RAISED, bd=2, bg="black")
    fr_directory.grid(row=0, column=0, sticky='ns')

    btn_open_dir = tk.Button(fr_directory, text='Open Directory', command=open_directory, bg="black", fg="green")
    btn_open_dir.pack(fill='x', padx=5, pady=5)

    btn_open = tk.Button(fr_directory, text='Open', command=open_file, bg="black", fg="green")
    btn_open.pack(fill='x', padx=5, pady=5)

    btn_save_as = tk.Button(fr_directory, text='Save As...', command=save_file, bg="black", fg="green")
    btn_save_as.pack(fill='x', padx=5, pady=5)

    dir_view = tk.Listbox(fr_directory, bg="black", fg="green", selectbackground="green", selectforeground="black")
    dir_view.pack(fill='both', expand=True, padx=5, pady=5)
    dir_view.bind('<Double-1>', on_file_select)

    tab_control = ttk.Notebook(window)
    tab_control.grid(row=0, column=1, sticky='nsew')

    # Status Bar
    status_var = tk.StringVar()
    status_bar = tk.Label(window, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor='w', bg="black", fg="green")
    status_bar.grid(row=1, column=0, columnspan=2, sticky='ew')

    # Menu
    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label='Open', command=open_file)
    file_menu.add_command(label='Save', command=save_file)
    file_menu.add_command(label='Save As...', command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=window.quit)
    menu_bar.add_cascade(label='File', menu=file_menu)

    # Key bindings for new and close tabs
    window.bind('<Control-t>', lambda e: create_tab())
    window.bind('<Control-w>', lambda e: close_tab())

    window.mainloop()


if __name__ == '__main__':
    text_editor()
