import random, os

# Creazione randomica attraverso os.system openssl
prime_number = int(os.popen("openssl prime -generate -bits 100").read().strip())
print("Random numbers generated:")
print(f"Generated prime number: {prime_number}")

secret = random.randint(1, prime_number-1)
alice = random.randint(1, prime_number-1)
bob = random.randint(1, prime_number-1)

print(f"Secret number: {secret}")
print(f"Alice's random number: {alice}")
print(f"Bob's random number: {bob}\n")

# Calcoli chiavi
Alice = pow(secret, alice, prime_number)
Bob = pow(secret, bob, prime_number)
print("Personal keys calculated:")
print(f"Alice's key: {Alice}")
print(f"Bob's key: {Bob}\n")

# Chiavi
kbob = pow(Alice, bob, prime_number)
kali = pow(Bob, alice, prime_number)
print("Keys calculated:")
print(f"Key for Bob: {kbob}")
print(f"Key for Alice: {kali}\n")

# Verifica che le chiavi siano uguali
if kbob == kali:
    print("Keys match!")
else:
    print("Keys do not match!")
