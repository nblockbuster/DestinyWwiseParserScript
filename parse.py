import json
import os
import sys
import time
import subprocess
import zipfile

from math import floor

#PUT YOUR OWN PATH HERE
#(it has to be a folder of .bnk files)

bnk_directory = ""
packages_path = "C:\\Steam SSD Games\\steamapps\\common\\Destiny 2\\packages"

def get_flipped_hex(h, length):
    if length % 2 != 0:
        print("Flipped hex length is not even.")
        return None
    
    return "".join(reversed([h[:length][i:i + 2] for i in range(0, length, 2)]))

def fill_hex_with_zeros(s, desired_length):
    return ("0"*desired_length + s)[-desired_length:]

def getPkgId(hash):
    pkgID = floor((int(get_flipped_hex(hash,8), 16) - 0x80800000) / 8192)
    return fill_hex_with_zeros("%04X" % pkgID, 4)

def getHashFromFile(file):
    pkg = file.replace(".bin", "").upper()
    firsthex_int = int(pkg[:4], 16)
    secondhex_int = int(pkg[5:], 16)
    one = firsthex_int*8192
    two = hex(one + secondhex_int + 2155872256)
    return get_flipped_hex(two[2:], 8).upper()
    

wd = os.getcwd()

if(not len(sys.argv) == 2):
    print("Usage: parse.py <path to .bnk file>")
    print("No file specified.")
    print("Please input a valid file format.")
    print("If you are using a file in the bnk directory, please either use the full path, or open this file in notepad and change the \"bnk_directory\" path.")
    print("Valid format examples: \"0129-1cfd\", \"0129-1cfd.bnk\", \"E:/bnks/0129-1cfd\", \"E:/bnks/0129-1cfd.bnk\"")
    exit(5)

if(sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1)):
    bnk_file = bnk_directory + "\\" + sys.argv[1]
elif (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1)):
    bnk_file = sys.argv[1]
elif(sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1)):
    bnk_file = bnk_directory + "\\" + sys.argv[1] + ".bnk"
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1)):
    bnk_file = sys.argv[1] + ".bnk"

if (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1) and sys.argv[1][-6:-4] != "80"):
    bnkname = sys.argv[1][-13:-4]
elif (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1) and sys.argv[1][-6:-4] != "80"):
    bnkname = sys.argv[1][-13:-4]
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1) and sys.argv[1][-2:] != "80"):
    bnkname = sys.argv[1][-9:]
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1) and sys.argv[1][-2:] != "80"):
    bnkname = sys.argv[1][-9:]
elif (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1) and sys.argv[1][-6:-4] == "80"):
    bnkname = sys.argv[1][-12:-4]
elif (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1) and sys.argv[1][-6:-4] == "80"):
    bnkname = sys.argv[1][-12:-4]
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1) and sys.argv[1][-2:] == "80"):
    bnkname = sys.argv[1][-8:]
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1) and sys.argv[1][-2:] == "80"):
    bnkname = sys.argv[1][-8:]

#make raw outputs folder
if not os.path.exists(wd + "\\raw_outputs"):
    os.makedirs(wd + "\\raw_outputs")
    os.makedirs(wd + "\\raw_outputs\\" + bnkname)

if not os.path.exists(wd + "\\outputs"):
    os.makedirs(wd + "\\outputs")
if(not os.path.exists(wd + "\\Resources\\wwiseparser\\WwiseParser.exe") or not os.path.exists(wd + "\\Resources\\Unpacker\\DestinyUnpackerCPP.exe")):
    os.makedirs(wd + "\\Resources")
    with zipfile.ZipFile(wd + "\\Resources.zip", 'r') as zip_ref:
        zip_ref.extractall(wd)

if(not os.path.isfile(bnk_file)):
    print("File not found, trying to call DestinyUnpacker...")
    #if (bnk_file[-4:] == ".bnk" and bnk_file[-6:-4] == "80"):
        #bnk_pkg = getPkgId(bnk_file[-12:-4])
        #print("1", bnk_pkg)
    #elif(bnk_file[-4:] == ".bnk" and bnk_file[-6:-4] != "80"):
        #bnk_pkg = bnk_file[-13:-9]
        #print("3", bnk_pkg)
    dunpacker = "Resources\\Unpacker\\DestinyUnpackerCPP.exe -p \"" + packages_path + "\" -o \"raw_outputs\\" + bnkname + "\" -s " + getHashFromFile(bnkname)
    print(dunpacker)
    subprocess.call(dunpacker, shell=True)
    bnk_file = wd + "\\raw_outputs\\" + bnkname + "\\" + bnkname + ".bnk"
    print("File found, continuing...")
    
