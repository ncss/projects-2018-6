files = ['venusaur.dat', 'charizard.dat', 'blastoise.dat']

byte_string = b''
for file in files:
    with open(file, 'rb') as f:
        byte_string += f.read()

with open('images.dat', 'wb') as f:
    f.write(byte_string)
