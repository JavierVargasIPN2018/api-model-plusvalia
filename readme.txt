docker build -t mlplusvalia-api .
    docker run -d -p 3016:8000 --name mlplusvalia mlplusvalia-api