import csv,glob,re,collections,json,datetime,os,sys
D='Output/HTML/Dialogue'
def cls(role):
    r=role.lower()
    if r.startswith('unidentified') or r=='' : return 'unid'
    if 'public commenter' in r or 'resident' in r or 'parent' in r or 'citizen' in r: return 'public'
    if 'student rep' in r: return 'student'
    if any(k in r for k in ['mayor','councilor','city manager','city council','assistant mayor']): return 'city'
    if any(k in r for k in ['auditor','attorney','consultant','nhsba','school boards association','guest','presenter','nh department','commissioner','legislat','representative','senator']): return 'outside'
    if any(k in r for k in ['superintendent','business administrator','director','principal','coordinator','assistant superintendent','finance','curriculum','teacher','staff','nurse','clerk','secretary','manager','technology','facilities','sped','special education','food','athletic','human resources','payroll','bookkeeper','accountant','administrator']) and 'board' not in r.split(',')[0]: return 'admin'
    if 'moderator' in r: return 'moderator'
    if 'board' in r or 'committee' in r or 'subcommittee' in r:
        if 'vice' in r: return 'vicechair'
        if 'chair' in r: return 'chair'
        return 'member'
    if 'group' in r or 'pledge' in r: return 'unid'
    return 'other'
def meeting_date(fn):
    stem=fn.split(' ',1)[1] if re.match(r'^\d+ ',fn) else fn
    m=re.search(r'(\d{6})(?:_\d)?\.mp4',stem) or re.search(r'(?<!\d)(\d{6})(?!\d)',stem)
    if m:
        s=m.group(1)
        try: return datetime.date(2000+int(s[4:6]),int(s[0:2]),int(s[2:4]))
        except: return None
    m=re.search(r'(?<!\d)(\d{5})(?!\d)',stem)  # M DD YY or MM D YY with no zero padding
    if m:
        s=m.group(1)
        for mo,da in ((s[0],s[1:3]),(s[0:2],s[2])):
            try: return datetime.date(2000+int(s[3:5]),int(mo),int(da))
            except: pass
    m=re.search(r'(?<!\d)(\d{4})(?!\d)',stem)
    if m:
        s=m.group(1)
        try: return datetime.date(2000+int(s[2:4]),int(s[0]),int(s[1]))
        except: return None
    return None
def era_of(d):
    # board era = from second Tuesday of March of year Y to the day before that in Y+1
    def st(y):
        d1=datetime.date(y,3,1); wd=(1-d1.weekday())%7
        return d1+datetime.timedelta(days=wd+7)
    y=d.year
    return y if d>=st(y) else y-1
def gini(xs):
    xs=sorted(x for x in xs if x>0); n=len(xs)
    if n<2: return 0.0
    s=sum(xs); c=sum((i+1)*x for i,x in enumerate(xs))
    return (2*c)/(n*s)-(n+1)/n
