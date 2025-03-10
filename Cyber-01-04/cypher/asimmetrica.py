from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os

# Funzione per generare e salvare la coppia di chiavi
def generate_keys():
    key_pair = RSA.generate(2048)
    private_key = key_pair.export_key()
    public_key = key_pair.publickey().export_key()

    # Salvataggio delle chiavi su file
    # (notare che private_key e public_key sono bytes e non str)
    with open("private.pem", "wb") as f:
        f.write(private_key)
    with open("public.pem", "wb") as f:
        f.write(public_key)

    # Messaggio di successo
    print("Chiavi generate e salvate come 'private.pem' e 'public.pem' nel path: " + os.getcwd())

# Funzione per importare la chiave pubblica
def load_public_key(file_path):
    with open(file_path, "r") as f:
        return RSA.import_key(f.read())

# Funzione per importare la chiave privata
def load_private_key():
    with open("private.pem", "r") as f:
        return RSA.import_key(f.read())

# Funzione per cifrare il messaggio
def encrypt_message(message: str, pub_key):
    cipher = PKCS1_OAEP.new(pub_key)
    encrypted_message = cipher.encrypt(message.encode("utf-8"))
    return base64.b64encode(encrypted_message).decode("utf-8")

# Funzione per decifrare il messaggio
def decrypt_message(encrypted_message, priv_key):
    cipher = PKCS1_OAEP.new(priv_key)
    decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message.decode("utf-8")

# Main
def main():
    while True:
        print("\nMenu:")
        print("1. Genera chiavi RSA")
        print("2. Cifra un messaggio")
        print("3. Decifra un messaggio")
        print("\n4. Esci\n")

        choice = input("Scegli un'opzione (1-4): ")

        if choice == '1':
            generate_keys()

        elif choice == '2':
            pub_key_path = input("\nInserisci il percorso del file della chiave pubblica (default: public.pem): ") or "public.pem"
            if not os.path.exists(pub_key_path):
                print("\nIl file della chiave pubblica non esiste. Assicurati che il nome o il path inserito sia corretto.\n")
                continue

            public_key = load_public_key(pub_key_path)
            message = input("\nInserisci il messaggio da cifrare: ")
            encrypted_message = encrypt_message(message, public_key)
            print("\nMessaggio cifrato:\n", encrypted_message, sep="")

        elif choice == '3':
            private_key = load_private_key()
            encrypted_input = input("\nInserisci il messaggio cifrato da decifrare: ")
            decrypted_message = decrypt_message(encrypted_input, private_key)
            print("\nMessaggio decifrato:\n", decrypted_message, sep="")

       

        elif choice == '4':
            print("\n\nUscita dal programma.")
            break

        else:
            print("\nScelta non valida. Riprova.\n\n")

if __name__ == "__main__":
    main()