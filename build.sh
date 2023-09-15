sudo docker build -q -t musicnbrain/repertoire-backend . -q
sudo docker run -q -d -p 5001:5001 --name repertoire-backend musicnbrain/repertoire-backend
