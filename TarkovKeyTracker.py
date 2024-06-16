from tkinter import *
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import os.path
import sqlite3

# Declare path for db
path = './database.db'

# Global vars
dbExists = os.path.isfile(path)

# Tkinter stuff
root = Tk()
root.title('JohnnyChops Keypedia')

def searchKey():
    keyResult = keyEntry.get()
    if keyResult:
        top = Toplevel()
        top.geometry("1200x600")
        top.config(bg='gray63')

        # Create a frame for the canvas and scrollbar
        frame = Frame(top, bg='gray63')
        frame.pack(fill=BOTH, expand=1)

        # Create a canvas and add it to the frame
        canvas = Canvas(frame, bg='gray63')
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add a scrollbar to the frame
        scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create another frame inside the canvas
        result_frame = Frame(canvas, bg='gray63')
        canvas.create_window((0, 0), window=result_frame, anchor="nw")

        Label(result_frame, bg='yellow', text=f"Results for '{keyResult}':").grid(row=0, column=0, columnspan=3)

        # Database search logic here
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("SELECT * FROM Keys WHERE key LIKE ?", ('%' + keyResult + '%',))
        results = c.fetchall()
        conn.close()

        if results:
            for idx, result in enumerate(results, start=1):
                Label(result_frame, bg='cornflower blue', text=f"Key: {result[0]}").grid(row=idx, column=0, padx=10, pady=5)
                Label(result_frame, bg='green', text=f"Amount: {result[1]}").grid(row=idx, column=1, padx=10, pady=5)
                Label(result_frame, bg='gray63', text=f"Description: {result[2]}").grid(row=idx, column=2, padx=10, pady=5)
        else:
            Label(result_frame, text="No results found.", bg='gray63').grid(row=1, column=0, columnspan=3)
    else:
        messagebox.showerror("Error", "Please enter a key to search.")


