fp = open("wordlist.txt", "w")

for i in range (10):
    for j in range (10):
        for k in range (10):
            for l in range (10):
                fp.write(str(i) + str(j) + str(k) + str(l) + "\n");
fp.close()