import kenlm
import sys
import os
import sqlite3
import importlib

langmodel=sys.argv[1]
perpdatabase=sys.argv[2]
tokenizer=sys.argv[3]

if not tokenizer=="None":
    if not tokenizer.endswith(".py"): tokenizer=SL_TOKENIZER+".py"
    spec = importlib.util.spec_from_file_location('', tokenizer)
    tokenizermod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tokenizermod)
    tokenizer=tokenizermod.Tokenizer()

if os.path.isfile(perpdatabase):
    os.remove(perpdatabase)

conn=sqlite3.connect(perpdatabase)
cur = conn.cursor() 
cur.execute("CREATE TABLE perplexities(id INTEGER PRIMARY KEY, perplexity REAL, source TEXT, target TEXT)")
model=kenlm.Model(langmodel) 
cont=0
data=[]
for line in sys.stdin:
    record=[]
    if 'q' == line.rstrip():
        break
    line=line.rstrip()
    camps=line.split("\t")
    source=camps[0]
    source=source.replace("’","'")
    if not tokenizer=="None":
        sourcetok=tokenizer.tokenize(source)
    else:
        sourcetok=source
    if len(camps)>=2:
        target=camps[1]
    else:
        target=""
    per=model.perplexity(sourcetok)
    record.append(cont)
    record.append(per)
    record.append(source)
    record.append(target)
    data.append(record)
    if cont%1000000==0:
        cur.executemany("INSERT INTO perplexities (id, perplexity, source, target) VALUES (?,?,?,?)",data)
        data=[]
        conn.commit()
    cont+=1
cur.executemany("INSERT INTO perplexities (id, perplexity, source, target) VALUES (?,?,?,?)",data)
conn.commit()
