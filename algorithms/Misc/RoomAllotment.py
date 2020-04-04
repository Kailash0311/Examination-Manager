def start_room_allotment_verify_process(category, room_allotment_file,room_map, room_list):
    print("*** Verifying Room Allotment File ... ***")
    # print(path)
    room_duplicate_rows(room_allotment_file)
    check_clashes_left_right_full(room_allotment_file)
    check_diff_enrol_count_tot_students(room_allotment_file)
    verify_room_map_and_room_list(room_map, room_list)
def verify_room_map_and_room_list(room_map, room_list):
    f = open(room_map)
    header = False
    room_map_dict = dict()
    for line in f.readlines():
        if(header):
            header = False
            continue
        line = line.strip()
        row = line.split(",")
        count = row[1]
        room = row[0].split("-")[0] # For F102 and F105 (lower and upper) 
        if(room[0] == "D"): # D208 series are ignored. 
            continue
        if(room not in room_map_dict):
            room_map_dict[room] = 0
        for i in range(count):
            room_map_dict[room] += row[i+2]
    room_list_dict = dict() 
    header = False
    f = open(room_list)
    
    for line in f.readlines():
        if(header):
            header = True
            continue
        line = line.strip()
        row = line.strip(",")
        if(row[0] not in room_list_dict):
            room_list_dict[row[0]] = 0
        room_list_dict[row[0]] += row[1]
    for key in room_list_dict:
        if(room_list_dict[key] != room_map_dict[key]):
            print("** Mismatch in Room Map and Room List  of Room ",key ,"**")
            print("Seat count in Room List", room_list_dict[key])
            print("Seat count in Room Map", room_map_dict[key])
            print("\n \n")
        
        

def check_diff_enrol_count_tot_students(csv):
    enrol_dict = dict()
    stu_allot = dict()
    f = open(csv)
    header = True
    for line in f.readlines():
        if(header == True):
            header = False
            continue
        line = line.strip()
        row = line.split(",")
        enrol_dict[row[1]] = int(row[5])
        if(row[1] not in stu_allot.keys()):
            stu_allot[row[1]] = int(row[4])
        else:
            stu_allot[row[1]] = stu_allot[row[1]] + int(row[4])
    for key in enrol_dict.keys():
        if(enrol_dict[key] - stu_allot[key] != 0):
            print("Mismatch in students alloted and course strength for course ", key)
            print("Students alloted in the course ", stu_allot[key])
            print("Course strength ,", enrol_dict[key])
    

def room_duplicate_rows(csv):
    print("Checking for duplicate rows... \n")
    f = open(csv)
    rows = []
    dup = 0
    header = True # Room Allotment file generated has header
    for i, line in enumerate(f):
        if(header == True):
            header = False
            continue
        line = line.strip()
        if(line not in rows):
            rows.append(line)
        else:
            print("Duplicate Row Found at row " , i+1)
            print(line, "\n")
            dup = 1
    if(not(dup)):
        print("No duplicate rows found ...")
def room_discrep_enroll_tot_st(csv):
    print("Do something here 4 ...")
def check_clashes_left_right_full(csv):
    print("Checking for clashes (LEFT/RIGHT/FULL) ... \n")
    clashes = dict()
    f = open(csv)
    clash = 0
    for i, row in enumerate(f):
        row = row.strip()
        line = row.split(",")
        # print(line)
        room_time = line[0] + line[6]
        if(room_time not in clashes.keys()):
            clashes[room_time] = []
        if(line[7] == "FULL" and len(clashes[room_time]) > 0):
            print("** Clash **")
            print("Cannot add FULL to the room which is already alloted LEFT/RIGHT")
            print("Row number ", i+1)
            clash = 1
            continue
        elif(line[7] != "FULL"):
            str = "FULL"
            if(line[7] not in clashes[room_time]):
                if(str not in clashes[room_time]):
                    clashes[room_time].append(line[7])
                else:
                    print("** Clash ** ")
                    print("Cannot add LEFT/RIGHT to the room which is already alloted FULL")
                    print("Row number ", i+1)
                    clash = 1
            # print(clashes[room_time])
            elif(line[7] in clashes[room_time]):
                print("** Clash **")
                print("Cannot add Two LEFTs/RIGHTs")
                print("Row number ", i+1)
                clash = 1
        else:
            clashes[room_time].append("FULL")
    if(not(clash)):
        print("No clashes found ...")


