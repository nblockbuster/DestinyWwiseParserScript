import json
import os
import sys
import subprocess
from types import NoneType
import zipfile
import functions as gf

from waapi import WaapiClient, CannotConnectToWaapiException
from pprint import pprint

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

client = NoneType

try:
    client = WaapiClient()
    print("Connected to Waapi.")
except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")
    exit()
    
print(client.is_connected())
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

import_audio_args = {
    "importOperation": "useExisting",
    "default": {
        "importLanguage": "SFX"
    },
    "imports": []
}

    
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
                    curtempo = "Default/120"
                    
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
                                    arg = {
                                            "objectPath": f"\\Interactive Music Hierarchy\\Default Work Unit\\{switch_name}\\MusicPlaylistContainer ({CurrentPlaylistId})\\MusicSegment {segment_order} ({sid})\\{mushash}",
                                            "audioFile": f"{wd}\\outputs\\{bnkname}\\wav\\{mushash}.wav",
                                        }
                                    if (arg not in import_audio_args["imports"]):
                                        import_audio_args["imports"].append(arg)
                                    
                                elif (child_track_obj["SoundCount"] == 0):
                                    print_list.pop()                           
                    
                    object_create_args = {
                        "parent": f"\\Interactive Music Hierarchy\\Default Work Unit\\{switch_name}\\MusicPlaylistContainer ({CurrentPlaylistId})",
                        "type": "MusicSegment",
                        "name": f"MusicSegment {segment_order} ({sid})",
                        "children": [
                            
                        ]
                    }
                    
                    result = client.call("ak.wwise.core.object.create", object_create_args)
                    pprint(result)
                    if (obj["Properties"]["ParameterCount"] != 0 and obj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                        result = client.call("ak.wwise.core.object.setProperty",
                        {
                            "object":f"\\Interactive Music Hierarchy\\Default Work Unit\\{switch_name}\\MusicPlaylistContainer ({CurrentPlaylistId})\\MusicSegment {segment_order} ({sid})",
                            "property": "Volume",
                            "value": obj["Properties"]["ParameterValues"][0]
                        })
                        pprint(result)
                        
                    
                    cue_create_args = {
                        "parent": f"\\Interactive Music Hierarchy\\Default Work Unit\\{switch_name}\\MusicPlaylistContainer ({CurrentPlaylistId})\\MusicSegment {segment_order} ({sid})",
                        "name": "Entry Cue",
                        "type": "MusicCue",
                        "list": "Cues",
                        "@TimeMs": obj["MusicCues"][0]["Time"],
                        "@CueType": 0
                    }
                
                    result = client.call("ak.wwise.core.object.create", cue_create_args)
                    pprint(result)
                    
                    cue_create_args["@TimeMs"] = (obj["MusicCues"][1]["Time"] - obj["MusicCues"][0]["Time"])
                    cue_create_args["@CueType"] = 1
                    cue_create_args["name"] = "Exit Cue"
                    
                    result = client.call("ak.wwise.core.object.create", cue_create_args)
                    pprint(result)
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
                    swid = obj["Id"]
                    switch_name = f"{bnkname}_MusicSwitchContainer_{swid}"
                    
                    switch_create_args = {
                        "parent": f"\\Interactive Music Hierarchy\\Default Work Unit",
                        "name": f"{switch_name}",
                        "type": "MusicSwitchContainer"
                    }
                    result = client.call("ak.wwise.core.object.create", switch_create_args)
                    pprint(result)
                    
                    switch_edit = {
                        "object": f"\\Interactive Music Hierarchy\\Default Work Unit\\{switch_name}",
                        "property": "Tempo",
                        "value": obj["Tempo"]
                    }
                    
                    result = client.call("ak.wwise.core.object.setProperty", switch_edit)
                    pprint(result)
                    
                    if (obj["Properties"]["ParameterCount"] != 0 and obj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                        switch_edit["property"] = "Volume"
                        switch_edit["value"] = obj["Properties"]["ParameterValues"][0]
                        result = client.call("ak.wwise.core.object.setProperty", switch_edit)
                        pprint(result)
                        
                    switch_edit["property"] = "TimeSignatureUpper"
                    switch_edit["value"] = obj["TimeSignatureUpper"]
                    
                    result = client.call("ak.wwise.core.object.setProperty", switch_edit)
                    pprint(result)
                        
                    switch_edit["property"] = "TimeSignatureLower"
                    switch_edit["value"] = obj["TimeSignatureLower"]
                    
                    result = client.call("ak.wwise.core.object.setProperty", switch_edit)
                    pprint(result)
                    
                    
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
                                
                                thestr = f"MusicPlaylistContainer #{p}[{pq}] ({CurrentPlaylistId}) | Tempo: {curtempo} | Time Signature: {timesig}"
                                if (obj2["Properties"]["ParameterCount"] > 0 and obj2["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                    vol = obj2["Properties"]["ParameterValues"][0]
                                    thestr += f" | VoiceVolume: {vol}"
                                print("\n" + thestr)
                                print_list.append("\n" + thestr + "\n")
                                list = obj2["Playlist"]
      
                                
                                
                                
                                object_create_args = {
                                    "parent": f"\\Interactive Music Hierarchy\\Default Work Unit\\{switch_name}",
                                    "type": "MusicPlaylistContainer",
                                    "name": f"MusicPlaylistContainer ({CurrentPlaylistId})",
                                    "children": []
                                }
                                
                                result = client.call("ak.wwise.core.object.create", object_create_args)
                                pprint(result)
                                
                                edit_playlist_args = {
                                    "object": f"\\Interactive Music Hierarchy\\Default Work Unit\\{switch_name}\\MusicPlaylistContainer ({CurrentPlaylistId})",
                                    "property": "Tempo",
                                    "value": obj2["Tempo"],
                                }
                                
                                result = client.call("ak.wwise.core.object.setProperty", edit_playlist_args)
                                pprint(result)
        
        
                                edit_playlist_args["property"] = "TimeSignatureUpper"
                                edit_playlist_args["value"] = obj2["TimeSignatureUpper"]
                                
                                result = client.call("ak.wwise.core.object.setProperty", edit_playlist_args)
                                pprint(result)
                                
                                
                                edit_playlist_args["property"] = "TimeSignatureLower"
                                edit_playlist_args["value"] = obj2["TimeSignatureLower"]
                                
                                result = client.call("ak.wwise.core.object.setProperty", edit_playlist_args)
                                pprint(result)
                                
                                if (obj2["Properties"]["ParameterCount"] > 0 and obj2["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                                    edit_playlist_args["property"] = "Volume"
                                    edit_playlist_args["value"] = obj2["Properties"]["ParameterValues"][0]
                                
                                result = client.call("ak.wwise.core.object.setProperty", edit_playlist_args)
                                pprint(result)
                                
                                
                                

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

result = client.call("ak.wwise.core.audio.import", import_audio_args)

"""
    get_playlist_segments = {
        "waql": f"\"\\Interactive Music Hierarchy\\Default Work Unit\\{bnkname}\" select descendants where type = /^MusicSegment/"
    }
    result = client.call("ak.wwise.core.object.get", get_playlist_segments)

    segments = result["return"]
    for segment in segments:
        cursegid = gf.get_flipped_hex(segment["name"][segment["name"].find("(")+1:segment["name"].find(")")], 8)
        cursegid = int(cursegid, 16)
        for obj in data["Objects"]:
            if obj["Type"] == "MusicSegment" and obj["Id"] == cursegid:
                if (obj["Properties"]["ParameterCount"] != 0 and obj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                    vol_set = {
                        "object": segment["id"],
                        "property": "Volume",
                        "value": obj["Properties"]["ParameterValues"][0]
                    }
                    
                    print(str(cursegid) + ": " + str(obj["Properties"]["ParameterValues"][0]))
                    result = client.call("ak.wwise.core.object.setProperty", vol_set)
                    pprint(result)
"""  
                  
get_playlist_tracks = {
    "waql": f"\"\\Interactive Music Hierarchy\\Default Work Unit\\{switch_name}\" select descendants where type = /^MusicTrack/"
}
track_result = client.call("ak.wwise.core.object.get", get_playlist_tracks)

tracks = track_result["return"]
for track in tracks:
    curtrackid = gf.get_flipped_hex(track["name"], 8)
    curtrackid = int(curtrackid, 16)
    for obj in data["Objects"]:
        if obj["Type"] == "MusicTrack" and obj["SoundCount"] != 0 and obj["Sounds"][0]["AudioId"] == curtrackid:
            if (obj["Properties"]["ParameterCount"] != 0 and obj["Properties"]["ParameterTypes"][0] == "VoiceVolume"):
                vol_set = {
                    "object": track["id"],
                    "property": "Volume",
                    "value": obj["Properties"]["ParameterValues"][0]
                }
                result = client.call("ak.wwise.core.object.setProperty", vol_set)
client.disconnect()
        
print("Done!")