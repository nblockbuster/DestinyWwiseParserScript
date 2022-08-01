import json
import os
import sys
import time
import subprocess
import zipfile
import functions as gf

from pprint import pprint

MusicTrackIds = []

#bnk_directory is unneeded if you set packages, but it's here for convenience
#packages_path doesnt matter if you set bnk_directory and dont want wave files to be extracted too.

#PUT YOUR OWN PATHS HERE
#!!!!
bnk_directory = "E:\\DestinyMusic\\AllBnks"
#bnk_directory = "E:\\DestinyMusic\\D2LDBnks\\bnk"
#bnk_directory = ""
packages_path = "D:\\Shadowkeep\\packages"
#packages_path = "C:\\Steam SSD Games\\steamapps\\Common\\Destiny 2\\packages"
#packages_path = "D:\\D2Y1\\packages"
#packages_path = "D:\\D2_Backups\\LastBL\\packages"
#packages_path = "D:\\PS4_Packages"
#!!!!
#PUT YOUR OWN PATHS HERE
    
wavexport = False #dont touch
version = "" #dont touch either

wd = os.getcwd()

if(len(sys.argv) < 2):
    print("Usage: parse.py <path to .bnk file>")
    print("No file specified.")
    print("Please input a valid file format.")
    print("If you are using a file in the bnk directory, please either use the full path, or open this file in notepad and change the \"bnk_directory\" path.")
    print("Valid format examples: \"0129-1cfd\", \"0129-1cfd.bnk\", \"E:/bnks/0129-1cfd\", \"E:/bnks/0129-1cfd.bnk\"")
    exit(5)
    
if (len(sys.argv) == 3):
    if(sys.argv[2] == "wav" or sys.argv[2] == "wavexport"):
        wavexport = True
        #print("3wav")
    if(sys.argv[2] == "d1"):
        version = "d1"
        #print("3d1")
    if(sys.argv[2] == "prebl"):
        version = "prebl"
        #print("3prebl")
    #if(sys.argv[3] == "d1"):
        #version = "d1"
        #print("34d1")
    #if(sys.argv[3] == "prebl"):
        #version = "prebl"
        #print("34prebl")
elif (len(sys.argv) == 4):
    if(sys.argv[2] == "wav" or sys.argv[3] == "wavexport"):
        wavexport = True
        #print("42wav")
    if(sys.argv[2] == "d1"):
        version = "d1"
        #print("42d1")
    if(sys.argv[2] == "prebl"):
        version = "prebl"
        #print("42prebl")   
    if(sys.argv[3] == "wav" or sys.argv[3] == "wavexport"):
        wavexport = True
        #print("43wav")
    if(sys.argv[3] == "d1"):
        version = "d1"
        #print("43d1")
    if(sys.argv[3] == "prebl"):
        version = "prebl"
        #print("43prebl")

if(sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1)):
    bnk_file = bnk_directory + "\\" + sys.argv[1]
elif (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1)):
    bnk_file = sys.argv[1]
elif(sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1)):
    if (bnk_directory != ""):
        bnk_file = bnk_directory + "\\" + sys.argv[1] + ".bnk"
    else:
        bnk_file = sys.argv[1] + ".bnk"
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1)):
    bnk_file = sys.argv[1] + ".bnk"
if (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1) and (sys.argv[1][-6:-4] != "80" or sys.argv[1][-6:-4] != "81")):
    bnkname = sys.argv[1][-13:-4]
elif (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1) and (sys.argv[1][-6:-4] != "80" or sys.argv[1][-6:-4] != "81")):
    bnkname = sys.argv[1][-13:-4]
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1) and (sys.argv[1][-2:] != "80" or sys.argv[1][-2:] != "81")):
    bnkname = sys.argv[1][-9:]
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1) and (sys.argv[1][-2:] != "80" or sys.argv[1][-2:] != "81")):
    bnkname = sys.argv[1][-9:]
elif (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1) and (sys.argv[1][-6:-4] == "80" or sys.argv[1][-6:-4] == "81")):
    bnkname = sys.argv[1][-12:-4]
elif (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1) and (sys.argv[1][-6:-4] == "80" or sys.argv[1][-6:-4] == "81")):
    bnkname = sys.argv[1][-12:-4]
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1) and (sys.argv[1][-2:] == "80" or sys.argv[1][-2:] == "81")):
    bnkname = sys.argv[1][-8:]
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1) and (sys.argv[1][-2:] == "80" or sys.argv[1][-2:] == "81")):
    bnkname = sys.argv[1][-8:]


#go through all files in the bnk_directory folder, and make the name of the file (without the extension!) 'bnkname'
#for file in os.listdir(bnk_directory):
    #nomus = False
    #bnkname = file[-13:-4]
    #bnk_file = bnk_directory + "\\" + file
    #make raw outputs folder
