#!/usr/bin/env python
import sys, optparse
from collections import Counter

optparser = optparse.OptionParser(prog='gen_vocab', description='generate a vocab from 1e6_sentences parsed data')
optparser.add_option('--emit', None, dest='emit', type='string', default="token", help='emit either [token] or [lemma]')
optparser.add_option('--add-pos-tag', None, action="store_true", dest='add_pos_tag', help='if true prepend each token/lemma with "_[postag]"')
optparser.add_option('--preserve-case', None, action="store_true", dest='preserve_case', help='keep case of token or lemma. dft is to lowercase')
optparser.add_option('--strip-CD', None, action="store_true", dest='strip_cd', help='if set then replace all tokens of type "CD" with DDD')
optparser.add_option('--keep-top', None, dest='keep_top', default=None, type='int', help='if set only keep top N tokens (by freq). other replaced with UNK')

opts, arguments = optparser.parse_args()
print >>sys.stderr, opts
if opts.emit not in ["token", "lemma"]: 
    raise Exception("unknown --emit option")
if opts.keep_top and opts.keep_top < 0:
    raise Exception("--keep-top must be non negative")

emit_token = opts.emit == "token"

# parse over all data converting tokens to potential embeddable forms
freqs = Counter()
records = []
for n, line in enumerate(sys.stdin):
    if (n%10000)==0: print >>sys.stderr, "reading", n
    record = []
    for triple in line.strip().split("\t"):
        token, lemma, pos_tag = triple.split(" ")
        emit_str = token if emit_token else lemma
        if not opts.preserve_case: 
            emit_str = emit_str.lower()
        if pos_tag == 'CD' and opts.strip_cd:
            emit_str = "DDD" 
        if opts.add_pos_tag:
            emit_str = "%s_%s" % (emit_str, pos_tag)
        record.append(emit_str)
        freqs[emit_str] += 1
    records.append(record)

# build white list based on topN most frequent.
whitelist = None
if opts.keep_top:
    whitelist = set()
    for token, _freq in freqs.most_common(opts.keep_top):
        whitelist.add(token)
    print >>sys.stderr, "whitelist has", len(whitelist), "items,", opts.keep_top, "requested"

# reemit
stats = Counter()
for n, record in enumerate(records):
    if (n%10000)==0: print >>sys.stderr, "writing", n
    output = []
    for token in record:
        if not whitelist or token in whitelist:
            output.append(token)
            stats['emit_token'] += 1
        else:
            # ("FL_%s" % token) for UNK hashing
            output.append("UNK")  
            stats['emit_UNK'] += 1
    print " ".join(output)
print >>sys.stderr, stats


