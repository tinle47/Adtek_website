#!/bin/bash
# runlh.sh <mode> <runs> <name:path>...   mode=orig|opt (máy chủ giả lập) hoặc live (website thật, kết nối trực tiếp)
S=$(dirname $(readlink -f $0)); MODE=$1; RUNS=$2; shift 2
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
mkdir -p $S/res $S/profiles
if [ "$MODE" != live ]; then
  [ -f $S/srv.pid ] && kill $(cat $S/srv.pid) 2>/dev/null; sleep 0.5
  node $S/server.mjs $MODE > $S/server-$MODE.log 2>&1 & echo $! > $S/srv.pid
  sleep 1
  MAP=(--host-resolver-rules="MAP adtek.agency 127.0.0.1")
else
  MAP=()
fi
for spec in "$@"; do n=${spec%%:*}; p=${spec#*:}
  for r in $(seq 1 $RUNS); do
    prof=$(mktemp -d -p $S/profiles)
    $CHROME --headless=new --no-sandbox --ignore-certificate-errors --remote-debugging-port=9333 --user-data-dir=$prof \
      "${MAP[@]}" --proxy-server=$HTTPS_PROXY --proxy-bypass-list=adtek.agency about:blank >/dev/null 2>&1 & cpid=$!
    sleep 2
    timeout 200 $S/lh/node_modules/.bin/lighthouse "https://adtek.agency$p" --port=9333 --quiet --only-categories=performance --form-factor=mobile \
      --output=json --output-path=$S/res/$MODE-$n-$r.json >/dev/null 2>>$S/res/err.txt || echo "fail $MODE $n $r"
    kill $cpid; wait $cpid 2>/dev/null
  done
done
[ "$MODE" != live ] && kill $(cat $S/srv.pid)
exit 0