if not os.path.exists(wd + "\\raw_outputs"):
    os.makedirs(wd + "\\raw_outputs")
    os.makedirs(wd + "\\raw_outputs\\" + bnkname)

if not os.path.exists(wd + "\\outputs"):
    os.makedirs(wd + "\\outputs")
if not os.path.exists(wd + "\\Resources\\wwiseparser\\WwiseParser.exe") or not os.path.exists(wd + "\\Resources\\Unpacker\\DestinyUnpackerCPP.exe"):
    os.makedirs(wd + "\\Resources")
    with zipfile.ZipFile(wd + "\\Resources.zip", 'r') as zip_ref:
        zip_ref.extractall(wd)

print(bnk_file)

if not os.path.isfile(bnk_file):
    print("File not found, trying to call DestinyUnpacker...")
    if(packages_path == ""):
        print("Packages path not set. Please edit file and set the path to the packages folder.")
        exit(9)
    #if (bnk_file[-4:] == ".bnk" and bnk_file[-6:-4] == "80"):
        #bnk_pkg = getPkgId(bnk_file[-12:-4])
        #print("1", bnk_pkg)
    #elif(bnk_file[-4:] == ".bnk" and bnk_file[-6:-4] != "80"):
        #bnk_pkg = bnk_file[-13:-9]
        #print("3", bnk_pkg)
    #print(bnkname)
    dunpacker = "Resources\\Unpacker\\DestinyUnpackerCPP.exe -p \"" + packages_path + "\" -o \"raw_outputs\\" + bnkname + "\" -s " + gf.getHashFromFile(bnkname)
    #print(version)
    if version != "":
        dunpacker += " -v " + version
    print(dunpacker)
    subprocess.call(dunpacker, shell=True)
    bnk_file = wd + "\\raw_outputs\\" + bnkname + "\\" + bnkname + ".bnk"
    #print(bnk_file)
    print(bnk_file + " created, continuing...")
    
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
GinsorIds = []
fromstate = {}
ScriptedSegIds = []
UnscriptedSegIds = []
PrintList2 = []

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
                nomus = True
                continue
            MusicPlaylistContainerIds = []
            Tempos = {}
            objc = 0
            o = 0
            for obj in data["Objects"]:
                if obj["Type"] == "MusicSwitchContainer":
                    if obj["Properties"]["ParentId"] == 0:
                        continue
                    curtempo = obj["Tempo"]
                    if(curtempo == 120.0):
                        curtempo = "Default/120.0"
                    #if(obj["Properties"]["ParentId"] == 0 and obj["PathSectionLength"] != 0):
                    #if(obj["PathSectionLength"] != 0 and obj["Paths"] != [] and fromstate == {}):
                        #for stobj in obj["Paths"]["Children"]:
                            #state = stobj["FromStateOrSwitchId"]
                            #audid = stobj["AudioId"]
                            #fromstate[audid] = state
                            #print(str(audid) + ": " + str(state))
                            
                    print(f"MusicSwitchContainer #{o} (" + str(obj["Id"]) + ") | Tempo:", curtempo, "\n")
                    print_list.append(f"MusicSwitchContainer #{o} (" + str(obj["Id"]) + ") | Tempo: " + str(curtempo) + "\n\n")
                    p = 0
                    for child in obj["ChildIds"]:
                        for obj2 in data["Objects"]:
                            if obj2["Id"] == child and obj2["Type"] == "MusicPlaylistContainer":
                                MusicPlaylistContainerIds.append(child)
                                
                                #if obj["Id"] == playlist and obj["Type"] == "MusicSwitchContainer":
                                #continue
                            #if obj["Id"] == playlist and obj["Type"] == "MusicPlaylistContainer":
                    pq = 0
                    for plid in MusicPlaylistContainerIds:
                        for obj2 in data["Objects"]:
                            if obj2["Id"] == plid and obj2["Type"] == "MusicPlaylistContainer":
                                curtempo = obj2["Tempo"]
                                if(curtempo == 120.0):
                                    curtempo = "Default/120.0"
                                time_up = obj2["TimeSignatureUpper"]
                                time_low = obj2["TimeSignatureLower"]
                                timesig = ""
                                new = "\n"
                                if(time_up == 4 and time_low == 4):
                                    timesig = "Default (4/4)"
                                else:
                                    timesig = "{time_up}/{time_low}".format(time_up=time_up, time_low=time_low)
                                new = "\n"
                                if(p==0):
                                    new=""
                                id = obj2["Id"]                            
                                if(obj2["Properties"]["ParameterCount"] > 0 and obj2["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                    vol = obj2["Properties"]["ParameterValues"][0]
                                    thestr = f"{new}MusicPlaylistContainer #{p}[{pq}] ({id}) | VoiceVolume: {vol} | Tempo: {curtempo} | Time Signature: {timesig}"
                                    #print(fromstate[id])
                                    #if(fromstate[id] != 0):
                                        #thestr += " | FromState: " + str(fromstate[id])
                                    print(thestr)
                                    print_list.append(thestr + "\n")
                                else:
                                    thestr = f"{new}MusicPlaylistContainer #{p}[{pq}] ({id}) | Tempo: {curtempo} | Time Signature: {timesig}"
                                    #if(fromstate[id] != 0):
                                        #thestr += " | FromState: " + str(fromstate[id])
                                    print(thestr)
                                    print_list.append(thestr + "\n")
                                list = obj2["Playlist"]
                                l = 0
                                #if(list["Type"] == "SequenceContinuous"):
                                if(list["ChildCount"] != 0):
                                    print("    {ttype} #{l}".format(ttype=list["Type"], l=l))
                                    print_list.append("    {ttype} #{l}".format(ttype=list["Type"], l=l) + "\n")
                                    i = 0
                                    g = 0
                                    for child in list["Children"]:
                                        if(child["Type"] == "MusicSegment"):
                                            for segobj in data["Objects"]:
                                                if segobj["Id"] == child["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                    ScriptedSegIds.append(child["SegmentId"])
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
                                                                    if(trobj["SoundCount"] != 0):                          
                                                                        vol = trobj["Properties"]["ParameterValues"][0]
                                                                        print("                MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol))
                                                                        print_list.append("                MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol) + "\n")
                                                                        
                                                                        mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                        print("                    Src GinsorID: ", mushash)
                                                                        print_list.append("                    Src GinsorID: " + mushash + "\n")
                                                                        GinsorIds.append(mushash)
                                                                elif(trobj["SoundCount"] != 0):
                                                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                    print("                Src GinsorID: ", mushash)
                                                                    print_list.append("                Src GinsorID: " + mushash + "\n")
                                                                    GinsorIds.append(mushash)
                                                                elif(trobj["SoundCount"] == 0):
                                                                    print_list.pop()
                                                                #elif(trobj["MusicCues"]):
                                                                    #mushash = get_flipped_hex(fill_hex_with_zeros(f'{trobj["MusicCues"][0]["Id"]:x}', 8), 8).upper()
                                                                    #print("                    Src GinsorID: ", mushash)
                                                                    #print_list.append("                    Src GinsorID: " + mushash + "\n")
                                        elif(child["Type"] == "RandomContinuous"):
                                            print("        RandomContinuous #{g}".format(g=g))
                                            print_list.append("        RandomContinuous #{g}".format(g=g) + "\n")
                                            i = 0
                                            for child2 in child["Children"]:
                                                if(child2["Type"] == "MusicSegment"):
                                                    for segobj in data["Objects"]:
                                                        if segobj["Id"] == child2["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                            ScriptedSegIds.append(child2["SegmentId"])
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

                                                                                mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                print("                        Src GinsorID: ", mushash)
                                                                                print_list.append("                        Src GinsorID: " + mushash + "\n")
                                                                                GinsorIds.append(mushash)
                                                                        elif(trobj["SoundCount"] != 0):
                                                                            mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                            print("                    Src GinsorID: ", mushash)
                                                                            print_list.append("                    Src GinsorID: " + mushash + "\n")
                                                                            GinsorIds.append(mushash)
                                                                        elif(trobj["SoundCount"] == 0):
                                                                            print_list.pop()
                                                elif(child2["Type"] == "SequenceContinuous"):
                                                    print("                SequenceContinuous #{g}".format(g=g))
                                                    print_list.append("                SequenceContinuous #{g}".format(g=g) + "\n")
                                                    i = 0
                                                    k = 0
                                                    for childchild in child2["Children"]:
                                                        if(childchild["Type"] == "MusicSegment"):
                                                            for segobj in data["Objects"]:
                                                                if segobj["Id"] == childchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                                    ScriptedSegIds.append(childchild["SegmentId"])
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

                                                                                        mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                        print("                                Src GinsorID: ", mushash)
                                                                                        print_list.append("                                Src GinsorID: " + mushash + "\n")
                                                                                        GinsorIds.append(mushash)
                                                                                elif(trobj["SoundCount"] != 0):
                                                                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                    print("                            Src GinsorID: ", mushash)
                                                                                    print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                                    GinsorIds.append(mushash)
                                                                                elif(trobj["SoundCount"] == 0):
                                                                                    print_list.pop()
                                                        elif(childchild["Type"] == "RandomStep"):
                                                            print("                RandomStep #{k}".format(k=k))
                                                            print_list.append("                RandomStep #{k}".format(k=k) + "\n")
                                                            for segchild in childchild["Children"]:
                                                                for segobj in data["Objects"]:
                                                                    if segobj["Id"] == segchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                                        ScriptedSegIds.append(segchild["SegmentId"])
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

                                                                                            mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                            print("                                Src GinsorID: ", mushash)
                                                                                            print_list.append("                                Src GinsorID: " + mushash + "\n")
                                                                                            GinsorIds.append(mushash)
                                                                                    elif(trobj["SoundCount"] != 0):
                                                                                        mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                        print("                            Src GinsorID: ", mushash)
                                                                                        print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                                        GinsorIds.append(mushash)
                                                                                    elif(trobj["SoundCount"] == 0):
                                                                                        print_list.pop()
                                                        elif(childchild["Type"] == "SequenceStep"):
                                                            print("                SequenceStep #{k}".format(k=k))
                                                            print_list.append("                SequenceStep #{k}".format(k=k) + "\n")
                                                            for segchild in childchild["Children"]:
                                                                for segobj in data["Objects"]:
                                                                    if segobj["Id"] == childchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                                        ScriptedSegIds.append(childchild["SegmentId"])
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

                                                                                            mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                            print("                    Src GinsorID: ", mushash)
                                                                                            print_list.append("                    Src GinsorID: " + mushash + "\n")
                                                                                            GinsorIds.append(mushash)
                                                                                    elif(trobj["SoundCount"] != 0):
                                                                                        mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                        print("                Src GinsorID: ", mushash)
                                                                                        print_list.append("                Src GinsorID: " + mushash + "\n")
                                                                                        GinsorIds.append(mushash)
                                                                                    elif(trobj["SoundCount"] == 0):
                                                                                        print_list.pop()
                                                        i+=1
                                                i+=1
                                        elif(child["Type"] == "SequenceContinuous"):
                                            print("            SequenceContinuous #{g}".format(g=g))
                                            print_list.append("            SequenceContinuous #{g}".format(g=g) + "\n")
                                            i = 0
                                            k = 0
                                            for childchild in child["Children"]:
                                                if(childchild["Type"] == "MusicSegment"):
                                                    for segobj in data["Objects"]:
                                                        if segobj["Id"] == childchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                            ScriptedSegIds.append(childchild["SegmentId"])
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

                                                                                mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                print("                            Src GinsorID: ", mushash)
                                                                                print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                                GinsorIds.append(mushash)
                                                                        elif(trobj["SoundCount"] != 0):
                                                                            mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                            print("                        Src GinsorID: ", mushash)
                                                                            print_list.append("                        Src GinsorID: " + mushash + "\n")
                                                                            GinsorIds.append(mushash)
                                                                        elif(trobj["SoundCount"] == 0):
                                                                            print_list.pop()
                                                elif(childchild["Type"] == "RandomStep"):
                                                    print("                RandomStep #{k}".format(k=k))
                                                    print_list.append("                RandomStep #{k}".format(k=k) + "\n")
                                                    for segchild in childchild["Children"]:
                                                        for segobj in data["Objects"]:
                                                            if segobj["Id"] == segchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                                ScriptedSegIds.append(segchild["SegmentId"])
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

                                                                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                    print("                            Src GinsorID: ", mushash)
                                                                                    print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                                    GinsorIds.append(mushash)
                                                                            elif(trobj["SoundCount"] != 0):
                                                                                mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                print("                        Src GinsorID: ", mushash)
                                                                                print_list.append("                        Src GinsorID: " + mushash + "\n")
                                                                                GinsorIds.append(mushash)
                                                                            elif(trobj["SoundCount"] == 0):
                                                                                print_list.pop()
                                                elif(childchild["Type"] == "SequenceStep"):
                                                    print("                SequenceStep #{k}".format(k=k))
                                                    print_list.append("                SequenceStep #{k}".format(k=k) + "\n")
                                                    for segchild in childchild["Children"]:
                                                        if segchild["Type"] == "MusicSegment":
                                                            for segobj in data["Objects"]:
                                                                if segobj["Id"] == segchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                                    ScriptedSegIds.append(segchild["SegmentId"])
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

                                                                                        mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                        print("                            Src GinsorID: ", mushash)
                                                                                        print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                                        GinsorIds.append(mushash)
                                                                                elif(trobj["SoundCount"] != 0):
                                                                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                    print("                    Src GinsorID: ", mushash)
                                                                                    print_list.append("                    Src GinsorID: " + mushash + "\n")
                                                                                    GinsorIds.append(mushash)
                                                                                elif(trobj["SoundCount"] == 0):
                                                                                    print_list.pop()
                                                        elif(segchild["Type"] == "SequenceContinuous"):
                                                            print("                SequenceContinuous #{g}".format(g=g))
                                                            print_list.append("                SequenceContinuous #{g}".format(g=g) + "\n")
                                                            for childchild1 in segchild["Children"]:
                                                                if(childchild1["Type"] == "MusicSegment"):
                                                                    for segobj in data["Objects"]:
                                                                        if segobj["Id"] == childchild1["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                                            ScriptedSegIds.append(childchild1["SegmentId"])
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

                                                                                                mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                                print("                                Src GinsorID: ", mushash)
                                                                                                print_list.append("                                Src GinsorID: " + mushash + "\n")
                                                                                                GinsorIds.append(mushash)
                                                                                        elif(trobj["SoundCount"] != 0):
                                                                                            mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                            print("                            Src GinsorID: ", mushash)
                                                                                            print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                                            GinsorIds.append(mushash)
                                                                                        elif(trobj["SoundCount"] == 0):
                                                                                            print_list.pop()
                                                                elif(childchild1["Type"] == "RandomStep"):
                                                                    print("                RandomStep #{k}".format(k=k))
                                                                    print_list.append("                RandomStep #{k}".format(k=k) + "\n")
                                                                    for segchild in childchild1["Children"]:
                                                                        for segobj in data["Objects"]:
                                                                            if segobj["Id"] == segchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                                                ScriptedSegIds.append(segchild["SegmentId"])
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

                                                                                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                                    print("                                Src GinsorID: ", mushash)
                                                                                                    print_list.append("                                Src GinsorID: " + mushash + "\n")
                                                                                                    GinsorIds.append(mushash)
                                                                                            elif(trobj["SoundCount"] != 0):
                                                                                                mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                                print("                            Src GinsorID: ", mushash)
                                                                                                print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                                                GinsorIds.append(mushash)
                                                                                            elif(trobj["SoundCount"] == 0):
                                                                                                print_list.pop()
                                                                    i+=1
                                                                    k+=1
                                                                elif(childchild1["Type"] == "SequenceStep"):
                                                                    print("                SequenceStep #{k}".format(k=k))
                                                                    print_list.append("                SequenceStep #{k}".format(k=k) + "\n")
                                                                    for segchild in childchild1["Children"]:
                                                                        for segobj in data["Objects"]:
                                                                            if segobj["Id"] == segchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                                                ScriptedSegIds.append(segchild["SegmentId"])
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

                                                                                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                                    print("                    Src GinsorID: ", mushash)
                                                                                                    print_list.append("                    Src GinsorID: " + mushash + "\n")
                                                                                                    GinsorIds.append(mushash)
                                                                                            elif(trobj["SoundCount"] != 0):
                                                                                                mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                                print("                Src GinsorID: ", mushash)
                                                                                                print_list.append("                Src GinsorID: " + mushash + "\n")
                                                                                                GinsorIds.append(mushash)
                                                                                            elif(trobj["SoundCount"] == 0):
                                                                                                print_list.pop()
                                                        
                                                elif(childchild["Type"] == "RandomContinuous"):
                                                    print("        RandomContinuous #{g}".format(g=g))
                                                    print_list.append("        RandomContinuous #{g}".format(g=g) + "\n")
                                                    i = 0
                                                    for child2 in childchild["Children"]:
                                                        if(child2["Type"] == "MusicSegment"):
                                                            for segobj1 in data["Objects"]:
                                                                if segobj1["Id"] == child2["SegmentId"] and segobj1["Type"] == "MusicSegment":
                                                                    ScriptedSegIds.append(child2["SegmentId"])
                                                                    curtempo = segobj1["Tempo"]
                                                                    if(curtempo == 120.0):
                                                                        curtempo = "Default"
                                                                    time_up = segobj1["TimeSignatureUpper"]
                                                                    time_low = segobj1["TimeSignatureLower"]
                                                                    timesig = ""
                                                                    if(time_up == 4 and time_low == 4):
                                                                        timesig = "Default (4/4)"
                                                                    else:
                                                                        timesig = "{time_up}/{time_low}".format(time_up=time_up, time_low=time_low)
                                                                    if(segobj1["Properties"]["ParameterCount"] != 0 and segobj1["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                                        vol =  segobj1["Properties"]["ParameterValues"][0]
                                                                        print("                MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig))
                                                                        print_list.append("                MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig) + "\n")
                                                                    else:
                                                                        print("                MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig))
                                                                        print_list.append("                MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig) + "\n")
                                                                    for trchild in segobj1["ChildIds"]:
                                                                        for trobj in data["Objects"]:
                                                                            if trobj["Id"] == trchild and trobj["Type"] == "MusicTrack":
                                                                                if(trobj["Properties"]["ParameterCount"] != 0 and trobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                                                    if(trobj["Sounds"]):                          
                                                                                        vol = trobj["Properties"]["ParameterValues"][0]
                                                                                        print("                    MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol))
                                                                                        print_list.append("                    MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol) + "\n")

                                                                                        mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                        print("                        Src GinsorID: ", mushash)
                                                                                        print_list.append("                        Src GinsorID: " + mushash + "\n")
                                                                                        GinsorIds.append(mushash)
                                                                                elif(trobj["SoundCount"] != 0):
                                                                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                    print("                    Src GinsorID: ", mushash)
                                                                                    print_list.append("                    Src GinsorID: " + mushash + "\n")
                                                                                    GinsorIds.append(mushash)
                                                                                elif(trobj["SoundCount"] == 0):
                                                                                    print_list.pop()
                                                        elif(child2["Type"] == "SequenceContinuous"):
                                                            print("                SequenceContinuous #{g}".format(g=g))
                                                            print_list.append("                SequenceContinuous #{g}".format(g=g) + "\n")
                                                            for childchild in child2["Children"]:
                                                                if(childchild["Type"] == "MusicSegment"):
                                                                    for segobj in data["Objects"]:
                                                                        if segobj["Id"] == childchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                                            ScriptedSegIds.append(childchild["SegmentId"])
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

                                                                                                mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                                print("                                Src GinsorID: ", mushash)
                                                                                                print_list.append("                                Src GinsorID: " + mushash + "\n")
                                                                                                GinsorIds.append(mushash)
                                                                                        elif(trobj["SoundCount"] != 0):
                                                                                            mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                            print("                            Src GinsorID: ", mushash)
                                                                                            print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                                            GinsorIds.append(mushash)
                                                                                        elif(trobj["SoundCount"] == 0):
                                                                                            print_list.pop()
                                                                elif(childchild["Type"] == "RandomStep"):
                                                                    print("                RandomStep #{k}".format(k=k))
                                                                    print_list.append("                RandomStep #{k}".format(k=k) + "\n")
                                                                    for segchild in childchild["Children"]:
                                                                        for segobj in data["Objects"]:
                                                                            if segobj["Id"] == segchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                                                ScriptedSegIds.append(segchild["SegmentId"])
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

                                                                                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                                    print("                                Src GinsorID: ", mushash)
                                                                                                    print_list.append("                                Src GinsorID: " + mushash + "\n")
                                                                                                    GinsorIds.append(mushash)
                                                                                            elif(trobj["SoundCount"] != 0):
                                                                                                mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                                print("                            Src GinsorID: ", mushash)
                                                                                                print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                                                GinsorIds.append(mushash)
                                                                                            elif(trobj["SoundCount"] == 0):
                                                                                                print_list.pop()
                                                                    i+=1
                                                                    k+=1
                                                                elif(childchild["Type"] == "SequenceStep"):
                                                                    print("                SequenceStep #{k}".format(k=k))
                                                                    print_list.append("                SequenceStep #{k}".format(k=k) + "\n")
                                                                    for segchild in childchild["Children"]:
                                                                        for segobj in data["Objects"]:
                                                                            if segobj["Id"] == childchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                                                ScriptedSegIds.append(childchild["SegmentId"])
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

                                                                                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                                    print("                    Src GinsorID: ", mushash)
                                                                                                    print_list.append("                    Src GinsorID: " + mushash + "\n")
                                                                                                    GinsorIds.append(mushash)
                                                                                            elif(trobj["SoundCount"] != 0):
                                                                                                mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                                print("                Src GinsorID: ", mushash)
                                                                                                print_list.append("                Src GinsorID: " + mushash + "\n")
                                                                                                GinsorIds.append(mushash)
                                                                                            elif(trobj["SoundCount"] == 0):
                                                                                                print_list.pop()
                                                                    i+=1
                                                                    k+=1
                                                                i+=1
                                                                k+=1
                                                    i+=1
                                                    k+=1
                                                    
                                                i+=1
                                                k+=1
                                                g+=1
                                        elif child["Type"] == "RandomStep":
                                            print("            RandomStep #{g}".format(g=g))
                                            print_list.append("            RandomStep #{g}".format(g=g) + "\n")
                                            i = 0
                                            k = 0
                                            for segchild2 in child["Children"]:
                                                if segchild2["Type"] == "MusicSegment":
                                                    ScriptedSegIds.append(segchild2["SegmentId"])
                                                    curtempo = segchild2["Tempo"]
                                                    if(curtempo == 120.0):
                                                        curtempo = "Default"
                                                    time_up = segchild2["TimeSignatureUpper"]
                                                    time_low = segchild2["TimeSignatureLower"]
                                                    timesig = ""
                                                    if(time_up == 4 and time_low == 4):
                                                        timesig = "Default (4/4)"
                                                    else:
                                                        timesig = "{time_up}/{time_low}".format(time_up=time_up, time_low=time_low)
                                                    if(segchild2["Properties"]["ParameterCount"] != 0 and segchild2["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                        vol =  segchild2["Properties"]["ParameterValues"][0]
                                                        print("                    MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig))
                                                        print_list.append("                    MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig) + "\n")
                                                    else:
                                                        print("                    MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig))
                                                        print_list.append("                    MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig) + "\n")
                                                    for trchild in segchild2["ChildIds"]:
                                                        for trobj in data["Objects"]:
                                                            if trobj["Id"] == trchild and trobj["Type"] == "MusicTrack":
                                                                if(trobj["Properties"]["ParameterCount"] != 0 and trobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                                    if(trobj["Sounds"]):                          
                                                                        vol = trobj["Properties"]["ParameterValues"][0]
                                                                        print("                        MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol))
                                                                        print_list.append("                        MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol) + "\n")
                                                                        mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                        print("                            Src GinsorID: ", mushash)
                                                                        print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                        GinsorIds.append(mushash)
                                                                elif(trobj["SoundCount"] != 0):
                                                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                    print("                        Src GinsorID: ", mushash)
                                                                    print_list.append("                        Src GinsorID: " + mushash + "\n")
                                                                    GinsorIds.append(mushash)
                                                                elif(trobj["SoundCount"] == 0):
                                                                    print_list.pop()
                                                elif segchild2["Type"] == "RandomStep":
                                                    print("            RandomStep #{g}".format(g=g))
                                                    print_list.append("            RandomStep #{g}".format(g=g) + "\n")
                                                    i = 0
                                                    k = 0
                                                    for segchild21 in segchild2["Children"]:
                                                        for segobj2 in data["Objects"]:
                                                            if segobj2["Id"] == segchild21["SegmentId"] and segobj2["Type"] == "MusicSegment":
                                                                ScriptedSegIds.append(segchild21["SegmentId"])
                                                                curtempo = segobj2["Tempo"]
                                                                if(curtempo == 120.0):
                                                                    curtempo = "Default"
                                                                time_up = segobj2["TimeSignatureUpper"]
                                                                time_low = segobj2["TimeSignatureLower"]
                                                                timesig = ""
                                                                if(time_up == 4 and time_low == 4):
                                                                    timesig = "Default (4/4)"
                                                                else:
                                                                    timesig = "{time_up}/{time_low}".format(time_up=time_up, time_low=time_low)
                                                                if(segobj2["Properties"]["ParameterCount"] != 0 and segobj2["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                                    vol =  segobj2["Properties"]["ParameterValues"][0]
                                                                    print("                    MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig))
                                                                    print_list.append("                    MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig) + "\n")
                                                                else:
                                                                    print("                    MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig))
                                                                    print_list.append("                    MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig) + "\n")
                                                                for trchild in segobj2["ChildIds"]:
                                                                    for trobj in data["Objects"]:
                                                                        if trobj["Id"] == trchild and trobj["Type"] == "MusicTrack":
                                                                            if(trobj["Properties"]["ParameterCount"] != 0 and trobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                                                if(trobj["Sounds"]):                          
                                                                                    vol = trobj["Properties"]["ParameterValues"][0]
                                                                                    print("                        MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol))
                                                                                    print_list.append("                        MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol) + "\n")
                                                                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                    print("                            Src GinsorID: ", mushash)
                                                                                    print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                                    GinsorIds.append(mushash)
                                                                            elif(trobj["SoundCount"] != 0):
                                                                                mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                print("                        Src GinsorID: ", mushash)
                                                                                print_list.append("                        Src GinsorID: " + mushash + "\n")
                                                                                GinsorIds.append(mushash)
                                                                            elif(trobj["SoundCount"] == 0):
                                                                                print_list.pop()
                                                i+=1
                                                k+=1
                                        elif child["Type"] == "SequenceStep":
                                            print("            SequenceStep #{g}".format(g=g))
                                            print_list.append("            SequenceStep #{g}".format(g=g) + "\n")
                                            i = 0
                                            k = 0
                                            for segchild2 in child["Children"]:
                                                if segchild2["Type"] == "MusicSegment":
                                                    for segobj2 in data["Objects"]:
                                                        if segobj2["Id"] == segchild2["SegmentId"] and segobj2["Type"] == "MusicSegment":
                                                            ScriptedSegIds.append(segchild2["SegmentId"])
                                                            curtempo = segobj2["Tempo"]
                                                            if(curtempo == 120.0):
                                                                curtempo = "Default"
                                                            time_up = segobj2["TimeSignatureUpper"]
                                                            time_low = segobj2["TimeSignatureLower"]
                                                            timesig = ""
                                                            if(time_up == 4 and time_low == 4):
                                                                timesig = "Default (4/4)"
                                                            else:
                                                                timesig = "{time_up}/{time_low}".format(time_up=time_up, time_low=time_low)
                                                            if(segobj2["Properties"]["ParameterCount"] != 0 and segobj2["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                                vol =  segobj2["Properties"]["ParameterValues"][0]
                                                                print("                    MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig))
                                                                print_list.append("                    MusicSegment #{i} | VoiceVolume: {vol} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, vol=vol, tempo=curtempo, timesig=timesig) + "\n")
                                                            else:
                                                                print("                    MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig))
                                                                print_list.append("                    MusicSegment #{i} | Tempo: {tempo} | Time Signature: {timesig}".format(i=i, tempo=curtempo, timesig=timesig) + "\n")
                                                            for trchild in segobj2["ChildIds"]:
                                                                for trobj in data["Objects"]:
                                                                    if trobj["Id"] == trchild and trobj["Type"] == "MusicTrack":
                                                                        if(trobj["Properties"]["ParameterCount"] != 0 and trobj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                                                            if(trobj["Sounds"]):                          
                                                                                vol = trobj["Properties"]["ParameterValues"][0]
                                                                                print("                        MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol))
                                                                                print_list.append("                        MusicTrack #{g} | VoiceVolume: {vol}".format(g=g, vol=vol) + "\n")
                                                                                mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                print("                            Src GinsorID: ", mushash)
                                                                                print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                                GinsorIds.append(mushash)
                                                                        elif(trobj["SoundCount"] != 0):
                                                                            mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                            print("                        Src GinsorID: ", mushash)
                                                                            print_list.append("                        Src GinsorID: " + mushash + "\n")
                                                                            GinsorIds.append(mushash)
                                                                        elif(trobj["SoundCount"] == 0):
                                                                            print_list.pop()
                                                elif(segchild2["Type"] == "SequenceContinuous"):
                                                    print("                SequenceContinuous #{g}".format(g=g))
                                                    print_list.append("                SequenceContinuous #{g}".format(g=g) + "\n")
                                                    i = 0
                                                    k = 0
                                                    for childchild in segchild2["Children"]:
                                                        if(childchild["Type"] == "MusicSegment"):
                                                            for segobj in data["Objects"]:
                                                                if segobj["Id"] == childchild["SegmentId"] and segobj["Type"] == "MusicSegment":
                                                                    ScriptedSegIds.append(childchild["SegmentId"])
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

                                                                                        mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                        print("                            Src GinsorID: ", mushash)
                                                                                        print_list.append("                            Src GinsorID: " + mushash + "\n")
                                                                                        GinsorIds.append(mushash)
                                                                                elif(trobj["SoundCount"] != 0):
                                                                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                                    print("                        Src GinsorID: ", mushash)
                                                                                    print_list.append("                        Src GinsorID: " + mushash + "\n")
                                                                                    GinsorIds.append(mushash)
                                                                                elif(trobj["SoundCount"] == 0):
                                                                                    print_list.pop()
                                        i+=1
                                        g+=1
                                for balls in obj2["ChildIds"]:
                                    if balls in ScriptedSegIds:
                                        continue
                                    else:
                                        print(balls)
                                        UnscriptedSegIds.append(balls)
                                        for unscriptobj in data["Objects"]:
                                            if(unscriptobj["Id"] == balls and unscriptobj["Type"] == "MusicSegment"):
                                                for trchild in unscriptobj["ChildIds"]:
                                                    for trobj in data["Objects"]:
                                                        if trobj["Id"] == trchild and trobj["Type"] == "MusicTrack":
                                                            if(trobj["SoundCount"] != 0):
                                                                curtempo = unscriptobj["Tempo"]
                                                                if(curtempo == 120.0):
                                                                    curtempo = "Default"
                                                                time_up = unscriptobj["TimeSignatureUpper"]
                                                                time_low = unscriptobj["TimeSignatureLower"]
                                                                timesig = ""
                                                                if(time_up == 4 and time_low == 4):
                                                                    timesig = "Default (4/4)"
                                                                else:
                                                                    timesig = "{time_up}/{time_low}".format(time_up=time_up, time_low=time_low)
                                                                parid = unscriptobj["Properties"]["ParentId"]
                                                                print(f"Unscripted MusicSegment | Tempo: {curtempo} | Time Signature: {timesig} | Parent ID: {parid}")
                                                                PrintList2.append("Unscripted MusicSegment | Tempo: {tempo} | Time Signature: {timesig} | Parent ID: {parid}".format(tempo=curtempo, timesig=timesig, parid=parid))
                                                                mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{trobj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                                                print("    Src GinsorID: ", mushash)
                                                                PrintList2.append("    Src GinsorID: " + mushash + "\n")
                                                                GinsorIds.append(mushash)
                                                
                                l+=1
                                
                            pq += 1
                        p+=1
            o+=1
        objc+=1
#if nomus:
    #continue
    
bnk_output = f"outputs\\{bnkname}"
if not os.path.exists(bnk_output):
    os.mkdir(bnk_output)

with open(f"{bnk_output}\\{bnkname}_unused.txt", "w") as f1:
    for id2 in PrintList2:
        f1.write(f"{id2}\n")
               
with open(f"{bnk_output}\\{bnkname}.txt", "w") as f:
    for line in print_list:
        f.write(line)
print(f"\nExported to {bnk_output}\\{bnkname}.txt")

if(len(GinsorIds) != 0 and wavexport):
    uniqueGinsorIds = set(GinsorIds)
    for ginsorID in uniqueGinsorIds:
        unpacker_cmd = "Resources\\Unpacker\\DestinyUnpackerCPP.exe -p \"" + packages_path + "\" -o \"" + bnk_output + "\\wav\" -s " + ginsorID + " -h -w"
        if (version):
            unpacker_cmd += " -v " + version
        print(unpacker_cmd)
        subprocess.check_call(unpacker_cmd, shell=True)


print("Done!")