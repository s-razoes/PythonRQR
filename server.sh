echo "Local ip"
cat /etc/hosts|grep -v ::|grep -v localhost
port=8080
echo "Port $port"
echo "Ctrl+C twice or"
echo "Use docker kill <Container Id> to stop"
python3 main.py
