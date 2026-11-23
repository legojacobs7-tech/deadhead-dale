#!/bin/bash
# usage: runall.sh ep plan.json outdir
EP=$1; PLAN=$2; OUT=$3
cd /home/claude/deadhead-dale/studio
python3 -c "import json;[print(s['k'],s['n']) for s in json.load(open('$PLAN'))['shots']]" | \
while read k n; do
  d=$OUT/s$(printf %02d $k)
  if [ -f $d/done ]; then continue; fi
  echo "$k $n $d"
done | xargs -P 2 -L 1 bash -c 'mkdir -p $2; python3 '$EP'.py $0 $1 $2 > $2/log.txt 2>&1 && touch $2/done'
echo ALLDONE > $OUT/ALLDONE
