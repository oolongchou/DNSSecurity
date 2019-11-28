import random
import sys,os
import tqdm

seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numberseed="1234567890"

def checkpath(result_path):
    isExists = os.path.exists(result_path)
    if not isExists:
        os.makedirs(result_path)



def loadNS(filename):
    File = open(filename, "r")
    outCMD=open("attack/afxrTest.txt","w")
    outUPDATE=open("attack/updatelist.txt","w")
    outUPDATECheck=open("attack/updatecheck.txt","w")
    for line in File:
        line = line.strip()
        try:
            outCMD.writelines("dig axfr " + line.split()[0] + " @" + line.split("\t")[-1] + "\n")

            outF = open("update/" + line.split()[0] +"@" + line.split("\t")[-1] + ".txt", "w")

            n=random.randrange(3,10)
            sa = []

            for i in range(n):
                sa.append(random.choice(seed))
            salt = ''.join(sa)
            #print(salt)

            rip = lambda: '.'.join(
                [str(int(''.join([str(random.randint(0, 2)), str(random.randint(0, 5)), str(random.randint(0, 5))])))
                 for _ in range(4)])
            randomip=str(rip())

            outF.writelines(
                "server " + line.split("\t")[-1] + "\n" + "update add "+ salt+"." + line.split()[
                    0] + " 86400 IN A "+ randomip + "\n" + "send \n")

            outUPDATE.writelines(line.split("\t")[0] +"@" + line.split("\t")[-1]+ "\n")

            outUPDATECheck.writelines(
                "dig @" + line.split("\t")[-1] + " " +salt+"."+ line.split("\t")[0] + '\t'+randomip+"\n")


        except Exception as e:
            print e
            continue

filename = sys.argv[1]

checkpath("attack/")

checkpath("update/")
loadNS(filename)

