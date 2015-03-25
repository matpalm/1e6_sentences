# 1e6 sentences dataset

## sample data

1e6 sentence is a simple dataset of a 1,000,000 "clean" sentences from wikipedia...

eg

```
Having heard rumors by way of Jamestown and John Smith, he and his crew decided to try to seek out a Southwest Passage through North America.
The magnitude of buoyant force may be appreciated a bit more from the following argument.
Modbus RTU is a compact, binary representation of the data.
Much of the newer power generation coming online in the last few years is natural gas or combined cycle natural gas plants.
In addition, some illnesses, particularly Circulatory system problems, reduce g-tolerance.
The average household size was 4.39 and the average family size was 4.44.
In the place of reliability, IRT offers the test information function which shows the degree of precision at different values of theta.
```

## corenlp tagging

runs the data through corenlp and emits token, its lemma and pos tag.

```
$ cd parse
$ mvn clean compile assembly:single
$ cat ../sentences.txt \
 | java -d64 -server -Xms25G -Xmx25G -jar ./target/parse-1-jar-with-dependencies.jar \
 > sentences.tagged.tsv
```

```
Public Public NNP	hearings hearing NNS	were be VBD	held hold VBN	in in IN	Salt Salt NNP	Lake Lake NNP City City NNP, , , Denver Denver NNP , , , Phoenix Phoenix NNP , , , Flagstaff Flagstaff NNP , , , Los Los NNP Angeles Angeles NNP , , , San San NNP Francisco Francisco NNP , , , and and CC Washington Washington NNP , , , D.C. D.C. NNP
On on IN      July July NNP	 10 10 CD	, , ,	both both CC forces force NNS faced face VBD each each DT    other other JJin in IN  Kyoto Kyoto NNP   . . .
Monmouth Monmouth NNP	's 's POS   status status NN	as as IN  the the DT	  last last JJ	 dry dry JJ    town town NN	 on on IN    the the DT	 west west NN coast coast NN of of IN the the DT United United NNP States States NNPS was be VBD ended end VBN by by IN a a DT popular popular JJ vote vote NN in in IN the the DT November November NNP2002 2002 CD election election NN . . .
```

## conversion to embeddable vocab

for embeddings we want simple symbolic tokens.

sentences_to_embeddables converts the output from corenlp into a series of space seperated embeddable symbols (ie one embedding per distinct token in this set)

```
$ time cat sentences.tagged.tsv | ./sentences_to_embeddables.py --emit=lemma --strip-CD --add-pos-tag --keep-top=50000 >sentences.lemma.CD.pos.50K.ssv
```

```
$ head sentences.lemma.CD.pos.50K.ssv
the_DT by-census_NN indicate_VBD UNK the_DT UNK DDD_CD population_NN be_VBD UNK to_TO DDD_CD ,_, a_DT reduction_NN UNK a_DT previous_JJ UNK UNK more_JJR UNK DDD_CD DDD_CD ._.
`_`` on_IN the_DT marble_NNP cliffs_NNPS '_POS -lrb-_-LRB- DDD_CD ,_, UNK UNK :_: `_`` UNK UNK marmorklippen_NN '_'' -rrb-_-RRB- use_VBZ UNK to_TO UNK jünger_NNP 's_POS negative_JJ perception_NNS UNK the_DT UNK in_IN UNK 's_POS germany_NNP ._.
homer_NNP UNK description_NN in_IN the_DT `_`` iliad_NNP `_`` homer_NNP ._.
public_NNP hearing_NNS be_VBD hold_VBN in_IN salt_NNP UNK UNK ,_, UNK ,_, phoenix_NNP ,_, flagstaff_NNP ,_, los_NNP angeles_NNP ,_, san_NNP UNK ,_, and_CC washington_NNP ,_, d.c._NNP
```

