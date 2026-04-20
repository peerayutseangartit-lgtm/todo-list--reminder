import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
from datetime import datetime

class SimpleTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("โปรแกรมแจ้งเตือนกันลืม")
        self.root.geometry("450x450")
        
        # รายการเก็บข้อมูลงาน [(เวลา, งาน, สถานะ)]
        self.tasks = []

        # --- ส่วนกรอกข้อมูล ---
        frame_input = tk.Frame(self.root, pady=10)
        frame_input.pack()

        tk.Label(frame_input, text="สิ่งที่ต้องทำ:").grid(row=0, column=0, sticky="w")
        self.task_entry = tk.Entry(frame_input, width=30)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="เวลา (เช่น 14:30):").grid(row=1, column=0, sticky="w")
        self.time_entry = tk.Entry(frame_input, width=15)
        self.time_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.time_entry.insert(0, datetime.now().strftime("%H:%M"))

        self.add_btn = tk.Button(frame_input, text="เพิ่มรายการ", command=self.add_task, bg="green", fg="white")
        self.add_btn.grid(row=2, column=1, sticky="e", pady=10)

        # --- ส่วนแสดงผล ---
        self.tree = ttk.Treeview(self.root, columns=("Time", "Task"), show="headings", height=10)
        self.tree.heading("Time", text="เวลา")
        self.tree.heading("Task", text="สิ่งที่ต้องทำ")
        self.tree.column("Time", width=80)
        self.tree.column("Task", width=300)
        self.tree.pack(pady=10, padx=10)

        # เริ่มระบบตรวจสอบเวลา (Background Thread)
        self.check_thread = threading.Thread(target=self.check_timer, daemon=True)
        self.check_thread.start()

    def add_task(self):
        task = self.task_entry.get()
        time_str = self.time_entry.get()

        if not task or not time_str:
            messagebox.showwarning("เตือน", "กรุณากรอกข้อมูลให้ครบ")
            return

        try:
            # เช็คว่ารูปแบบเวลาถูกต้องไหม
            datetime.strptime(time_str, "%H:%M")
            
            # เพิ่มข้อมูลลงในรายการและตาราง
            self.tasks.append({"time": time_str, "task": task, "done": False})
            self.tree.insert("", tk.END, values=(time_str, task))
            
            self.task_entry.delete(0, tk.END)
            messagebox.showinfo("สำเร็จ", f"เพิ่มรายการ '{task}' ตอน {time_str} แล้ว")
        except ValueError:
            messagebox.showerror("ผิดพลาด", "กรุณาใส่เวลาในรูปแบบ HH:MM (เช่น 08:00)")

    def check_timer(self):
        while True:
            now = datetime.now().strftime("%H:%M")
            for item in self.tasks:
                if item["time"] == now and not item["done"]:
                    item["done"] = True
                    # แจ้งเตือนด้วยหน้าต่างเด้ง
                    messagebox.showinfo("ได้เวลาแล้ว!", f"🔔 ถึงเวลาทำ: {item['task']}")
            
            time.sleep(30) # เช็คทุก 30 วินาที

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleTodoApp(root)
    root.mainloop()