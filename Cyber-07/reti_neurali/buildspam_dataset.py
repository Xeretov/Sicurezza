import os
import pandas as pd

def load_emails_from_directory(directory_path, label):
    """
    Carica tutti i file di testo da directory_path,
    restituendo una lista di dizionari {'text': contenuto, 'label': label}.
    """
    emails_data = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
                # A seconda delle tue esigenze, potresti voler rimuovere intestazioni o processare ulteriormente il testo
                emails_data.append({'text': content, 'label': label})
    return emails_data

# Percorsi (adatta in base a dove hai estratto il corpus)
spam_dir = 'spamassassin_public_corpus/spam'
spam_dir2 = 'spamassassin_public_corpus/spam_2'
easy_ham_dir = 'spamassassin_public_corpus/easy_ham'
easy_ham_dir2 = 'spamassassin_public_corpus/easy_ham_2'
hard_ham_dir = 'spamassassin_public_corpus/hard_ham'  # opzionale

# Carica spam (label=1)
spam_emails = load_emails_from_directory(spam_dir, label=1)
spam_emails2 = load_emails_from_directory(spam_dir2, label=1)

# Carica ham (label=0)
easy_ham_emails = load_emails_from_directory(easy_ham_dir, label=0)
easy_ham_emails2 = load_emails_from_directory(easy_ham_dir2, label=0)
hard_ham_emails = load_emails_from_directory(hard_ham_dir, label=0)  # opzionale

# Combina tutto in un'unica lista
all_emails = spam_emails + spam_emails2 + easy_ham_emails + easy_ham_emails2 + hard_ham_emails

# Crea un DataFrame
df = pd.DataFrame(all_emails)

# Opzionale: shuffle (per mescolare spam e ham)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Esporta in CSV
df.to_csv('spam_dataset.csv', index=False)
print("Creato spam_dataset.csv con", len(df), "righe.")