print("Parsing " + bnk_file)
        
os.chdir(wd + "\\raw_outputs")
wparse = f"{wd}\\Resources\\wwiseparser\\WwiseParser.exe", bnk_file
#print(wparse)
subprocess.check_output(wparse, shell=True).decode()
os.chdir(wd)

#if(sys.argv[1][-4:] == ".bnk"):
#    bnkname = sys.argv[1][-9:-4]
#elif(sys.argv[1][-4:] != ".bnk"):
#    bnkname = sys.argv[1]
#elif

#print(bnkname)
print_list = []
MusicTrackIds = []
for hirc_file in os.listdir(wd + "\\raw_outputs\\" + bnkname):
    if hirc_file == "hirc.json":
        hirc_path = wd + "\\raw_outputs\\" + bnkname + "\\hirc.json"
        print("Parsing " + hirc_path)
        start_time = time.time()
        with open(hirc_path) as json_file:
            data = json.load(json_file)           
            for obj in data["Objects"]:
                if obj["Type"] == "MusicTrack":
                    MusicTrackIds.append(obj["Id"])
            if(len(MusicTrackIds) == 0):
                print("No music tracks found.")
                exit(8)
            MusicPlaylistContainerIds = []
            Tempos = {}
            objc = 0
            o = 0
            for obj in data["Objects"]:
                if obj["Type"] == "MusicSwitchContainer":
                    curtempo = obj["Tempo"]
                    if(curtempo == 120.0):
                        curtempo = "Default/120.0"
                    #print(f"MusicSwitchContainer #{o} (" + str(obj["Id"]) + ") | Tempo:", curtempo)
                    #print_list.append(f"MusicSwitchContainer #{o} (" + str(obj["Id"]) + ") | Tempo: " + str(curtempo) + "\n")
                    for child in obj["ChildIds"]:
                        for obj2 in data["Objects"]:
                            if obj2["Id"] == child and obj2["Type"] == "MusicPlaylistContainer":
                                MusicPlaylistContainerIds.append(child)
                        if(obj2["Id"] == child and obj2["Properties"]["ParentId"] == 0):
                            continue
                    o+=1
                objc+=1
                p = 0
            for playlist in MusicPlaylistContainerIds:
                for obj in data["Objects"]:
                    if obj["Id"] == playlist and obj["Type"] == "MusicSwitchContainer":
                        continue
                    if obj["Id"] == playlist and obj["Type"] == "MusicPlaylistContainer":
                        curtempo = obj["Tempo"]
                        if(curtempo == 120.0):
                            curtempo = "Default/120.0"
                        time_up = obj["TimeSignatureUpper"]
                        time_low = obj["TimeSignatureLower"]
                        timesig = ""
                        if(time_up == 4 and time_low == 4):
                            timesig = "Default (4/4)"
                        else:
                            timesig = "{time_up}/{time_low}".format(time_up=time_up, time_low=time_low)
                        new = "\n"
                        if(p==0):
                            new=""
                        if(obj["Properties"]["ParameterCount"] > 0 and obj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                            vol = obj["Properties"]["ParameterValues"][0]
                            print(f"{new}MusicPlaylistContainer #{p} (" + str(obj["Id"]) + ") | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(new=new, vol=vol, tempo=curtempo, timesig=timesig))
                            print_list.append(f"{new}MusicPlaylistContainer #{p} (" + str(obj["Id"]) + ") | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(new=new, vol=vol, tempo=curtempo, timesig=timesig) + "\n")
                        else:
                            print(f"{new}MusicPlaylistContainer #{p} (" + str(obj["Id"]) + ") | Tempo: {tempo} | Time Signature: {timesig}".format(new=new,tempo=curtempo, timesig=timesig))
                            print_list.append(f"{new}MusicPlaylistContainer #{p} (" + str(obj["Id"]) + ") | Tempo: {tempo} | Time Signature: {timesig}".format(new=new, tempo=curtempo, timesig=timesig) + "\n")
                        
                        if(obj["Tempo"] != 0):
                            Tempos[obj["Id"]] = obj["Tempo"]
                        list = obj["Playlist"]
                        l = 0
                        #if(list["Type"] == "SequenceContinuous"):
                        if(list["ChildCount"] != 0):
                            print("    {ttype} #{l}".format(ttype=list["Type"], l=l))
                            print("        {ttype} Loop Count: {loop}".format(ttype=list["Type"], loop=list["LoopCount"]))
                            print("        {ttype} Avoid Repeat Count: {repeat}".format(ttype=list["Type"], repeat=list["AvoidRepeatCount"]))
                            print_list.append("    {ttype} #{l}".format(ttype=list["Type"], l=l) + "\n")
                            print_list.append("        {ttype} Loop Count: ".format(ttype=list["Type"]) + str(list["LoopCount"]) + "\n")
                            print_list.append("        {ttype} Avoid Repeat Count: ".format(ttype=list["Type"]) + str(list["AvoidRepeatCount"]) + "\n")
                            i = 0
                            for child in list["Children"]:
                                g = 0
                                if(child["Type"] == "MusicSegment"):
                                    for segobj in data["Objects"]:
                                        if segobj["Id"] == child["SegmentId"] and segobj["Type"] == "MusicSegment":
                                            curtempo = segobj["Tempo"]
                                            if(curtempo == 120.0):
                                                curtempo = "Default"
                                            time_up = segobj["TimeSignatureUpper"]
                                            time_low = segobj["TimeSignatureLower"]
                                            timesig = ""
                                            if(time_up == 4 and time_low == 4):
                                                timesig = "Default (4/4)"
                                            else:
                                                timesig = "{time_up}/{time_low}".format(time_up=time_up, time_low=time_low)
                                            if(segobj["Properties"]["ParameterCount"] != 0 and segobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                vol =  segobj["Properties"]["ParameterValues"][0]
                                                print("            MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig))
                                                print_list.append("            MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig) + "\n")
                                            else:
                                                print("            MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig))
                                                print_list.append("            MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig) + "\n")
                                                
                                            for trchild in segobj["ChildIds"]:
                                                for trobj in data["Objects"]:
                                                    if trobj["Id"] == trchild and trobj["Type"] == "MusicTrack":
                                                        if(trobj["Properties"]["ParameterCount"] != 0 and trobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                            if(trobj["Sounds"]):                          
                                                                vol = trobj["Properties"]["ParameterValues"][0]
                                                                print("                MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol))
                                                                print_list.append("                MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol) + "\n")

                                                                mushash = get_flipped_hex(fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                print("                    Src GinsorID: ", mushash)
                                                                print_list.append("                    Src GinsorID: " + mushash + "\n")
                                                        elif(trobj["Properties"]["ParameterCount"] == 0):
                                                            mushash = get_flipped_hex(fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                            print("                Src GinsorID: ", mushash)
                                                            print_list.append("                Src GinsorID: " + mushash + "\n")
                                                        #elif(trobj["MusicCues"]):
                                                            #mushash = get_flipped_hex(fill_hex_with_zeros(f'{trobj["MusicCues"][0]["Id"]:x}', 8), 8).upper()
                                                            #print("                    Src GinsorID: ", mushash)
                                                            #print_list.append("                    Src GinsorID: " + mushash + "\n")
                                elif(child["Type"] == "RandomContinuous"):
                                    print("        RandomContinuous #{g}".format(g=g))
                                    print("            RandomContinuous Loop Count:", child["LoopCount"])
                                    print("            RandomContinuous Avoid Repeat Count:", child["AvoidRepeatCount"])
                                    print_list.append("        RandomContinuous #{g}".format(g=g) + "\n")
                                    print_list.append("            RandomContinuous Loop Count: " + str(child["LoopCount"]) + "\n")
                                    print_list.append("            RandomContinuous Avoid Repeat Count: " + str(child["AvoidRepeatCount"]) + "\n")
                                    i = 0
                                    for child in list["Children"]:
                                        if(child["Type"] == "MusicSegment"):
                                            for segobj in data["Objects"]:
                                                if segobj["Id"] == child["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                    curtempo = segobj["Tempo"]
                                                    if(curtempo == 120.0):
                                                        curtempo = "Default"
                                                    time_up = segobj["TimeSignatureUpper"]
                                                    time_low = segobj["TimeSignatureLower"]
                                                    timesig = ""
                                                    if(time_up == 4 and time_low == 4):
                                                        timesig = "Default (4/4)"
                                                    else:
                                                        timesig = "{time_up}/{time_low}".format(time_up=time_up, time_low=time_low)
                                                    if(segobj["Properties"]["ParameterCount"] != 0 and segobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                        vol =  segobj["Properties"]["ParameterValues"][0]
                                                        print("                MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig))
                                                        print_list.append("                MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig) + "\n")
                                                    else:
                                                        print("                MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig))
                                                        print_list.append("                MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig) + "\n")
                                                    for trchild in segobj["ChildIds"]:
                                                        for trobj in data["Objects"]:
                                                            if trobj["Id"] == trchild and trobj["Type"] == "MusicTrack":
                                                                if(trobj["Properties"]["ParameterCount"] != 0 and trobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                                    if(trobj["Sounds"]):                          
                                                                        vol = trobj["Properties"]["ParameterValues"][0]
                                                                        print("                    MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol))
                                                                        print_list.append("                    MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol) + "\n")

                                                                        mushash = get_flipped_hex(fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                        print("                        Src GinsorID: ", mushash)
                                                                        print_list.append("                        Src GinsorID: " + mushash + "\n")
                                                                elif(trobj["Properties"]["ParameterCount"] == 0):
                                                                    mushash = get_flipped_hex(fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                    print("                    Src GinsorID: ", mushash)
                                                                    print_list.append("                    Src GinsorID: " + mushash + "\n")
                                        i+=1
                                elif(child["Type"] == "SequenceContinuous"):
                                    print("            SequenceContinuous #{g}".format(g=g))
                                    print("                SequenceContinuous Loop Count:", child["LoopCount"])
                                    print("                SequenceContinuous Avoid Repeat Count:", child["AvoidRepeatCount"])
                                    print_list.append("            SequenceContinuous #{g}".format(g=g) + "\n")
                                    print_list.append("                SequenceContinuous Loop Count: " + str(child["LoopCount"]) + "\n")
                                    print_list.append("                SequenceContinuous Avoid Repeat Count: " + str(child["AvoidRepeatCount"]) + "\n")
                                    i = 0
                                    k = 0
                                    for childchild in child["Children"]:
                                        if(childchild["Type"] == "MusicSegment"):
                                            for segobj in data["Objects"]:
                                                if segobj["Id"] == childchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                    curtempo = segobj["Tempo"]
                                                    if(curtempo == 120.0):
                                                        curtempo = "Default"
                                                    time_up = segobj["TimeSignatureUpper"]
                                                    time_low = segobj["TimeSignatureLower"]
                                                    timesig = ""
                                                    if(time_up == 4 and time_low == 4):
                                                        timesig = "Default (4/4)"
                                                    else:
                                                        timesig = "{time_up}/{time_low}".format(time_up=time_up, time_low=time_low)
                                                    if(segobj["Properties"]["ParameterCount"] != 0 and segobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                        vol =  segobj["Properties"]["ParameterValues"][0]
                                                        print("                    MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig))
                                                        print_list.append("                    MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig) + "\n")
                                                    else:
                                                        print("                    MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig))
                                                        print_list.append("                    MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig) + "\n")
                                                    for trchild in segobj["ChildIds"]:
                                                        for trobj in data["Objects"]:
                                                            if trobj["Id"] == trchild and trobj["Type"] == "MusicTrack":
                                                                if(trobj["Properties"]["ParameterCount"] != 0 and trobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                                    if(trobj["Sounds"]):                          
                                                                        vol = trobj["Properties"]["ParameterValues"][0]
                                                                        print("                        MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol))
                                                                        print_list.append("                        MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol) + "\n")

                                                                        mushash = get_flipped_hex(fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                        print("                            Src GinsorID: ", mushash)
                                                                        print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                elif(trobj["Properties"]["ParameterCount"] == 0):
                                                                    mushash = get_flipped_hex(fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                    print("                        Src GinsorID: ", mushash)
                                                                    print_list.append("                        Src GinsorID: " + mushash + "\n")
                                        elif(childchild["Type"] == "RandomStep"):
                                            print("                RandomStep #{k}".format(k=k))
                                            print("                    RandomStep Loop Count:", childchild["LoopCount"])
                                            print("                    RandomStep Avoid Repeat Count:", childchild["AvoidRepeatCount"])
                                            print_list.append("                RandomStep #{k}".format(k=k) + "\n")
                                            print_list.append("                    RandomStep Loop Count: " + str(childchild["LoopCount"]) + "\n")
                                            print_list.append("                    RandomStep Avoid Repeat Count: " + str(childchild["AvoidRepeatCount"]) + "\n")
                                            for segchild in childchild["Children"]:
                                                for segobj in data["Objects"]:
                                                    if segobj["Id"] == segchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                        curtempo = segobj["Tempo"]
                                                        if(curtempo == 120.0):
                                                            curtempo = "Default"
                                                        time_up = segobj["TimeSignatureUpper"]
                                                        time_low = segobj["TimeSignatureLower"]
                                                        timesig = ""
                                                        if(time_up == 4 and time_low == 4):
                                                            timesig = "Default (4/4)"
                                                        else:
                                                            timesig = "{time_up}/{time_low}".format(time_up=time_up, time_low=time_low)
                                                        if(segobj["Properties"]["ParameterCount"] != 0 and segobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                            vol =  segobj["Properties"]["ParameterValues"][0]
                                                            print("                        MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig))
                                                            print_list.append("                        MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig) + "\n")
                                                        else:
                                                            print("                        MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig))
                                                            print_list.append("                        MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig) + "\n")
                                                        for trchild in segobj["ChildIds"]:
                                                            for trobj in data["Objects"]:
                                                                if trobj["Id"] == trchild and trobj["Type"] == "MusicTrack":
                                                                    if(trobj["Properties"]["ParameterCount"] != 0 and trobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                                        if(trobj["Sounds"]):                          
                                                                            vol = trobj["Properties"]["ParameterValues"][0]
                                                                            print("                            MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol))
                                                                            print_list.append("                            MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol) + "\n")

                                                                            mushash = get_flipped_hex(fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                            print("                                Src GinsorID: ", mushash)
                                                                            print_list.append("                                Src GinsorID: " + mushash + "\n")
                                                                    elif(trobj["Properties"]["ParameterCount"] == 0):
                                                                        mushash = get_flipped_hex(fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                        print("                            Src GinsorID: ", mushash)
                                                                        print_list.append("                            Src GinsorID: " + mushash + "\n")
                                        elif(childchild["Type"] == "SequenceStep"):
                                            print("                SequenceStep #{k}".format(k=k))
                                            print("                    SequenceStep Loop Count:", childchild["LoopCount"])
                                            print("                    SequenceStep Avoid Repeat Count:", childchild["AvoidRepeatCount"])
                                            print_list.append("                SequenceStep #{k}".format(k=k) + "\n")
                                            print_list.append("                    SequenceStep Loop Count: " + str(childchild["LoopCount"]) + "\n")
                                            print_list.append("                    SequenceStep Avoid Repeat Count: " + str(childchild["AvoidRepeatCount"]) + "\n")
                                            for segchild in childchild["Children"]:
                                                for segobj in data["Objects"]:
                                                    if segobj["Id"] == childchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                        curtempo = segobj["Tempo"]
                                                        if(curtempo == 120.0):
                                                            curtempo = "Default"
                                                        time_up = segobj["TimeSignatureUpper"]
                                                        time_low = segobj["TimeSignatureLower"]
                                                        timesig = ""
                                                        if(time_up == 4 and time_low == 4):
                                                            timesig = "Default (4/4)"
                                                        else:
                                                            timesig = "{time_up}/{time_low}".format(time_up=time_up, time_low=time_low)
                                                        if(segobj["Properties"]["ParameterCount"] != 0 and segobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                            vol =  segobj["Properties"]["ParameterValues"][0]
                                                            print("            MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig))
                                                            print_list.append("            MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig) + "\n")
                                                        else:
                                                            print("            MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig))
                                                            print_list.append("            MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig) + "\n")
                                                        for trchild in segobj["ChildIds"]:
                                                            for trobj in data["Objects"]:
                                                                if trobj["Id"] == trchild and trobj["Type"] == "MusicTrack":
                                                                    if(trobj["Properties"]["ParameterCount"] != 0 and trobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                                        if(trobj["Sounds"]):                          
                                                                            vol = trobj["Properties"]["ParameterValues"][0]
                                                                            print("                MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol))
                                                                            print_list.append("                MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol) + "\n")

                                                                            mushash = get_flipped_hex(fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                            print("                    Src GinsorID: ", mushash)
                                                                            print_list.append("                    Src GinsorID: " + mushash + "\n")
                                                                    elif(trobj["Properties"]["ParameterCount"] == 0):
                                                                        mushash = get_flipped_hex(fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                        print("                Src GinsorID: ", mushash)
                                                                        print_list.append("                Src GinsorID: " + mushash + "\n")
                                        i+=1
                                        k+=1
                                i+=1
                                g+=1
                        l+=1
                p+=1
    with open(f"outputs\\{bnkname}.txt", "w") as f:
        for line in print_list:
            f.write(line)
print(f"\nExported to outputs\\{bnkname}.txt")
print("Done!")