from ast import Lambda
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_tp3_dpbo"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)
    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    # Input 3
    optJK = [
        ("Laki-laki", "Laki-laki"),
        ("Perempuan", "Perempuan")
    ]
    input_jenisKelamin = StringVar()
    input_jenisKelamin.set("Laki-laki")
    label3 = Label(dframe, text="Jenis Kelamin").grid(row=2, column=0, sticky="w")
    jkcol = 1
    def clicked(value):
        myLabel = Label(top, text=value)
        myLabel.pack()
    for text, jk in optJK:
        Radiobutton(dframe, text=text, variable=input_jenisKelamin, value=jk).grid(row=2, column=jkcol, padx=20, pady=10, sticky='w')
        jkcol += 1

    # Input 4
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label4 = Label(dframe, text="Jurusan").grid(row=3, column=0, sticky="w")
    input4 = OptionMenu(dframe, input_jurusan, *options)
    input4.grid(row=3, column=1, padx=20, pady=10, sticky='w')

    # Input 5
    def comboclick(event):
        myLabel = Label(top, text=input_hobi.get()).pack()
    optHobi = ["Bermain game", "Jalan-jalan", "Baca novel", "Nonton film", "Bernyanyi"]
    label5 = Label(dframe, text="Hobi").grid(row=4, column=0, sticky="w")
    input_hobi = ttk.Combobox(dframe, value=optHobi)
    input_hobi.current(0)
    input_hobi.grid(row=4, column=1, padx=20, pady=10, sticky='w')

    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[insertData(top, input_nama, input_nim, input_jurusan, input_jenisKelamin, input_hobi), top.withdraw()])
    btn_submit.grid(row=3, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Gak jadi / Kembali", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=3, column=1, padx=10)

# Untuk memasukan data
def insertData(parent, nama, nim, jurusan, jenis_kelamin, hobi):
    top = Toplevel()
    # Get data
    nama = nama.get()
    nim = nim.get()
    jurusan = jurusan.get()
    jenis_kelamin = jenis_kelamin.get()
    hobi = hobi.get()

    # cek jika data mahasiswa lengkap
    if nama and nim and jurusan and jenis_kelamin and hobi:
        # Input data disini
        sql = "INSERT INTO mahasiswa (nim, nama, jurusan, jenis_kelamin, hobi) VALUES (%s, %s, %s, %s, %s)"
        val = (nim, nama, jurusan, jenis_kelamin, hobi)
        dbcursor.execute(sql, val)
        mydb.commit()
        btn_ok = Button(top, text="Syap! Data masuk", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
    # jika ada data yang kosong
    else:
        btn_ok = Button(top, text="Data ada yang kosong!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
  
# Window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title4 = Label(tableFrame, text="Jenis Kelaim", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title4 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label4 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label4 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=5)
        i += 1

# Dialog konfirmasi hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Window fasilitas kampus
def viewFasilitas():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Daftar Fasilitas Kampus")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Fasilitas Kampus")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    photoFrame = LabelFrame(frame)
    photoFrame.grid(row=1, column = 0, columnspan=2)

    # Ambil data foto
    my_img1 = ImageTk.PhotoImage(Image.open('images/lab_mikrobiologi_resize.jpg'))
    my_img2 = ImageTk.PhotoImage(Image.open('images/lab_mutlimedia_resize.jpg'))
    my_img3 = ImageTk.PhotoImage(Image.open('images/lab_teknik_produksi_resize.jpg'))
    my_img4 = ImageTk.PhotoImage(Image.open('images/perpustakaan_resize.jpg'))
    image_list = [my_img1, my_img2, my_img3, my_img4]

    # Tampilkan nomor foto
    status = Label(photoFrame, text="Image 1 of " + str(len(image_list)), bd=1, relief=SUNKEN, anchor=E)

    # Buat label foto
    photoLabel = Label(photoFrame, image=my_img1)
    photoLabel.grid(row=2, column=0, columnspan=3)

    # Tombol next
    def forward(image_number):
        nonlocal photoLabel
        nonlocal btn_forward
        nonlocal btn_backward

        # Proses maju ke foto selanjutnya
        photoLabel.grid_forget()
        photoLabel = Label(photoFrame, image=image_list[image_number - 1])
        btn_forward = Button(photoFrame, text=">>", command=lambda: forward(image_number + 1))
        btn_backward = Button(photoFrame, text="<<", command=lambda: back(image_number - 1))

        # Matikan tombol next jika sudah mencapai foto terakhir
        if image_number == len(image_list):
            btn_forward = Button(photoFrame, text=">>", state=DISABLED)

        photoLabel.grid(row=2, column=0, columnspan=3)
        btn_backward.grid(row=3, column=0)
        btn_forward.grid(row=3, column=2)

        # Update nomor foto
        status = Label(photoFrame, text="Image " + str(image_number) +" of " + str(len(image_list)), bd=1, relief=SUNKEN, anchor=E)
        status.grid(row=4, column=0, columnspan=3, sticky=W+E)

    # Tombol back
    def back(image_number):
        nonlocal photoLabel
        nonlocal btn_forward
        nonlocal btn_backward

        # Proses mundur ke foto sebelumnya
        photoLabel.grid_forget()
        photoLabel = Label(photoFrame, image=image_list[image_number - 1])
        btn_forward = Button(photoFrame, text=">>", command=lambda: forward(image_number + 1))
        btn_backward = Button(photoFrame, text="<<", command=lambda: back(image_number - 1))

        # Matikan tombol back jika sudah mencapai foto pertama
        if image_number == 1:
            btn_backward = Button(photoFrame, text="<<", state=DISABLED)

        photoLabel.grid(row=2, column=0, columnspan=3)
        btn_backward.grid(row=3, column=0)
        btn_forward.grid(row=3, column=2)

        # Update nomor foto
        status = Label(photoFrame, text="Image " + str(image_number) +" of " + str(len(image_list)), bd=1, relief=SUNKEN, anchor=E)
        status.grid(row=4, column=0, columnspan=3, sticky=W+E)

    # Display button
    btn_backward = Button(photoFrame, text="<<", command=lambda: back(), state=DISABLED)
    btn_forward = Button(photoFrame, text=">>", command=lambda: forward(2))

    btn_backward.grid(row=3, column=0)
    btn_forward.grid(row=3, column=2, pady=10)
    status.grid(row=4, column=0, columnspan=3, sticky=W+E)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

def delAll():
    top = Toplevel()
    # Delete data disini
    sql = "DELETE FROM mahasiswa"
    dbcursor.execute(sql)
    mydb.commit()

    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(pady=20)

# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=2, column=0, pady=5)

# View fasilitas btn
b_fasilitas = Button(buttonGroup, text="Daftar Fasilitas Kampus", command=viewFasilitas, width=30)
b_fasilitas.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()