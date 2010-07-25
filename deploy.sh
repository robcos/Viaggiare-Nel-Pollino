#!/bin/bash
echo 
echo "##############################"
echo "Deploying new version of branch" 
git branch | grep "*"
echo "##############################"
echo 


clean=$(git status | grep -c "working directory clean")
[ "$clean" == "1" ] || {
  echo "Commit your changes first"
  exit
}

git log -n 1 | head -1 >templates/version.txt

echo last commit
cat templates/version.txt
echo

python ./sitemap_gen-1.4/sitemap_gen.py  --config=sitemap_gen-1.4/config.xml

appcfg.py update ../Viaggiare-Nel-Pollino/ -e robcos@robcos.com
