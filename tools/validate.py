#!/usr/bin/env python3
"""Validate a Kannect level file. Usage: validate.py FILE.json [--quiet]
A file is a JSON list of walls:
{"difficulty":1-5,
 "groups":[{"link":"Birds","note":"optional","tiles":[["SWIFT"],["KITE","🪁"],["WREN"],["FINCH"]]}, x4],
 "overlaps":{"ROOK":["Birds"]}}   # word -> links of OTHER groups in this wall it could also fit
"""
import json,sys,re,itertools,collections
def norm(l): return re.sub(r'[^a-z0-9]+',' ',l.lower()).strip()
def solutions(cands,limit=3):
    n=0
    def rec(i,used):
        nonlocal n
        if n>=limit: return
        if i==4: n+=1; return
        for c in itertools.combinations([w for w in cands[i] if w not in used],4):
            rec(i+1,used|set(c))
    rec(0,frozenset()); return n
def check_wall(w,i):
    errs=[]; E=lambda m: errs.append(f"wall {i+1}: {m}")
    g=w.get('groups',[])
    if len(g)!=4: E("needs 4 groups"); return errs
    if w.get('difficulty') not in (1,2,3,4,5): E("difficulty must be 1-5")
    words=[];links=[];pics=0
    for G in g:
        links.append(G.get('link',''))
        if not G.get('link'): E("group missing link")
        if len(G.get('tiles',[]))!=4: E(f"{G.get('link')}: needs 4 tiles"); continue
        for t in G['tiles']:
            if not isinstance(t,list) or not t: E(f"bad tile {t}"); continue
            x=t[0]; words.append(x)
            if not re.fullmatch(r"[A-Z]{2,9}",x): E(f"'{x}': tiles must be one word, 2-9 capital letters A-Z")
            if len(t)>1:
                pics+=1
                if re.search(r'[A-Za-z0-9]',t[1]) or len(t[1])>8: E(f"'{x}': picture must be a single emoji")
    if len(set(words))!=16: E("16 distinct words required: "+str([x for x,c in collections.Counter(words).items() if c>1]))
    if len(set(map(norm,links)))!=4: E("duplicate link in wall")
    if not 3<=pics<=7: E(f"needs 3-7 picture tiles, has {pics}")
    ov=w.get('overlaps',{})
    cands=[set(t[0] for t in G['tiles']) for G in g]
    for word,ls in ov.items():
        if word not in words: E(f"overlap word {word} not in wall"); continue
        for l in ls:
            if l not in links: E(f"overlap link '{l}' not in wall"); continue
            j=links.index(l)
            if word in cands[j]: E(f"{word} already belongs to '{l}'")
            cands[j].add(word)
    if len(ov)<3: E(f"needs at least 3 red-herring words in overlaps, has {len(ov)}")
    if not errs and solutions([sorted(c) for c in cands])!=1: E("declared overlaps allow more than one valid solution")
    return errs
def main():
    data=json.load(open(sys.argv[1],encoding='utf8')); errs=[]
    seen={};wc=collections.Counter()
    for i,w in enumerate(data):
        errs+=check_wall(w,i)
        for G in w.get('groups',[]):
            k=norm(G.get('link',''))
            if k in seen: errs.append(f"wall {i+1}: link '{G['link']}' already used in wall {seen[k]+1}")
            seen[k]=i
            for t in G.get('tiles',[]): wc[t[0]]+=1
    for x,c in wc.items():
        if c>1: errs.append(f"word {x} used {c} times in this file (max 1)")
    print(f"{len(data)} walls, {len(errs)} problems")
    for e in errs: print(" -",e)
    sys.exit(1 if errs else 0)
if __name__=='__main__': main()
