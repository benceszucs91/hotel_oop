import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self, roomnumber, ar):
        self.roomnumber = roomnumber
        self.ar = ar

    @abstractmethod
    def get_info(self):
        pass

class OnebedRoom(Room):
    def __init__(self, roomnumber):
        super().__init__(roomnumber, 10000)

    def get_info(self):
        return f"Egyágyas szoba {self.roomnumber}, Ár: {self.ar} Ft/éj"

class TwobedRoom(Room):
    def __init__(self, roomnumber):
        super().__init__(roomnumber, 15000)

    def get_info(self):
        return f"Kétágyas szoba {self.roomnumber}, Ár: {self.ar} Ft/éj"

class Reservation:
    def __init__(self, room, date):
        self.room = room
        self.date = date

    def __str__(self):
        return f"Foglalás - Szoba: {self.room.roomnumber}, Dátum: {self.date}, Ár: {self.room.ar} Ft"

class Hotel:
    def __init__(self, nev):
        self.nev = nev
        self.rooms = []
        self.reservations = []

    def room_hozzaadas(self, room):
        self.rooms.append(room)

    def room_reservation(self, roomnumber, date):
        for room in self.rooms:
            if room.roomnumber == roomnumber:
                if not self.ellenoriz_reservation(room, date):
                    reservation = Reservation(room, date)
                    self.reservations.append(reservation)
                    return f"Foglalás sikeres: {reservation}"
                else:
                    return "Ez a szoba már foglalt a megadott dátumra."
        return "Nincs ilyen szobaszám."

    def reservation_cancel(self, roomnumber, date):
        for reservation in self.reservations:
            if reservation.room.roomnumber == roomnumber and reservation.date == date:
                self.reservations.remove(reservation)
                return "Foglalás sikeresen lemondva."
        return "Nincs ilyen foglalás."

    def osszes_reservation_listazasa(self):
        if not self.reservations:
            return "Nincsenek foglalások."
        return "\n".join(str(reservation) for reservation in self.reservations)

    def ellenoriz_reservation(self, room, date):
        for reservation in self.reservations:
            if reservation.room == room and reservation.date == date:
                return True
        return False

def felhasznaloi_interfesz():
    szalloda = Hotel("Példa Szálloda")
    szalloda.room_hozzaadas(OnebedRoom(101))
    szalloda.room_hozzaadas(TwobedRoom(102))
    szalloda.room_hozzaadas(OnebedRoom(103))

    szalloda.room_reservation(101, "2024-06-01")
    szalloda.room_reservation(102, "2024-06-02")
    szalloda.room_reservation(103, "2024-06-03")
    szalloda.room_reservation(101, "2024-06-04")
    szalloda.room_reservation(102, "2024-06-05")

    def reservation():
        roomnumber = int(room_number_entry.get())
        date = cal.get_date()
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        if date_obj > datetime.now().date():
            uzenet = szalloda.room_reservation(roomnumber, date)
            messagebox.showinfo("Foglalás", uzenet)
        else:
            messagebox.showerror("Hiba", "Csak jövőbeni dátumokra lehet foglalni.")

    def cancel():
        roomnumber = int(room_number_entry.get())
        date = cal.get_date()
        uzenet = szalloda.reservation_cancel(roomnumber, date)
        messagebox.showinfo("Lemondás", uzenet)

    def listazas():
        reservations = szalloda.osszes_reservation_listazasa()
        messagebox.showinfo("Foglalások", reservations)

    root = tk.Tk()
    root.title("Szálloda Roomfoglalási Rendszer")

    room_number_label = tk.Label(root, text="Szobaszám:")
    room_number_label.pack()
    room_number_entry = tk.Entry(root)
    room_number_entry.pack()

    date_label = tk.Label(root, text="Válasszon dátumot:")
    date_label.pack()
    cal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=20)

    reservation_btn = tk.Button(root, text="Foglalás", command=reservation)
    reservation_btn.pack(pady=5)

    cancel_btn = tk.Button(root, text="Lemondás", command=cancel)
    cancel_btn.pack(pady=5)

    listazas_btn = tk.Button(root, text="Összes foglalás listázása", command=listazas)
    listazas_btn.pack(pady=5)

    room_lista = tk.Listbox(root, width=40)
    room_lista.pack(pady=20)

    for room in szalloda.rooms:
        room_lista.insert(tk.END, room.get_info())

    root.mainloop()

if __name__ == "__main__":
    felhasznaloi_interfesz()
