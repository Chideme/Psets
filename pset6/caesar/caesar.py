# import modules
import sys

def function():
    if len(sys.argv) == 2 :
        k = int(sys.argv[1])
        plain = input("plaintext: ")
        cypher = ""
        for i in range(0,len(plain)):
            if plain[i].isalpha():
                if plain[i].isupper():
                    a = ord(plain[i]) - 65
                    b = 65 + ((a + k) % 26)
                    cypher += chr(b)
                else:
                    c = ord(plain[i]) - 97
                    d = 97 + ((c + k) % 26)
                    cypher += chr(d)
            else:
                cypher += plain[i]
        print("ciphertext: {}".format(cypher))
        sys.exit(0)
    else:
        print("Usage: python caesar k")
        sys.exit(1)

if __name__ == '__main__':
    function()