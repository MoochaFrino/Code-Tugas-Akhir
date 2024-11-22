import tkinter as tk
from tkinter import messagebox 
from tkinter import PhotoImage

class Sparepart:
    def __init__(self, nama, stok):
        self.nama = nama
        self.stok = stok

class SparepartStore:
    def __init__(self):
        self.spareparts = [
            Sparepart("Oli Mesin", 20),
            Sparepart("Filter Udara", 7),
            Sparepart("Busi", 12),
            Sparepart("Rem Depan", 12),
            Sparepart("Rem Belakang", 16),
            Sparepart("Shockbreaker", 5),
            Sparepart("Knalpot", 9),
            Sparepart("Spion", 30),
            Sparepart("Lampu depan", 24),
            Sparepart("Ban", 40),
            Sparepart("Minyak rem", 17),
            Sparepart("Rantai", 9),
            Sparepart("Vbelt", 18)
        ]

    def get_spareparts(self):
        return self.spareparts

class App:
    def __init__(self, window):
        self.window = window
        self.window.title("Pengecekan Stok Sparepart Bengkel")
        self.window.geometry("500x500")
        self.window.configure(bg="#1A1A1D")
        self.window.resizable(False, False)
        self.image_path =PhotoImage(file=r"D:\Tugas kuliah\Coding\TA semester 1\Gambar\bengkel.png")
        bg_image = tk.Label(window, image=self.image_path)
        bg_image.place(relheight=1, relwidth=1)

        self.store = SparepartStore()
        self.jumlah_pesanan = 0

        # Frame untuk daftar sparepart
        self.frame_list = tk.Frame(window, bg="white")
        self.frame_list.pack(pady=50)

        # Label 
        self.label = tk.Label(self.frame_list, text="Daftar Sparepart:", font=("Times New Roman", 12, "bold"), bg="white", fg="#333333")
        self.label.pack()

        # Listbox dengan scrollbar
        self.listbox_frame = tk.Frame(self.frame_list)
        self.listbox_frame.pack()
        
        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.listbox_frame, yscrollcommand=self.scrollbar.set, font=("Times New Roman", 11), width=45, height=8, bg="#ffffff", fg="#333333", selectbackground="#4caf50",selectmode=tk.MULTIPLE)
        self.scrollbar.config(command=self.listbox.yview)
        
        self.listbox.pack(side=tk.LEFT)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Button Frame
        self.button_frame = tk.Frame(window, bg="white")
        self.button_frame.pack(pady=10)

        # Buttons
        self.button_check_stock = tk.Button(self.button_frame, text="Cek Stok", font=("Times new roman", 10, "bold"), bg="dark blue", fg="white", activebackground="red", activeforeground="white", width=15, command=self.check_stock)
        self.button_check_stock.grid(row=0, column=0, padx=5, pady=5)

        self.button_order = tk.Button(self.button_frame, text="Pesan Sparepart", font=("Times New Roman", 10, "bold"), bg="dark green", fg="white", activebackground="cyan", activeforeground="white", width=15, command=self.order_sparepart)
        self.button_order.grid(row=0, column=1, padx=5, pady=5)
        
        # Tombol Exit Program
        self.button_exit = tk.Button(window, text="Keluar", font=("Times New Roman", 10, "bold"), bg="red", fg="white", activebackground="dark red", activeforeground="white", width=15, command=self.exit_program)
        self.button_exit.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        self.populate_spareparts()

    def populate_spareparts(self):
        for sparepart in self.store.get_spareparts():
            self.listbox.insert(tk.END, sparepart.nama)

    def check_stock(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Peringatan", "Silahkan pilih sparepart.")
            return
    
        stok_info = []
        for index in selected_indices:
            sparepart = self.store.get_spareparts()[index]
            stok_info.append(f"{sparepart.nama} - Stok: {sparepart.stok}")
    
        messagebox.showinfo("Stok Sparepart", "\n".join(stok_info))

    def order_sparepart(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Peringatan", "Silahkan pilih sparepart.")
            return
    
        #Reset list orders sebelum membuat yang baru
        self.orders=[]

        # Frame baru untuk pemesanan
        self.order_frame = tk.Toplevel(self.window)
        self.order_frame.title("Pesan Sparepart")
        self.order_frame.geometry("400x400")
        self.order_frame.configure(bg="Cyan")
        self.order_frame.resizable(False, False)

        # Canvas dan scrollbar untuk scrollable area
        canvas = tk.Canvas(self.order_frame, bg="Cyan")
        scrollbar = tk.Scrollbar(self.order_frame, orient="vertical", command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame untuk konten yang scrollable
        content_frame = tk.Frame(canvas, bg="Cyan")
        canvas.create_window((0, 0), window=content_frame, anchor="n")

        # Aktifkan scrollwheel
        canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))

        # List untuk menyimpan pesanan
        self.orders = []
        for index in selected_indices:
            sparepart = self.store.get_spareparts()[index]
            order = {"sparepart": sparepart, "jumlah": 0}
            self.orders.append(order)

        # Tampilkan setiap sparepart yang dipilih untuk dipesan
        for i, order in enumerate(self.orders):
            frame = tk.Frame(content_frame, bg="white", padx=10, pady=10, relief="raised", bd=2)
            frame.pack(pady=10, padx=10, fill="x", expand=True)

            # Nama sparepart dan stok yang tersedia
            label = tk.Label(frame, text=f"{order['sparepart'].nama}\nStok Tersedia: {order['sparepart'].stok}", font=("Times New Roman", 12), bg="white", anchor="center")
            label.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

            # Jumlah pesanan
            jumlah_label = tk.Label(frame, text=f"Jumlah Pesanan: {order['jumlah']}", font=("Times New Roman", 12), bg="white", anchor="center")
            jumlah_label.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

            # Tombol untuk mengurangi dan menambah jumlah pesanan
            button_minus = tk.Button(frame, text="-", font=("Times New Roman", 12), width=6, command=lambda order=order, jumlah_label=jumlah_label: self.update_order_quantity(-1, order, jumlah_label))
            button_minus.grid(row=2, column=0, pady=5, padx=5)

            button_plus = tk.Button(frame, text="+", font=("Times New Roman", 12), width=6, command=lambda order=order, jumlah_label=jumlah_label: self.update_order_quantity(1, order, jumlah_label))
            button_plus.grid(row=2, column=1, pady=5, padx=5)

        # Tombol konfirmasi
        confirm_button = tk.Button(content_frame, text="Konfirmasi", font=("Times New Roman", 10, "bold"), bg="green", fg="white", command=self.confirm_orders)
        confirm_button.pack(pady=20, fill="x",padx=10)

        # Update scrollregion setelah semua konten ditambahkan
        content_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def update_order_quantity(self, change, order, jumlah_label):
        # Update jumlah pesanan dan batas stok
        order["jumlah"] = max(0, min(order["jumlah"] + change, order["sparepart"].stok))
        jumlah_label.config(text=f"Jumlah Pesanan: {order['jumlah']}")
        if order["sparepart"].stok == 0:
            messagebox.showwarning("Stok Habis", f"{order['sparepart'].nama} tidak tersedia saat ini.")
            return

    def confirm_orders(self):
        pesan = []
        for order in self.orders:
            if order["jumlah"] > 0:
                if order["jumlah"] <= order["sparepart"].stok:
                    order["sparepart"].stok -= order["jumlah"]
                    pesan.append(f"{order['jumlah']} {order['sparepart'].nama} (Stok tersisa: {order['sparepart'].stok})")
                else:
                    messagebox.showwarning("Peringatan", f"Pesanan {order['sparepart'].nama} melebihi stok!")
                    return

        if pesan:
            messagebox.showinfo("Pemesanan Berhasil", "Anda telah memesan:\n" + "\n".join(pesan))
        else:
            messagebox.showwarning("Peringatan", "Tidak ada pesanan yang dibuat.")
    
        self.order_frame.destroy()

        self.listbox.delete(0, tk.END)
        self.populate_spareparts()

    def exit_program(self):
        if messagebox.askokcancel("Exit", "Apakah Anda yakin ingin keluar?"): self.window.destroy()

if __name__ == "__main__":
    window = tk.Tk()
    app = App(window)
    window.mainloop()
