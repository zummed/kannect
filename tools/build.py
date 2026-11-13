#!/usr/bin/env python3
"""Merge levels/core.json + levels/batch_*.json into kannect.html.

Wall numbers are permanent. levels/order.json records the play order; walls already in it keep their
place, and walls not yet in it are appended to the end. Newly added walls are mixed among themselves:
gentle to hard, alternating between their batch files so subjects do not clump. Walls marked
"feature": true (personal ones) are instead spaced evenly through the new walls.
Words may recur across walls; a new wall is dropped only if it fails validation or repeats a group
(the same four tiles, or three of the same four) that is already in the game.
Usage: build.py [--dry]"""
import json,glob,sys,os,collections,itertools,hashlib
sys.path.insert(0,os.path.dirname(__file__))
from validate import check_wall,group_words,same_combo
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
combos=[];words=collections.Counter();out=[];ids=[];dropped=collections.Counter()
def take(w):
    for g in w['groups']:
        combos.append(group_words(g))
        for t in g['tiles']: words[t[0]]+=1
    ids.append(wid(w))
    out.append({'groups':[{k:g[k] for k in ('link','note','tiles') if k in g} for g in w['groups']]})
missing=[i for i in order if i not in byid]
if missing: sys.exit(f'{len(missing)} walls listed in order.json are no longer in any level file; restoring them keeps numbering stable: {missing[:5]}')
for i in order: take(byid[i])
kept=len(out); placed=set(order)
for w in core:
    if wid(w) not in placed: take(w); placed.add(wid(w))
pool=[];pending=[];regular=[];feature=[]
for d in range(1,6):
    cols=[[(n,i,w) for i,w in enumerate(b) if w.get('difficulty')==d and 'groups' in w] for n,b in batches]
    for row in itertools.zip_longest(*cols): pool+=[x for x in row if x]
pool.sort(key=lambda x: not x[2].get('feature'))  # feature walls claim their groups first (stable sort keeps the rest in order)
for n,i,w in pool:
    try: k=wid(w)
    except Exception: dropped[n+': invalid']+=1; continue
    if k in placed: continue
    if check_wall(w,i): dropped[n+': invalid']+=1; continue
    mine=[group_words(g) for g in w['groups']]
    if any(same_combo(a,c) for a in mine for c in combos+pending): dropped[n+': repeated group']+=1; continue
    pending+=mine; placed.add(k); (feature if w.get('feature') else regular).append(w)
# feature walls (marked "feature": true, e.g. personal ones) are spaced evenly through this build's new walls
for j,w in enumerate(feature): regular.insert(round((j+.5)*len(regular)/len(feature))+j,w)
for w in regular: take(w)
print(f'{len(out)} walls: {kept} already placed, {len(out)-kept} appended; {sum(dropped.values())} dropped',dict(dropped))
print(len(words),'distinct words; most reused:',words.most_common(8))
if '--dry' in sys.argv: sys.exit()
json.dump(ids,open(op,'w'),indent=0)
p=f'{root}/kannect.html'; s=open(p,encoding='utf8').read()
a=s.index('const LEVELS=['); b=s.index('];\n',a)+3
body=',\n'.join(json.dumps(w,ensure_ascii=False,separators=(',',':')) for w in out)
page=s[:a]+'const LEVELS=[\n'+body+'\n];\n'+s[b:]
open(p,'w',encoding='utf8').write(page)
# index.html: the same game as a complete web page, for hosting anywhere (GitHub Pages etc.)
SHELL='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#E4ECEF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0F1820" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<style>:root{color-scheme:light;padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
'''
t=page.index('<style>')
open(f'{root}/index.html','w',encoding='utf8').write(SHELL+page[:t]+'</head>\n<body>\n'+page[t:]+'</body>\n</html>\n')
