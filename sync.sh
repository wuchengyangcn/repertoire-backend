sync=0

cd ~/repertoire-back
git fetch
if git status | grep -q 'is behind'; then
  sync=1
fi

if [ $sync == 1 ]; then
  echo "clean docker"
  sudo docker kill $(sudo docker ps --filter "name=repertoire-backend" -q)
  sudo docker rm $(sudo docker ps --filter "name=repertoire-backend" -q)
  sudo docker rmi $(sudo docker images musicnbrain/repertoire-backend -q)
  sudo docker rmi $(sudo docker images python -q)

  echo "build docker"
  cd ~/repertoire-backend
  ./build.sh
fi

echo "backend sync complete"