def createdb():
    global dbExists
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS Keys")
    c.execute('''CREATE TABLE Keys (
                    key TEXT,
                    amount INTEGER,
                    description TEXT
                )''')
    # Insert predefined keys with descriptions
    initial_keys = [
        ('factory emergency exit key', 0, 'Factory key, keep used for doors on factory and that one big doorway on customs'),
        ('pumping station back door key', 0, 'This is an optional location for the quest Sanitary Standards - Part 1 otherwise trash, spit on it'),
        ('pumping station front door key', 0, 'This is an optional location for the quest Sanitary Standards - Part 1 otherwise trash, spit on it'),
        ('dorm guard desk key', 0, 'Customs key, okay early game loot keep if poor, not a rare key'),
        ('dorm overseer key', 0, 'Customs. Keep needed for Against the Conscience - Part 1 and quest Decisions, Decisions or Between Two Fires decent loose loot'),
        ('dorm room 103 key', 0, 'Customs. eh, might as well keep, spawns food items, good for those timmys who always forget to eat and whine about needing food if you preston drop'),
        ('dorm room 104 key', 0, 'Customs two stack dorms, kinda bad loot, one toolbox and two jackets keep if running customs'),
        ('dorm room 105 key', 0, 'Customs two stack always spawns keep, one safe spawn and loose loot'),
        ('dorm room 108 key', 0, 'Customs three stack mid loot, one drawers, one pc, loose loot'),
        ('dorm room 110 key', 0, 'customs three stack always spawns in one of the building in some locker, possible fuel con fuel, flash drive car battery spawn, keep.'),
        ('dorm room 114 key', 0, 'Customs three stack keep for pharmacist quest, supposed to spawn in the jacket at the checkpoint'),
        ('dorm room 118 key', 0, 'Customs three stack, has tweo jackets keep if enough space'),
        ('dorm room 203 key', 0, 'customs three stack keep for shaking up teller, only has two duffle bags '),
        ('dorm room 204 key', 0, 'Customs three stack, kinda trahs one weapon locker, loose loot'),
        ('dorm room 206 key', 0, 'customs two stack quest to make therapist all wet or something otherwise can maybe spawn w filters'),
        ('dorm room 214 key', 0, 'customs three stack This is an optional quest location for the Quest Shaking up the Teller if you dont have a Dorm room 203 key has a safe loose loot'),
        ('dorm room 218 key', 0, 'customs three stack loose weapon loot, kinda trash'),
        ('dorm room 220 key', 0, 'customs three stack needed for hand in for chemical part 1 and need for part 2 so dont sell it. zb-14 key spawn jack duffle and roubles'),
        ('dorm room 303 key', 0, 'customs three stack needed for golden swag and trust regain, trash loot, one crate, loose weapon loot'),
        ('dorm room 306 key', 0, 'customs three stack bad key trash put it down'),
        ('dorm room 308 key', 0, 'customs three stack trash, used in a cwaft to make thermite so turns out thermite be a use for it afterall'),
        ('dorm room 314 marked key', 0, 'Keep you big dummy, gotta mark the sp00ky spot or whatever'),
        ('dorm room 315 key', 0, 'customs three stack trash, loose roubles'),
        ('gas station office key', 0, 'Customs, gas station, decent loot, can see out the windows'),
        ('gas station storage room key', 0, 'customs gas station, need one for trust reain quest trash loot, one medbad and medcase'),
        ('machinery key', 0, 'customs keep needed for bronze pocket watch and for your casual friends who havent dont the quest'),
        ('military checkpoint key', 0, 'customs, trash loot, weapon rack grenade case, wooden ammo case can be used in a trade for m2 sword'),
        ('portable bunkhouse key', 0, 'customs no loot, needed for bad rep evidence'),
        ('portable cabin key', 0, 'customs not the one for golden ziboo, but it got some loot, 3 jackets loose loot, right next to golden zibbo'),
        ('tarcone directors office key', 0, 'customs big red (if you dont chew big red frick you) needed for delivery from the past and farming pt 3 also decent loot'),
        ('trailer park portable cabin key', 0, 'customs needed for golden zibbo no loot, trash'),
        ('unknown key', 0, 'not a clue'),
        ('usec stash key', 0, 'customs warehouse, keep decent loot'),
        ('shatuns hideout', 0, 'woods arena shit, in the house in the western village'),
        ('shturmans stash key', 0, 'woods keep, stash in on the log pile'),
        ('yotota car key', 0, 'The pickup truck parked in the lumber yard next to the three cabins on Woods. loose loot also for a trade from skier for an mp-153'),
        ('zb-014 key', 0, 'woods keep bunker boy is an extract sometimes and has loot for some icecream cones'),
        ('cottage back door key', 0, 'Description for key4'),
        ('cottage safe key', 0, 'Description for key4'),
        ('gas station safe key', 0, 'Description for key4'),
        ('health resort east wing office room 107 key', 0, 'Description for key4'),
        ('Health Resort east wing office room 108 key', 0, 'Description for key4'),
        ('Health Resort east wing room 205 key', 0, 'Description for key4'),
        ('Health Resort east wing room 206 key', 0, 'Description for key4'),
        ('Health Resort east wing room 209 key', 0, 'Description for key4'),
        ('Health Resort east wing room 213 key', 0, 'Description for key4'),
        ('Health Resort east wing room 216 key', 0, 'Description for key4'),
        ('Health Resort east wing room 222 key', 0, 'Description for key4'),
        ('Health Resort east wing room 226 key', 0, 'Description for key4'),
        ('Health Resort east wing room 306 key', 0, 'Description for key4'),
        ('Health Resort east wing room 308 key', 0, 'Description for key4'),
        ('Health Resort east wing room 310 key', 0, 'Description for key4'),
        ('Health Resort east wing room 313 key', 0, 'Description for key4'),
        ('Health Resort east wing room 314 key', 0, 'Description for key4'),
        ('Health Resort east wing room 316 key', 0, 'Description for key4'),
        ('Health Resort east wing room 322 key', 0, 'Description for key4'),
        ('Health Resort east wing room 328 key', 0, 'Description for key4'),
        ('Health Resort management office safe key', 0, 'Description for key4'),
        ('Health Resort management warehouse safe key', 0, 'Description for key4'),
        ('Health Resort office key with a blue tape', 0, 'Description for key4'),
        ('Health Resort universal utility room key', 0, 'Description for key4'),
        ('Health Resort west wing office room 104 key', 0, 'Description for key4'),
        ('Health Resort west wing office room 112 key', 0, 'Description for key4'),
        ('Health Resort west wing room 203 key', 0, 'Description for key4'),
        ('Health Resort west wing room 203 key', 0, 'Description for key4'),
        ('Health Resort west wing room 205 key', 0, 'Description for key4'),
        ('Health Resort west wing room 207 key', 0, 'Description for key4'),
        ('Health Resort west wing room 216 key', 0, 'Description for key4'),
        ('Health Resort west wing room 218 key', 0, 'Description for key4'),
        ('Health Resort west wing room 219 key', 0, 'Description for key4'),
        ('Health Resort west wing room 220 key', 0, 'Description for key4'),
        ('Health Resort west wing room 221 key', 0, 'Description for key4'),
        ('Health Resort west wing room 222 key', 0, 'Description for key4'),
        ('Health Resort west wing room 301 key', 0, 'Description for key4'),
        ('Health Resort west wing room 303 key', 0, 'Description for key4'),
        ('Health Resort west wing room 306 key', 0, 'Description for key4'),
        ('Health Resort west wing room 309 key', 0, 'Description for key4'),
        ('Health Resort west wing room 321 safe key', 0, 'Description for key4'),
        ('Health Resort west wing room 323 key', 0, 'Description for key4'),
        ('Health Resort west wing room 325 key', 0, 'Description for key4'),
        ('HEP station storage room key', 0, 'Description for key4'),
        ('SMW car key', 0, 'Description for key4'),
        ('Vorons hideout key', 0, 'Description for key4'),
        ('Weather station safe key', 0, 'Description for key4'),
        ('EMERCOM medical unit key', 0, 'interchange starts here for key4'),
        ('Goshan cash register key', 0, 'Description for key4'),
        ('Grumpys hideout key', 0, 'Description for key4'),
        ('IDEA cash register key', 0, 'Description for key4'),
        ('Kiba Arms inner grate door key', 0, 'Description for key4'),
        ('Kiba Arms outer door key', 0, 'Description for key4'),
        ('NecrusPharm pharmacy key', 0, 'Description for key4'),
        ('Object 11SR keycard', 0, 'Description for key4'),
        ('Object 21WS keycard', 0, 'Description for key4'),
        ('OLI administration office key', 0, 'Description for key4'),
        ('OLI cash register key', 0, 'Description for key4'),
        ('OLI logistics department office key', 0, 'Description for key4'),
        ('OLI outlet utility room key', 0, 'Description for key4'),
        ('Power substation utility cabin key', 0, 'Description for key4'),
        ('ULTRA medical storage key', 0, 'Description for key4'),
        ('Abandoned factory marked key', 0, 'street start here'),
        ('Archive room key', 0, 'Description for key4'),
        ('Aspect company office key', 0, 'Description for key4'),
        ('Backup hideout key', 0, 'Description for key4'),
        ('Beluga restaurant director key', 0, 'Description for key4'),
        ('Car dealership closed section key', 0, 'Description for key4'),
        ('Car dealership directors office room key', 0, 'Description for key4'),
        ('Cargo container mesh door key', 0, 'Description for key4'),
        ('Chekannaya 15 apartment key', 0, 'Description for key4'),
        ('Concordia apartment 8 home cinema key', 0, 'Description for key4'),
        ('Concordia apartment 8 room key', 0, 'Description for key4'),
        ('Concordia apartment 34 room key', 0, 'Description for key4'),
        ('Concordia apartment 63 room key', 0, 'Description for key4'),
        ('Concordia apartment 64 key', 0, 'Description for key4'),
        ('Concordia apartment 64 office room key', 0, 'Description for key4'),
        ('Concordia security room key', 0, 'Description for key4'),
        ('Construction site bunkhouse key', 0, 'Description for key4'),
        ('Financial institution office key', 0, 'Description for key4'),
        ('Financial institution small office key', 0, 'Description for key4'),
        ('Iron gate key', 0, 'Description for key4'),
        ('Negotiation room key', 0, 'Description for key4'),
        ('MVD academy entrance hall guard room key', 0, 'Description for key4'),
        ('Mysterious room marked key', 0, 'Description for key4'),
        ('PE teachers office key', 0, 'Description for key4'),
        ('Pinewood hotel room 206 key', 0, 'Description for key4'),
        ('Pinewood hotel room 215 key', 0, 'Description for key4'),
        ('Primorsky 46-48 skybridge key', 0, 'Description for key4'),
        ('Primorsky 48 apartment key', 0, 'Description for key4'),
        ('Real estate agency office room key', 0, 'Description for key4'),
        ('Relaxation room key', 0, 'Description for key4'),
        ('Rusted bloody key', 0, 'Description for key4'),
        ('Stair landing key', 0, 'Description for key4'),
        ('Store managers key', 0, 'Description for key4'),
        ('Supply department directors office key', 0, 'Description for key4'),
        ('Tarbank cash register department key', 0, 'Description for key4'),
        ('TerraGroup meeting room key', 0, 'Description for key4'),
        ('TerraGroup security armory key', 0, 'Description for key4'),
        ('X-ray room key', 0, 'Description for key4'),
        ('Zmeisky 3 apartment 8 key', 0, 'Description for key4'),
        ('Zmeisky 5 apartment 20 key', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),
        ('key323', 0, 'Description for key4'),



    ]
    c.executemany("INSERT INTO Keys (key, amount, description) VALUES (?, ?, ?)", initial_keys)
    conn.commit()
    conn.close()
    dbExists = True

if not dbExists:
    createdb()
else:
    print("Database exists.")

# Label
keyEntry = Entry(root, width=35, borderwidth=5)
keyEntry.grid(row=1, column=0, columnspan=20, padx=100, pady=50)

# Button
searchButton = Button(root, text="Search", command=searchKey)
searchButton.grid(row=1, column=18, padx=10)

# Mainloop
root.mainloop()