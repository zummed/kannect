#!/usr/bin/env python3
"""Merge levels/core.json + levels/batch_*.json into kannect.html.
Drops walls that fail validation, repeat a link, or would use a word a third time. Usage: build.py [--dry]"""
import json,glob,sys,os,collections,itertools
sys.path.insert(0,os.path.dirname(__file__))
from validate import check_wall,norm
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORD_CAP=2
core=json.load(open(f'{root}/levels/core.json',encoding='utf8'))
batches=[]
for f in sorted(glob.glob(f'{root}/levels/batch_*.json')):
    try: batches.append((os.path.basename(f),json.load(open(f,encoding='utf8'))))
    except Exception as e: print('SKIP',f,e)
# gentle ramp: by difficulty, round-robin across batches so subjects alternate
pool=[]
for d in range(1,6):
    cols=[[(n,i,w) for i,w in enumerate(b) if w.get('difficulty')==d] for n,b in batches]
    for row in itertools.zip_longest(*cols):
        pool+= [x for x in row if x]
links=set();words=collections.Counter();out=[];dropped=collections.Counter()
def take(w):
    for g in w['groups']:
        links.add(norm(g['link']))
        for t in g['tiles']: words[t[0]]+=1
    out.append({'groups':[{k:g[k] for k in ('link','note','tiles') if k in g} for g in w['groups']]})
for w in core: take(w)
for n,i,w in pool:
    if check_wall(w,i): dropped[n+': invalid']+=1; continue
    if any(norm(g['link']) in links for g in w['groups']): dropped[n+': repeated link']+=1; continue
    if any(words[t[0]]>=WORD_CAP for g in w['groups'] for t in g['tiles']): dropped[n+': overused word']+=1; continue
    take(w)
print(len(out),'walls kept;',sum(dropped.values()),'dropped',dict(dropped))
print('words used twice:',sum(1 for c in words.values() if c>1),'of',len(words))
if '--dry' in sys.argv: sys.exit()
p=f'{root}/kannect.html'; s=open(p,encoding='utf8').read()
a=s.index('const LEVELS=['); b=s.index('];\n',a)+3
body=',\n'.join(json.dumps(w,ensure_ascii=False,separators=(',',':')) for w in out)
open(p,'w',encoding='utf8').write(s[:a]+'const LEVELS=[\n'+body+'\n];\n'+s[b:])
