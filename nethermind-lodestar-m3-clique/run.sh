docker-compose up -d el

# Wait for EL to be alive
until $(curl --output /dev/null --silent --head --fail http://127.0.0.1:8545); do
    echo "Waiting for EL to be alive..."
    sleep 1
done

docker-compose up -d el cl

# Wait for CL to be alive
until $(curl --output /dev/null --silent --fail http://127.0.0.1:9596/eth/v1/node/health); do
    echo "Waiting for CL to be alive..."
    sleep 1
done

docker-compose up el cl verifier --abort-on-container-exit