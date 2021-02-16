BASEDIR=$(dirname "$0")
cd $BASEDIR
cd ..

while :
do
  git checkout master
  git pull origin master
  sleep 15s
done

