import csv,glob,re,json,os,collections
csv.field_size_limit(10**9)
D=os.path.expanduser('~/mnt/Government Transparency Project/Output/HTML/Dialogue')
OUT=os.path.expanduser('~/mnt/Government Transparency Project/Output/Reports/children-appeals/_work')
ODD={'Claremont School Board - 8526.CSV':'2026-08-05','Claremont School Board Meeting 2123.mp4.CSV':'2023-02-01'}
def fdate(f):
    if f in ODD: return ODD[f]
    m=re.search(r'(\d{5,6})(?:\.mp4)?\.CSV$',f); d=m.group(1).zfill(6)
    mm,dd,yy=d[:2],d[2:4],d[4:]
    return f"20{yy}-{mm}-{dd}"
C=r"(?:kids?|child(?:ren)?|students?|youth|young people|learners|pupils?)"
A=[rf"\bour (?:own )?{C}\b",
 rf"\b(?:for|to|of|on) (?:the|these|those|all|every|each|our|their|your|my) {C}\b",
 rf"\bbest interests? of",rf"\bwhat(?:'s| is| was) best for",
 rf"\b{C} (?:first|come first|deserve|need to|should|must)\b",
 rf"\babout (?:the |our )?{C}",rf"\bput(?:ting)? (?:the |our )?{C} first",
 rf"\b(?:benefit|benefits|benefiting|harm|hurt|hurts|hurting|damage|detriment|impact|impacts|impacted) (?:of |for |to |on |the )?(?:the |our )?{C}",
 rf"\b{C}(?:'s|s')? (?:education|future|welfare|well-?being|needs|interests?|success|achievement|experience|safety|learning)",
 rf"\b(?:sake|behalf) of",rf"\b(?:good|better|best|worse|worst|right|wrong|fair|unfair) (?:for|to) (?:the |our |all )?{C}",
 rf"\b(?:student|child|children|kid)[- ](?:centered|focused)\b",
 rf"\bstudent (?:achievement|outcomes?|success|performance|welfare|learning|safety|needs?)\b",
 rf"\b(?:the|these|those|our) (?:kids|children)\b",rf"\byoung people\b",rf"\byouth\b"]
pa=re.compile("|".join(A),re.I)
anyc=re.compile(rf"\b{C}\b|\bchild's\b|\bchildren's\b|\bstudent's\b|\bstudents'\b",re.I)
turns=[]
for f in sorted(glob.glob(D+'/*.CSV')):
    fn=os.path.basename(f); date=fdate(fn)
    rows=list(csv.DictReader(open(f,encoding='utf-8-sig')))
    cur=None
    def flush():
        pass
    chunks=[]
    for i,x in enumerate(rows):
        key=(x['Speaker'])
        w=len(x['Dialogue'].split())
        if cur and cur['speaker']==key and cur['words']+w<=250:
            cur['text']+=' '+x['Dialogue']; cur['words']+=w; cur['end']=x['End']; cur['rows'].append(i)
        else:
            if cur: chunks.append(cur)
            cur={'file':fn,'date':date,'speaker':key,'role':x['Role'],'start':x['Start'],'start_sec':x['Start (sec)'],'end':x['End'],'url':x['Video URL'],'text':x['Dialogue'],'words':w,'rows':[i]}
    if cur: chunks.append(cur)
    for j,c in enumerate(chunks):
        c['id']=f"{fn.split('.')[0].split(' ')[0]}-{j}" if fn[0].isdigit() else f"{abs(hash(fn))%99999}-{j}"
        c['prev']=(chunks[j-1]['speaker']+': '+' '.join(chunks[j-1]['text'].split()[-45:])) if j>0 else ''
        c['next']=(chunks[j+1]['speaker']+': '+' '.join(chunks[j+1]['text'].split()[:30])) if j+1<len(chunks) else ''
        turns.append(c)
cand=[t for t in turns if pa.search(t['text'])]
rest=[t for t in turns if not pa.search(t['text']) and anyc.search(t['text'])]
print('turns',len(turns),'candidates',len(cand),'student-mention non-candidates',len(rest))
words=sum(t['words'] for t in cand);print('cand words',words)
import random;random.seed(7)
audit=random.sample(rest,min(400,len(rest)))
for name,L in [('candidates',cand),('audit',audit)]:
    with open(f'{OUT}/{name}.jsonl','w') as fh:
        for t in L: fh.write(json.dumps(t)+'\n')
json.dump({'turns':len(turns),'cand':len(cand),'rest':len(rest)},open(f'{OUT}/counts.json','w'))
print(collections.Counter(t['file'] for t in cand).most_common(3))
