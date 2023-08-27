docker build -t musicnbrain/repertoire-backend .
docker run -d -p 5001:5001 --name repertoire-backend musicnbrain/repertoire-backend
