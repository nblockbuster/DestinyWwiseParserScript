from math import floor
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