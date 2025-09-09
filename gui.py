import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SOS GAME")
        self.geometry("400x300")
        frame = tk.Frame(self, bg='white')
        frame.pack(fill="both", expand=True)

        # Only create and pack the header label once, at the top
        self.label = tk.Label(frame, text="Welcome to SOS", font=("Helvetica", 25), bg='white', fg='black')
        self.label.pack(pady=10, fill="x")

        self.choice = tk.StringVar(value="S")
        tk.Radiobutton(frame, text="S", variable=self.choice, value="S", bg='white').pack(anchor="w")
        #Add a line separator
        separator = tk.Frame(frame, height=2, bd=1, relief="sunken", bg='black')
        separator.pack(fill="x", padx=5, pady=5)
        tk.Radiobutton(frame, text="O", variable=self.choice, value="O", bg='white').pack(anchor="w")

        self.check_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="Check box", variable=self.check_var, bg='white').pack(anchor="w")

        tk.Button(frame, text="Quit", command=self.destroy, bg='white').pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()