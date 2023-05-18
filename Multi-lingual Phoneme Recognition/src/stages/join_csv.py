import csv

def process_word(word: str)-> str:
    r = ''
    for l in word:
        if not l.isalpha() and l!=' ':
            continue
        r+=l.lower()
    return r

f1 = open('/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/xls-r_dataset_v2.csv')
f2 = open('/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/датасет6.csv')

f1.readline()
f2.readline()

d_words = {}

f1_reader = csv.reader(f1)

for line in f1_reader:
    ix, word, ipa = line
    d_words[process_word(word)] = (ix, ipa)

f1.close()

f1_reader = csv.reader(f2)

ix2=1001
for line in f1_reader:
    ix, word, ipa = line
    d_words[str(ix)] = (ix2, ipa)
    ix2+=1

f1.close()

out_f = open('/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/xls-r_dataset_v3.csv', 'w')
csv_writer = csv.writer(out_f)
i=0
csv_writer.writerow(['','text','IPA'])
for word, (ix, ipa) in d_words.items():
    csv_writer.writerow([ix, word, ipa])
out_f.close()