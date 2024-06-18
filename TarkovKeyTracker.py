from tkinter import *
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import os.path
import sqlite3

# Declare path for db
path = './database.db'

# Global vars
dbExists = os.path.isfile(path)
result_frame = None
top = None

# Tkinter stuff
root = Tk()
root.title('JohnnyChops Keypedia')

def addKey(key):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("UPDATE Keys SET amount = amount + 1 WHERE key = ?", (key,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Updated", f"added {key}")

def subtractKey(key):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("UPDATE Keys SET amount = amount - 1 WHERE key = ? AND amount > 0", (key,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Updated", f"removed {key}")

def refreshResults():
    global result_frame
    if result_frame is not None:
        for widget in result_frame.winfo_children():
            widget.destroy()

        keyResult = keyEntry.get()
        Label(result_frame, bg='yellow', text=f"Results for '{keyResult}':").grid(row=0, column=0, columnspan=5)

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
                Button(result_frame, text="+", command=lambda key=result[0]: addKey(key)).grid(row=idx, column=3, padx=5)
                Button(result_frame, text="-", command=lambda key=result[0]: subtractKey(key)).grid(row=idx, column=4, padx=5)
        else:
            Label(result_frame, text="No results found.", bg='gray63').grid(row=1, column=0, columnspan=5)

def searchKey():
    global result_frame, top
    keyResult = keyEntry.get()
    if keyResult:
        if top is None or not top.winfo_exists():
            top = Toplevel()
            top.geometry("1800x600")
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

            # Add refresh button
            Button(top, text="Refresh", command=refreshResults).pack()

        refreshResults()
    else:
        messagebox.showerror("Error", "Please enter a key to search.")

def showAllKeys():
    global result_frame, top
    if top is None or not top.winfo_exists():
        top = Toplevel()
        top.geometry("1800x600")
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

    for widget in result_frame.winfo_children():
        widget.destroy()

    Label(result_frame, bg='yellow', text="All Keys with Amount > 0:").grid(row=0, column=0, columnspan=5)

    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT * FROM Keys WHERE amount > 0")
    results = c.fetchall()
    conn.close()

    if results:
        for idx, result in enumerate(results, start=1):
            Label(result_frame, bg='cornflower blue', text=f"Key: {result[0]}").grid(row=idx, column=0, padx=10, pady=5)
            Label(result_frame, bg='green', text=f"Amount: {result[1]}").grid(row=idx, column=1, padx=10, pady=5)
            Label(result_frame, bg='gray63', text=f"Description: {result[2]}").grid(row=idx, column=2, padx=10, pady=5)
            Button(result_frame, text="+", command=lambda key=result[0]: addKey(key)).grid(row=idx, column=3, padx=5)
            Button(result_frame, text="-", command=lambda key=result[0]: subtractKey(key)).grid(row=idx, column=4, padx=5)
    else:
        Label(result_frame, text="No keys with amount > 0 found.", bg='gray63').grid(row=1, column=0, columnspan=5)



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
        ('dorm room 204 key', 0, 'Customs three stack, kinda trash one weapon locker, loose loot'),
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
        ('cottage back door key', 0, 'shoreline back door to cottage needed for quest Colleagues - Part 2 some loot inside'),
        ('cottage safe key', 0, 'shoreline Unlocks the safe on the second floor in the locked Villa on Shoreline'),
        ('gas station safe key', 0, 'literally useless its always unlocked'),
        ('health resort east wing office room 107 key', 0, 'shoreline ledx and gpu spawn'),
        ('Health Resort east wing office room 108 key', 0, 'shoreline again useless rooms always unlocked'),
        ('Health Resort east wing room 205 key', 0, 'shoreline can get to 206 few weapon boxes loose meds'),
        ('Health Resort east wing room 206 key', 0, 'shoreline can get to 205, few weapon boxes loose meds, Rare loose loot'),
        ('Health Resort east wing room 209 key', 0, 'shoreline can get to 213, however its always open silly guy '),
        ('Health Resort east wing room 213 key', 0, 'shoreline its always open silly guy'),
        ('Health Resort east wing room 216 key', 0, 'shoreline its always open silly guy'),
        ('Health Resort east wing room 222 key', 0, 'also opens e226 good room, ledx bitcoin'),
        ('Health Resort east wing room 226 key', 0, 'also opens e222 good room, ledx bitcoin'),
        ('Health Resort east wing room 306 key', 0, 'shoreline also opens E308 cargo x part 1 and lend lease part 1 led x spawn dvl spawn'),
        ('Health Resort east wing room 308 key', 0, 'shoreline also opens E306 cargo x part 1 and lend lease part 1 led x spawn dvl spawn'),
        ('Health Resort east wing room 310 key', 0, 'shoreline splish splash throw this key in the trash'),
        ('Health Resort east wing room 313 key', 0, 'shoreline also opens E314'),
        ('Health Resort east wing room 314 key', 0, 'shoreline also opens e314 ledx med bags weapons'),
        ('Health Resort east wing room 316 key', 0, 'shoreline poor loot weapon case sv-98 basically trash'),
        ('Health Resort east wing room 322 key', 0, 'shoreline its always open silly guy'),
        ('Health Resort east wing room 328 key', 0, 'shoreline also opens utility room ledx gpu spawn pc and duffle Used in the Quest Wet Job - Part 5 when you dont have a Health Resort universal utility room key'),
        ('Health Resort management office safe key', 0, 'shoreline safe key duh'),
        ('Health Resort management warehouse safe key', 0, 'shoreline safe key duh'),
        ('Health Resort office key with a blue tape', 0, 'shoreline Sanny boys key The first floor, room 110 ledx and gpu spawn quest Chemistry Closet '),
        ('Health Resort universal utility room key', 0, 'shoreline also opens E328 ledx gpu spawn pc and duffle Used in the Quest Wet Job - Part 5'),
        ('Health Resort west wing office room 104 key', 0, 'shoreline ledx and blue keycard spwan'),
        ('Health Resort west wing office room 112 key', 0, 'shoreline Needed for the Quest Vitamins - Part 1 Blue keycard spawn location '),
        ('Health Resort west wing room 203 key', 0, 'shoreline also opens W205 mulitple ledx / gpu spawns in both rooms'),
        ('Health Resort west wing room 205 key', 0, 'shoreline for key4 also opens w203 mulitple ledx / gpu spawns in both rooms'),
        ('Health Resort west wing room 207 key', 0, 'shoreline splish splash throw this key in the trash its always open'),
        ('Health Resort west wing room 216 key', 0, 'shoreline Needed for the quest Lend-Lease - Part 1 ledx spawn weapon parts spawn loose loot'),
        ('Health Resort west wing room 218 key', 0, 'shoreline also opens W221/W222 loose loot and duffles decent filler key'),
        ('Health Resort west wing room 219 key', 0, 'shoreline Used in the Quest Spa Tour - Part 4 when you dont have a Health Resort west wing room 220 key 3m armor spawn loose loot'),
        ('Health Resort west wing room 220 key', 0, 'shoreline Used in the Quest Spa Tour - Part 4 when you dont have a Health Resort west wing room 219 key loose loot weapon boxes'),
        ('Health Resort west wing room 221 key', 0, 'shoreline also opens W218/W222 loose loot and duffles decent filler key'),
        ('Health Resort west wing room 222 key', 0, 'shoreline also opens W220/W218 loose loot and duffles decent filler key'),
        ('Health Resort west wing room 301 key', 0, 'shoreline also opens w304 good room multiple ledx and gpu spawns'),
        ('Health Resort west wing room 303 key', 0, 'shoreline NOT USED FOR A QUEST ITS ALWAYS OPEN DONT BUY IT'),
        ('Health Resort west wing room 306 key', 0, 'shoreline Used in the Quest Health Care Privacy - Part 2 loose loot dead scav'),
        ('Health Resort west wing room 309 key', 0, 'its always open silly guy'),
        ('Health Resort west wing room 321 safe key', 0, 'shoreline safe key'),
        ('Health Resort west wing room 323 key', 0, 'shoreline its always open silly guy'),
        ('Health Resort west wing room 325 key', 0, 'shoreline its always open silly guy'),
        ('HEP station storage room key', 0, 'shoreline weapon boxes one intel spawn inside water power'),
        ('SMW car key', 0, 'shoreline blue car at cottages loose loot'),
        ('Vorons hideout key', 0, 'shoreline arena key'),
        ('Weather station safe key', 0, 'shoreline its always open silly guy'),
        ('EMERCOM medical unit key', 0, 'interchange Needed for the Quest Vitamins - Part 1 loose meds ledx portable defib'),
        ('Goshan cash register key', 0, 'interchange 1 needs to be found for the quest Supervisor 30 cash registers'),
        ('Grumpys hideout key', 0, 'interchange arena key'),
        ('IDEA cash register key', 0, 'interchange 20 cash registers'),
        ('Kiba Arms inner grate door key', 0, 'interchange one of two keys for kiba This is a required location for the quest Provocation lotta guns armor etc'),
        ('Kiba Arms outer door key', 0, 'interchange one of two keys for kiba This is a required location for the quest Provocation lotta guns armor etc'),
        ('NecrusPharm pharmacy key', 0, 'interchange loose med spawn, tales tell of a ledx spawn but I have no proof'),
        ('Object 11SR keycard', 0, 'interchange exit key This is a required location for the quest Provocation'),
        ('Object 21WS keycard', 0, 'interchange weapon stash, as the name implies weapon loose loot'),
        ('OLI administration office key', 0, 'interchange one pc and loose loot'),
        ('OLI cash register key', 0, 'interchange 18 cash registers'),
        ('OLI logistics department office key', 0, 'Required for the quest Database - Part 2 from Ragman one pc loose loot'),
        ('OLI outlet utility room key', 0, 'interchange basic loose loot'),
        ('Power substation utility cabin key', 0, 'interchagne cabin outside power, one mp-153 spawn, weapon box'),
        ('ULTRA medical storage key', 0, 'interchange big money room ledx defibs stims meds'),
        ('Abandoned factory marked key', 0, 'streets This is a required location for the quest Broadcast - Part 4 rare loot spawn'),
        ('Archive room key', 0, 'streets 2 drawers and a locked safe'),
        ('Aspect company office key', 0, 'This key is not necessary to get into the building since it has a hole in the wall on the backside.'),
        ('Backup hideout key', 0, 'streets This is a required location for the quest Missing Informant duffle rare loot spawn loose loot'),
        ('Beluga restaurant director key', 0, 'streets This is a possible location for the quest Beyond the Red Meat - Part 1 pcs jackets loose loot valuables '),
        ('Car dealership closed section key', 0, 'streets This is a required location for the quest Your Car Needs a Service tech crate loose loot pc weapons cases'),
        ('Car dealership directors office room key', 0, 'streets This is a required location for the quest Your Car Needs a Service 2 drawers pc valuable loose loot'),
        ('Cargo container mesh door key', 0, 'streets weapon boxes loose loot'),
        ('Chekannaya 15 apartment key', 0, 'streets This is a required location for the quest House Arrest - Part 2 loose loot electronics stims valuables'),
        ('Concordia apartment 8 home cinema key', 0, 'streets  valuable loose loot'),
        ('Concordia apartment 8 room key', 0, 'streets  valuable loose loot'),
        ('Concordia apartment 34 room key', 0, 'streets Loose loot Valuables, Electronics, Provisions ammo boxes'),
        ('Concordia apartment 63 room key', 0, 'streets Loose loot Valuables, Electronics, Medical items, Stimulants'),
        ('Concordia apartment 64 key', 0, 'streets Loose loot Valuables, Provisions, Paper ammo boxes, Other items'),
        ('Concordia apartment 64 office room key', 0, 'streets Loose loot Electronics, Other items'),
        ('Concordia security room key', 0, 'streets This is a required location for the quest Surveillance 2 pcs safe  weapon loose loot'),
        ('Construction site bunkhouse key', 0, 'streets med loose loot 2 jackets med boxes'),
        ('Financial institution office key', 0, 'streets 5 pcs 1 duffle Loose loot Valuables, Provisions, Building materials, Household materials, Energy elements'),
        ('Financial institution small office key', 0, 'streets pc drawers safe'),
        ('Iron gate key', 0, 'streets This is a required location for the quest House Arrest - Part 1  Loose loot Valuables, Provisions, Stimulants, Electronics,ammo, Other items  '),
        ('Negotiation room key', 0, 'streets This is a required location for the quest Developers Secrets - Part 1 Loose loot (Valuables) medbag relax room key sometimes on metal table'),
        ('MVD academy entrance hall guard room key', 0, 'streets dead scav t5000 sports bag'),
        ('Mysterious room marked key', 0, 'streets This is a required location for the quest Broadcast - Part 5 Loose loot(multiple very rare Valuables, Weapons, Containers, Currency, Keycards'),
        ('PE teachers office key', 0, 'streets Loose loot Provisions'),
        ('Pinewood hotel room 206 key', 0, 'streets empty safe (nikita why?) Loose loot Provisions, Energy elements, Flammable materials '),
        ('Pinewood hotel room 215 key', 0, 'streets This is a required location for the quest Watching You Loose loot (Provisions, Energy elements, Flammable materials) '),
        ('Primorsky 46-48 skybridge key', 0, 'streets This is a required location for the quests Ballet Lover, Audiophile and Spotter 1 pc Loose loot (Valuables, Electronics)'),
        ('Primorsky 48 apartment key', 0, 'streets Loose loot (Valuables, Electronics)'),
        ('Real estate agency office room key', 0, 'streets This is a possible location for the quest Properties All Around Loose loot (Valuables, Electronics) '),
        ('Relaxation room key', 0, 'streets This is a required location for the quest Developers Secrets - Part 2 high value loot multiple duffles'),
        ('Rusted bloody key', 0, 'streets This is a required location for the quest The Door high value keys high value loot '),
        ('Stair landing key', 0, 'streets No loot, but the ability to jump onto the stair landing that connects the second with the first floor, or straight down to the first floor if youre about that life'),
        ('Store managers key', 0, 'streets pc safe duffle Loose loot (Flammable materials, Household materials)'),
        ('Supply department directors office key', 0, 'streets locekd safe drawer Loose loot (Provisions, Flammable materials)'),
        ('Tarbank cash register department key', 0, 'streets The cash register booths bank safe'),
        ('TerraGroup meeting room key', 0, 'streets 2 intel spawns 1 drawer This is a possible location for the quest Beyond the Red Meat - Part 2'),
        ('TerraGroup security armory key', 0, 'streets weapon spawns pcs weapon crates'),
        ('X-ray room key', 0, 'streets 1 drawer med supplies'),
        ('Zmeisky 3 apartment 8 key', 0, 'streets duffle Loose loot (Valuables) '),
        ('Zmeisky 5 apartment 20 key', 0, 'streets Loose loot (Energy elements, Electronics, Provisions) sports bag'),
        ('Keycard with a blue marking', 0, 'labs This is a location for the quest TerraGroup Employee Loose loot (Meds and Medical supplies) stims '),
        ('TerraGroup Labs access keycard', 0, 'labs entry to labs needed to turn in for several quests'),
        ('TerraGroup Labs arsenal storage room key', 0, 'labs Valuables weapon mods meds'),
        ('TerraGroup Labs keycard (Black)', 0, 'labs This is a required location for the quest Following the Bread Crumbs med case med itims stims many ledx spawns'),
        ('TerraGroup Labs keycard (Blue)', 0, 'labs meds medcase ledx spawns'),
        ('TerraGroup Labs keycard (Green)', 0, 'labs med itesm black keycard ledx intel weapon box mods ammo mp5'),
        ('TerraGroup Labs keycard (Red)', 0, 'Its pretty bad, just discard it'),
        ('TerraGroup Labs keycard (Violet)', 0, 'labs Possible Military COFDM Wireless Signal Transmitter and UHF RFID Reader on the server rack weapon mods money, Multiple Valuables on the shelf next to the door'),
        ('TerraGroup Labs keycard (Yellow)', 0, 'labs Valuables, Electronics and Medical supplies on the chairs one pc'),
        ('TerraGroup Labs managers office room key', 0, 'labs This is a possible location for the quest Following the Bread Crumbs valuables intell folder'),
        ('TerraGroup Labs weapon testing area key', 0, 'labs This is a required location for the quest Following the Bread Crumbs weapon realted loot nothing crazy'),
        ('RB-AK key', 0, 'reserve virtex aesa tetriz two pcs Loose tech loot'),
        ('RB-AM key', 0, 'reserve intel folder Loose loot Building Materials, Tools, and Weapon mods'),
        ('RB-AO key', 0, 'reserve weapon rack Loose loot (Weapon mods)'),
        ('RB-BK marked key', 0, 'reserve Loose loot (multiple very rare Valuables, Weapons, Containers, Currency, Keycards)'),
        ('RB-GN key', 0, 'reserve Possible spawn of FP-100 filter Possible spawn of 6-STEN-140-M military battery '),
        ('RB-KORL key', 0, 'reserve 2 drawers intell spawn'),
        ('RB-KPRL key', 0, 'reserve intell spawn safe weapon cabinet'),
        ('RB-KSM key', 0, 'reserve This is a mandatory quest location for the quest Disease History Loose loot (Medical supplies)'),
        ('RB-MP11 key', 0, 'reserve intel one jacket'),
        ('RB-MP12 key', 0, 'reserve intel One 6-STEN-140-M military battery spawn loose loot'),
        ('RB-MP13 key', 0, 'reserve Possible spawn for 6-STEN-140-M military battery intel spawn'),
        ('RB-MP21 key', 0, 'reserve weapon mods 6-STEN-140-M military battery spawn (On the table to the right of the door.) intel spawn loose loot'),
        ('RB-MP22 key', 0, 'reserve Possible 6-STEN-140-M military battery loose loot tools and weapon items'),
        ('RB-OB key', 0, 'reserve intel spawn Required for the quest Inventory Check from Ragman Multiple valuable loot spawns on the desk'),
        ('RB-OP key', 0, 'reserve intel spawn Valuables spawn on shelf'),
        ('RB-ORB1 key', 0, 'reserve Required for the quest Inventory Check from Ragman intel spawn loose loot weapon loot'),
        ('RB-ORB2 key', 0, 'reserve Required for the quest Inventory Check from Ragman loose loot weapon loot'),
        ('RB-ORB3 key', 0, 'reserve Required for the quest Inventory Check from Ragman loose loot weapon loot'),
        ('RB-PKPM marked key', 0, 'reserve 3 drawers Loose loot (multiple very rare Valuables, Weapons, Containers, Currency, Keycards)'),
        ('RB-PSP1 key', 0, 'reserve 4 food crates one med crate one tech crate one toolboox Loose loot (Food, Drinks, Fuel)'),
        ('RB-PSP2 key', 0, 'reserve one med crate two ration crates two tech crates'),
        ('RB-PSV1 key', 0, 'reserve two med crates one ration one tech crate'),
        ('RB-PSV2 key', 0, 'reserve three med crates one tech crate'),
        ('RB-RH key', 0, 'reserve weapon rack weapon spawn 2 drawers'),
        ('RB-RLSA key', 0, 'reserve Loose loot (Weapon mods, Ammunition) one intel loose military tech items'),
        ('RB-RS key', 0, 'reserve Loose tech loot toolboxes'),
        ('RB-SMP key', 0, 'reserve This is a mandatory quest location for the quest Disease History. Loose loot (Medical supplies, Medical items, Stimulants) '),
        ('RB-ST key', 0, 'reserve Quest Surplus Goods Quest Revision - Reserve Quest Snatchtank battery ofz aesa military cable Loose loot (Ammunition, Weapon mods and Electronics) '),
        ('RB-TB key', 0, 'reserve weapon racks Loose loot (Weapon mods, Ammunition)'),
        ('RB-VO marked key', 0, 'reserve Loose loot (multiple very rare Valuables, Weapons, Containers, Currency, Keycards)'),
        ('Conference room key', 0, ' lighthouse locked safe  pc Loose loot (Ammo packs, Electronics, Provisions, Meds, Medical supplies)'),
        ('Convenience store storage room key', 0, 'lighthouse Loose loot (Meds, Medical supplies, Valuables, Provisions) medcase '),
        ('Hillside house key', 0, 'lighthouse Loose loot (Provisions, Valuables) Military Electronics spawn in the sink (Phased array element, Virtex'),
        ('Leons hideout key', 0, 'lighthouse arena key'),
        ('Merin car trunk key', 0, 'lighthouse Valuables electronics stims'),
        ('Operating room key', 0, 'lighthouse This is a required location for the quest Broadcast - Part 1  Electronics Possible BTC spawn on the table, left of room from entrance '),
        ('Police truck cabin key', 0, 'lighthouse Intell folder spawn in front of the seat'),
        ('Radar station commandant room key', 0, 'lighthouse  Used in the Quest Top Secret Loose loot (Tools, Weapon mods, valuables) jackets weapon  box pc '),
        ('Rogue USEC barrack key', 0, 'lighthouse This is a possible location for the quest Getting Acquainted Physical Bitcoin spawn on the chair Loose weapon mods weapon crates '),
        ('Rogue USEC stash key', 0, 'lighthouse Weapon mods Loose loot weapon boxes'),
        ('Rogue USEC workshop key', 0, 'lighthouse tank battery under the table 2 toolboxes'),
        ('Shared bedroom marked key', 0, 'lighthouse Loose loot (multiple very rare Valuables, Weapons, Containers, Currency, Keycards) sports bag jackets '),
        ('USEC cottage first safe key', 0, 'lighthouse virtex vpx cofdm Silicon Optoelectronic Integrated Circuits textbook '),
        ('USEC cottage room key', 0, 'lighthouse for Loose loot (Currency)'),
        ('USEC cottage second safe key', 0, 'lighthouse Loose loot (Currency) virtex vpx cofdm Silicon Optoelectronic Integrated Circuits textbook'),
        ('Water treatment plant storage room key', 0, 'lighthouse This is a possible location for the quest Getting Acquainted tech supply crate loose loot'),
        ('TerraGroup science office key', 0, 'ground zero Used in the Quest Saving the Mole 3 pcs 3 drawers'),
        ('Underground parking utility room key', 0, 'ground zero daed scav ammo box grenade box weapon box'),
        ('Unity Credit Bank cash register key', 0, 'ground zero 1 safe 1 drawer'),
        ('Folding car key', 0, 'no where for key4'),
        ('Missam forklift key', 0, 'no where 1 needs to be found in raid for the quest Collector'),
        ('Primorsky Ave apartment key', 0, 'trades only'),
        ('RB-PP key', 0, 'trades only'),
        ('Store safe key', 0, 'trades only'),
        ('VAZ car key', 0, 'trades only'),
        ('Weapon safe key', 0, 'trades only'),




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
searchButton.grid(row=1, column=19, padx=10)
showAllButton = Button(root, text="Show All owned Keys", command=showAllKeys)
showAllButton.grid(row=2, column=19, padx=10)

# Mainloop
root.mainloop()