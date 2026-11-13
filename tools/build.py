#!/usr/bin/env python3
"""Merge levels/core.json + levels/batch_*.json into kannect.html.

Wall numbers are permanent. levels/order.json records the play order; walls already in it keep their
place, and walls not yet in it are appended to the end. Newly added walls are mixed among themselves:
gentle to hard, alternating between their batch files so subjects do not clump.
A new wall is dropped if it fails validation, repeats a link, or would use a word a third time.
Usage: build.py [--dry]"""
import json,glob,sys,os,collections,itertools,hashlib
sys.path.insert(0,os.path.dirname(__file__))
from validate import check_wall,norm
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORD_CAP=2
def wid(w):  # identity of a wall = its sixteen words, so moving or reformatting a file changes nothing
    return hashlib.sha1(' '.join(sorted(t[0] for g in w['groups'] for t in g['tiles'])).encode()).hexdigest()[:12]
core=json.load(open(f'{root}/levels/core.json',encoding='utf8'))
batches=[]
for f in sorted(glob.glob(f'{root}/levels/batch_*.json')):
    try: batches.append((os.path.basename(f),json.load(open(f,encoding='utf8'))))
    except Exception as e: print('SKIP',f,e)
byid={}
for n,b in [('core.json',core)]+batches:
    for w in b:
        try: byid.setdefault(wid(w),w)
        except Exception: pass
op=f'{root}/levels/order.json'
order=json.load(open(op)) if os.path.exists(op) else []
links=set();words=collections.Counter();out=[];ids=[];dropped=collections.Counter()
def take(w):
    for g in w['groups']:
        links.add(norm(g['link']))
        for t in g['tiles']: words[t[0]]+=1
    ids.append(wid(w))
    out.append({'groups':[{k:g[k] for k in ('link','note','tiles') if k in g} for g in w['groups']]})
missing=[i for i in order if i not in byid]
if missing: sys.exit(f'{len(missing)} walls listed in order.json are no longer in any level file; restoring them keeps numbering stable: {missing[:5]}')
for i in order: take(byid[i])
kept=len(out); placed=set(order)
for w in core:
    if wid(w) not in placed: take(w); placed.add(wid(w))
pool=[]
for d in range(1,6):
    cols=[[(n,i,w) for i,w in enumerate(b) if w.get('difficulty')==d and 'groups' in w] for n,b in batches]
    for row in itertools.zip_longest(*cols): pool+=[x for x in row if x]
for n,i,w in pool:
    try: k=wid(w)
    except Exception: dropped[n+': invalid']+=1; continue
    if k in placed: continue
    if check_wall(w,i): dropped[n+': invalid']+=1; continue
    if any(norm(g['link']) in links for g in w['groups']): dropped[n+': repeated link']+=1; continue
    if any(words[t[0]]>=WORD_CAP for g in w['groups'] for t in g['tiles']): dropped[n+': overused word']+=1; continue
    take(w); placed.add(k)
print(f'{len(out)} walls: {kept} already placed, {len(out)-kept} appended; {sum(dropped.values())} dropped',dict(dropped))
print('words used twice:',sum(1 for c in words.values() if c>1),'of',len(words))
if '--dry' in sys.argv: sys.exit()
json.dump(ids,open(op,'w'),indent=0)
p=f'{root}/kannect.html'; s=open(p,encoding='utf8').read()
a=s.index('const LEVELS=['); b=s.index('];\n',a)+3
body=',\n'.join(json.dumps(w,ensure_ascii=False,separators=(',',':')) for w in out)
open(p,'w',encoding='utf8').write(s[:a]+'const LEVELS=[\n'+body+'\n];\n'+s[b:])
