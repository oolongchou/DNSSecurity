import sys

filename1 = sys.argv[1]
filename2 = sys.argv[2]
listf = open(filename1)

file1 = {}

for line in listf:
    line = line.strip()
    file1[line] = 0


listf = open(filename2)


file2 = {}

for line in listf:
    line = line.strip()
    file2[line] = 0

outputf = open(filename1.strip(".txt")+"_diff.txt","w")

for line in file2:
    #if line not in file1:
    if line in file1:
        outputf.write(line + "\n")
