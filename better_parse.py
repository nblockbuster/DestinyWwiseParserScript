import json
import os
import sys
import subprocess
from types import NoneType
import zipfile
import functions as gf

#bnk_directory is unneeded if you set packages, but it's here for convenience
#packages_path doesnt matter if you set bnk_directory and dont want wave files to be extracted too.

#PUT YOUR OWN PATHS HERE
#!!!!


bnk_directory = "E:\\DestinyMusic\\AllBnks"
packages_path = "D:\\Shadowkeep\\packages"
#packages_path = "C:\\Steam SSD Games\\steamapps\\Common\\Destiny 2\\packages"
#packages_path = "D:\\D2Y1\\packages"
#packages_path = "D:\\D2_Backups\\LastBL\\packages"
#packages_path = "D:\\PS4_Packages"


#!!!!
#PUT YOUR OWN PATHS HERE
    
wavexport = False
version = ""

wd = os.getcwd()

if(len(sys.argv) < 2):
    print("Usage: parse.py <path to .bnk file>")
    print("No file specified.")
    print("Please input a valid file format.")
    print("If you are using a file in the bnk directory, please either use the full path, or open this file in notepad and change the \"bnk_directory\" path.")
    print("Valid format examples: \"0129-1cfd\", \"0129-1cfd.bnk\", \"E:/bnks/0129-1cfd\", \"E:/bnks/0129-1cfd.bnk\"")
    exit(5)
    
if (len(sys.argv) == 3):
    if (sys.argv[2] == "wav" or sys.argv[2] == "wavexport"):
        wavexport = True
    if (sys.argv[2] == "d1"):
        version = "d1"
    if (sys.argv[2] == "prebl"):
        version = "prebl"
elif (len(sys.argv) == 4):
    if (sys.argv[2] == "wav" or sys.argv[3] == "wavexport"):
        wavexport = True
    if (sys.argv[2] == "d1"):
        version = "d1"
    if (sys.argv[2] == "prebl"):
        version = "prebl"
    if (sys.argv[3] == "wav" or sys.argv[3] == "wavexport"):
        wavexport = True
    if (sys.argv[3] == "d1"):
        version = "d1"
    if (sys.argv[3] == "prebl"):
        version = "prebl"

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
    bnkname = sys.argv[1][-12:-4]
elif (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1) and (sys.argv[1][-6:-4] != "80" or sys.argv[1][-6:-4] != "81")):
    bnkname = sys.argv[1][-12:-4]
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1) and (sys.argv[1][-2:] != "80" or sys.argv[1][-2:] != "81")):
    bnkname = sys.argv[1][-9:]
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1) and (sys.argv[1][-2:] != "80" or sys.argv[1][-2:] != "81")):
    bnkname = sys.argv[1][-9:]
elif (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1) and (sys.argv[1][-6:-4] == "80" or sys.argv[1][-6:-4] == "81")):
    bnkname = sys.argv[1][-12:-4]
elif (sys.argv[1][-4:] == ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1) and (sys.argv[1][-6:-4] == "80" or sys.argv[1][-6:-4] == "81")):
    bnkname = sys.argv[1][-12:-4]
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") == -1 or sys.argv[1].find("/") == -1) and (sys.argv[1][-2:] == "80" or sys.argv[1][-2:] == "81")):
    bnkname = sys.argv[1][-9:]
elif (sys.argv[1][-4:] != ".bnk" and (sys.argv[1].find("\\") != -1 or sys.argv[1].find("/") != -1) and (sys.argv[1][-2:] == "80" or sys.argv[1][-2:] == "81")):
    bnkname = sys.argv[1][-9:]

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
    dunpacker = "Resources\\Unpacker\\DestinyUnpackerCPP.exe -p \"" + packages_path + "\" -o \"raw_outputs\\" + bnkname + "\" -s " + gf.getHashFromFile(bnkname)
    if version != "":
        dunpacker += " -v " + version
    print(dunpacker)
    subprocess.call(dunpacker, shell=True)
    bnk_file = wd + "\\raw_outputs\\" + bnkname + "\\" + bnkname + ".bnk"
    print(bnk_file + " created, continuing...")
    
