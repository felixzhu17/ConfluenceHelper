black . 
git commit -a -m 'minor update'
bumpversion --verbose --current-version 0.0.2 patch
git push
bash update_package.sh


