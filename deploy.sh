#!/bin/bash
echo 
echo "##############################"
echo "Deploying new version of branch" 
git branch | grep "*"
echo "##############################"
echo 
git log -n 1 | head -1 >templates/version.txt

echo last commit
cat templates/version.txt
echo

appcfg.py update ../Viaggiare-Nel-Pollino/ -e robcos@robcos.com