rows=[]
for f in sorted(glob.glob(D+'/*.CSV')):
    fn=os.path.basename(f); d=meeting_date(fn)
    if not d: print('nodate',fn,file=sys.stderr); continue
    body='SAU6' if 'SAU6' in fn else ('Finance' if 'Finance' in fn else ('Deliberative' if 'Deliberative' in fn else ('Budget' if 'Budget' in fn else ('Joint' if 'Joint' in fn or 'City' in fn else 'Board'))))
    secs=collections.Counter(); bysp=collections.Counter(); spcls={}
    txt=collections.Counter(); total=0.0; nrows=0; pubturns=0
    with open(f,encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try: dur=float(r['End (sec)'])-float(r['Start (sec)'])
            except: continue
            if dur<0 or dur>600: continue
            c=cls(r.get('Role') or ''); sp=(r.get('Speaker') or '').strip()
            secs[c]+=dur; total+=dur; nrows+=1
            if c in('member','chair','vicechair'):
                bysp[sp]+=dur; spcls[sp]=c
            t=(r.get('Dialogue') or '').lower()
            if re.search(r'roll ?call',t): txt['rollcall']+=1
            if re.search(r'(all|those) (those )?in favor',t): txt['voicevote']+=1
            if re.search(r'non-? ?public',t): txt['nonpublic']+=1
            if 'unanimous' in t: txt['unanimous']+=1
            if re.search(r'\baudit',t): txt['audit']+=1
            if 'fund balance' in t: txt['fundbal']+=1
            if 'esser' in t: txt['esser']+=1
            if 'reimburs' in t: txt['reimb']+=1
            if re.search(r'\bi (would like to |want to |)(make a |)(motion|move)\b|so moved',t): txt['motion']+=1
            if 'consent agenda' in t: txt['consent']+=1
            if 'second reading' in t or 'first reading' in t: txt['reading']+=1
            if re.search(r'point of order|out of order',t): txt['order']+=1
            if c=='public': pubturns+=1
    board=sum(bysp.values())
    top=max(bysp.values()) if bysp else 0
    chairsecs=sum(v for k,v in bysp.items() if spcls[k]=='chair')
    rows.append(dict(file=fn,date=d.isoformat(),era=era_of(d),body=body,total_min=round(total/60,1),
        board_share=round(board/total,3) if total else 0, admin_share=round(secs['admin']/total,3) if total else 0,
        public_share=round(secs['public']/total,3) if total else 0, outside_share=round(secs['outside']/total,3) if total else 0,
        unid_share=round(secs['unid']/total,3) if total else 0,
        chair_share_of_board=round(chairsecs/board,3) if board else 0, top_share_of_board=round(top/board,3) if board else 0,
        board_gini=round(gini(bysp.values()),3), n_board_speakers=len(bysp), public_turns=pubturns, **txt))
keys=['file','date','era','body','total_min','board_share','admin_share','public_share','outside_share','unid_share','chair_share_of_board','top_share_of_board','board_gini','n_board_speakers','public_turns','rollcall','voicevote','nonpublic','unanimous','audit','fundbal','esser','reimb','motion','consent','reading','order']
with open('Output/Reports/signatures-by-meeting.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=keys,extrasaction='ignore'); w.writeheader()
    for r in rows: w.writerow({k:r.get(k,0) for k in keys})
# by era, School Board meetings only (Board+Finance+Budget+Special), and SAU6 separately
def agg(sel,label):
    by=collections.defaultdict(list)
    for r in sel: by[r['era']].append(r)
    out=[]
    for e in sorted(by):
        rs=by[e]; n=len(rs); tm=sum(r['total_min'] for r in rs)
        def wavg(k): return round(sum(r[k]*r['total_min'] for r in rs)/tm,3) if tm else 0
        def per10h(k): return round(sum(r.get(k,0) for r in rs)/(tm/600),2) if tm else 0
        out.append(dict(era=e,meetings=n,hours=round(tm/60,1),board_share=wavg('board_share'),admin_share=wavg('admin_share'),public_share=wavg('public_share'),outside_share=wavg('outside_share'),unid_share=wavg('unid_share'),chair_share=wavg('chair_share_of_board'),top_share=wavg('top_share_of_board'),gini=round(sum(r['board_gini'] for r in rs)/n,3),
            rollcall_per10h=per10h('rollcall'),voicevote_per10h=per10h('voicevote'),nonpublic_per10h=per10h('nonpublic'),unanimous_per10h=per10h('unanimous'),audit_per10h=per10h('audit'),fundbal_per10h=per10h('fundbal'),esser_per10h=per10h('esser'),reimb_per10h=per10h('reimb'),motion_per10h=per10h('motion'),public_turns_per10h=per10h('public_turns')))
    with open(f'Output/Reports/signatures-by-era-{label}.csv','w',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    print('==',label)
    print(','.join(out[0].keys()))
    for o in out: print(','.join(str(v) for v in o.values()))
agg([r for r in rows if r['body']!='SAU6'],'claremont')
agg([r for r in rows if r['body']=='SAU6'],'sau6')
