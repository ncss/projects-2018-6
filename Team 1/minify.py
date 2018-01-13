import sys
text = []
for line in open(sys.argv[1]):
    if line.strip() and not line.strip().startswith('#'):
        text.append(line.rstrip())
        print(repr(line))

filename = sys.argv[1][:-3]+'_mini.py'
with open(filename, 'w') as f:
    f.write('\n'.join(text))
