import sqlite3
import codecs
import sys

perpdatabase=sys.argv[1]
limit=int(sys.argv[2])
outfile=sys.argv[3]

conn=sqlite3.connect(perpdatabase)
cur = conn.cursor() 
cur.execute("SELECT id,perplexity,source,target FROM perplexities ORDER BY perplexity ASC limit "+str(limit)+";")


results=cur.fetchall()

sortida=codecs.open(outfile,"w",encoding="utf-8")
for result in results:
    cadena=result[2]+"\t"+result[3]
    sortida.write(cadena+"\n")
    

