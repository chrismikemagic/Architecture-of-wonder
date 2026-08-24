import re, json, sys
lines = open(sys.argv[1], encoding='utf-8').read().split('\n')
comments = []
page = None
cur = None
col = None
page_text = []   # left column text of current page
page_texts = {}
hdr = re.compile(r'Built for Wonder — Decode Behavior')
pg = re.compile(r'^\s*Page:\s*(\d+)\s*$')
auth = re.compile(r'Author: James Scott\s+Subject: ([A-Za-z ]+?)\s+Date: (.+)$')
def flush():
    global cur
    if cur:
        cur['comment'] = ' '.join(x.strip() for x in cur['comment'] if x.strip())
        comments.append(cur); cur=None
for ln in lines:
    m = pg.match(ln)
    if m:
        flush(); page = int(m.group(1)); page_text=[]; page_texts[page]=page_text; col=None; continue
    if 'file:///' in ln or hdr.search(ln) or ln.strip() in ('‐','fi','') :
        if ln.strip()=='' : pass
        continue
    if 'This page contains no comments' in ln:
        continue
    m = auth.search(ln)
    if m:
        flush()
        col = ln.index('Author:')
        cur = {'page': page, 'kind': m.group(1).strip(), 'date': m.group(2).strip(), 'comment': []}
        left = ln[:col].strip()
        if left: page_text.append(left)
        continue
    if col is not None and len(ln) > col:
        left = ln[:col].strip(); right = ln[col:].strip()
        if left: page_text.append(left)
        if right and cur is not None: cur['comment'].append(right)
    else:
        t = ln.strip()
        if t: page_text.append(t)
flush()
for c in comments:
    c['page_text'] = ' '.join(page_texts.get(c['page'], []))
json.dump(comments, open(sys.argv[2],'w'), indent=1, ensure_ascii=False)
print(len(comments), 'comments;', len(set(c['page'] for c in comments)), 'pages')
with open(sys.argv[3],'w') as f:
    for i,c in enumerate(comments,1):
        f.write(f"### [{i}] p{c['page']} ({c['kind']})\n{c['comment']}\n\n")
