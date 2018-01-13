from pokemon_img import *

with open('blastoise.dat', 'wb') as f:
    for line in blastoise.split('\n'):
        try:

            print(line)
            byte_line = int(line.strip(), 2).to_bytes(7, 'big')
        except:
            print(line)
        f.write(byte_line)

with open('blastoise.dat', 'rb') as f:
    byte_string = f.read()

image = [byte_string[a:a+7] for a in range(0, len(byte_string), 7)]
print(image)
final = [bin(int.from_bytes(line, 'big'))[2:] for line in image]
print('\n'.join(final))