print("Parsing " + bnk_file)
        
os.chdir(wd + "\\raw_outputs")
wparse = f"{wd}\\Resources\\wwiseparser\\WwiseParser.exe", bnk_file
subprocess.check_output(wparse, shell=True).decode()
os.chdir(wd)

data = NoneType

switch_name = ""

print_list = []
MusicTrackIds = []
GinsorIds = []
fromstate = {}
ScriptedSegIds = []
UnscriptedSegIds = []
PrintList2 = []
iterat = 1
CurrentPlaylistId = 0
    
def gen_list(list: any, l: any):
    if(list["ChildCount"] != 0):
        stri = "    {ttype} #{l}".format(ttype=list["Type"], l=l)
        print(stri)
        print_list.append(stri + "\n")
        b = 0
        for child in list["Children"]:
            recursive(child, 0, b)
            b+=1
    return

def recursive(child: any = NoneType, id = 0, segment_order = 0):
    global wd
    global iterat
    spaces = ' ' * iterat
    if (id != 0):
        for obj in data["Objects"]:
            if (obj["Id"] == id and obj["Type"] == "MusicSegment"):
                time_up = obj["TimeSignatureUpper"]
                time_low = obj["TimeSignatureLower"]
                timesig = ""
                
                if (time_up == 4 and time_low == 4):
                    timesig = "Default (4/4)"
                else:
                    timesig = f"{time_up}/{time_low}"
                    
                curtempo = obj["Tempo"]
                
                if (curtempo == 120.0):
                    curtempo = "Parent Tempo/120"
                    
                l = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{id:x}', 8), 8).upper()
                spc = ' ' * (iterat + 7)
                stri = "{spaces}{ttype} {l} | Tempo: {tempo} | Time Signature: {timesig}".format(spaces=spc, ttype=obj["Type"], l=l, tempo=curtempo, timesig=timesig)
                
                if (obj["Properties"]["ParameterCount"] != 0 and obj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                    vol =  obj["Properties"]["ParameterValues"][0]
                    
                    stri += " | Volume: {vol}".format(vol=vol)
                    
                print(stri)
                print_list.append(stri + "\n")
                if (obj["ChildCount"] != 0):
                    sid = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{id:x}', 8), 8).upper()
                    for child_id in obj["ChildIds"]:
                        for child_track_obj in data["Objects"]:
                            if (child_track_obj["Id"] == child_id and child_track_obj["Type"] == "MusicTrack"):
                                l = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{child_track_obj["Id"]:x}', 8), 8).upper()
                                spc2 = ' ' * (iterat + 11)
                                stri = "{spaces}{ttype} {l}".format(spaces=spc2, ttype=child_track_obj["Type"], l=l)
                                if (child_track_obj["Properties"]["ParameterCount"] != 0 and child_track_obj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                    vol = child_track_obj["Properties"]["ParameterValues"][0]
                                    stri += f" | VoiceVolume: {vol}"
                                print(stri)
                                print_list.append(stri + "\n")
                                if (child_track_obj["SoundCount"] != 0):
                                    mushash = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{child_track_obj["Sounds"][0]["AudioId"]:x}', 8), 8).upper()
                                    spc3 = ' ' * (iterat + 15)
                                    stri = "{spaces}Src GinsorID: {mushash}".format(spaces=spc3, mushash=mushash)
                                    
                                    print(stri)
                                    print_list.append(stri + "\n")
                                    GinsorIds.append(mushash)
                                    
                                elif (child_track_obj["SoundCount"] == 0):
                                    print_list.pop()                           
        return   
    
    if child.get("isGroup") != None:
        if (child["isGroup"] == True):
            stri = "{spaces}{ttype} {l}".format(spaces=spaces, ttype=child["Type"], l=child["UnknownId"].hex().upper())
            print(stri)
            print_list.append(stri + "\n")

    if (child["ChildCount"] != 0):
        recursive(child["Children"][0])

    if (child["Type"] == "MusicSegment"):
        recursive(NoneType, child["SegmentId"], segment_order)
        


for hirc_file in os.listdir(wd + "\\raw_outputs\\" + bnkname):
    if hirc_file == "hirc.json":
        hirc_path = wd + "\\raw_outputs\\" + bnkname + "\\hirc.json"
        print("Parsing " + hirc_path)
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
            o = 0
            for obj in data["Objects"]:
                if obj["Type"] == "MusicSwitchContainer":
                    if obj["Properties"]["ParentId"] == 0:
                        continue
                    curtempo = obj["Tempo"]
                    if(curtempo == 120.0):
                        curtempo = "Default/120.0"
                        print(f"MusicSwitchContainer #{o} (" + gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{obj["Id"]:x}', 8), 8).upper() + ") | Tempo:", curtempo, "\n")
                    print_list.append(f"MusicSwitchContainer #{o} (" + gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{obj["Id"]:x}', 8), 8).upper() + ") | Tempo: " + str(curtempo) + "\n")
                    
                    p = 0
                    for child in obj["ChildIds"]:
                        for obj2 in data["Objects"]:
                            if obj2["Id"] == child and obj2["Type"] == "MusicPlaylistContainer":
                                MusicPlaylistContainerIds.append(child)
                    pq = 0
                    l = 0
                    for plid in MusicPlaylistContainerIds:
                        for obj2 in data["Objects"]:
                            if obj2["Id"] == plid and obj2["Type"] == "MusicPlaylistContainer":
                                curtempo = obj2["Tempo"]
                                if(curtempo == 120.0):
                                    curtempo = "Default/120.0"
                                time_up = obj2["TimeSignatureUpper"]
                                time_low = obj2["TimeSignatureLower"]
                                timesig = ""
                                if(time_up == 4 and time_low == 4):
                                    timesig = "Default (4/4)"
                                else:
                                    timesig = f"{time_up}/{time_low}"
                                id = obj2["Id"]     
                                CurrentPlaylistId = gf.get_flipped_hex(gf.fill_hex_with_zeros(f'{id:x}', 8), 8).upper()
                                
                                thestr = f"MusicPlaylistContainer #{l}[{pq}] ({CurrentPlaylistId}) | Tempo: {curtempo} | Time Signature: {timesig}"
                                if (obj2["Properties"]["ParameterCount"] > 0 and obj2["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                    vol = obj2["Properties"]["ParameterValues"][0]
                                    thestr += f" | VoiceVolume: {vol}"
                                print("\n" + thestr)
                                print_list.append("\n" + thestr + "\n")
                                list = obj2["Playlist"]
      
                                gen_list(list, l)
                                iterat = 1
                                l+=1
                            pq+=1

bnk_output = f"outputs\\{bnkname}"
if not os.path.exists(bnk_output):
    os.mkdir(bnk_output)
               
with open(f"{bnk_output}\\{bnkname}.txt", "w") as f:
    for line in print_list:
        f.write(line)
print(f"\nExported to {bnk_output}\\{bnkname}.txt")

if (len(GinsorIds) != 0 and wavexport):
    uniqueGinsorIds = set(GinsorIds)
    for ginsorID in uniqueGinsorIds:
        unpacker_cmd = "Resources\\Unpacker\\DestinyUnpackerCPP.exe -p \"" + packages_path + "\" -o \"" + bnk_output + "\\wav\" -s " + ginsorID + " -h -w"
        if (version):
            unpacker_cmd += " -v " + version
        print(unpacker_cmd)
        subprocess.check_call(unpacker_cmd, shell=True)
        
print("Done!")