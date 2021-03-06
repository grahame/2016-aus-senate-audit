# 2016-aus-senate-audit

This repository supports the possible auditing of the 2016 Australian
Senate elections.

This work is joint with Vanessa Teague (U. Melbourne), Philip Stark (UC Berkeley),
Zara Perumal (MIT), Berj K Chilingirian (MIT),
Ian Gordon (U. Melbourne), Damjan Vukcevic, and
Ronald L. Rivest (MIT).

One approach we plan to explore is the 
["Bayesian audit"](http://people.csail.mit.edu/rivest/pubs.html#RS12)
method of Rivest and Shen.

Another family of approaches we may explore are the "black-box auditing" methods
developed by Stark and Rivest (unpublished, although mentioned in
[this talk](http://people.csail.mit.edu/rivest/pubs.html#Riv16x)).
These are ballot-polling methods (not comparison audits).  
These approaches can use a variety of methods for computing "variant samples",
since as a Polya's Urn approach, or the
method developed by Rivest and Yu.

We use with appreciation python [code and
materials](https://github.com/grahame/dividebatur) developed by
Grahame Bowland for computing the outcome of such an election.
Some output from his program can be found
[here](https://sirgraha.me/senate2016/).

We also appreciate and use the 
[code and materials](https://github.com/berjc/election-engine)
developed by Berj K Chilingirian, Zara Perumal, and Eric C Huppert as a framework for election auditing.

Further materials related to post-election audits can be found on the
[voting-related web page of Philip B. Stark](https://www.stat.berkeley.edu/~stark/Vote/index.htm).


## Source

Requires python 3

To clone repo with submodules:
```
git clone --recursive  https://github.com/ron-rivest/2016-aus-senate-audit.git 
````
To pull the latest working versions of submodules use:
```
git submodule foreach git pull origin master
```

