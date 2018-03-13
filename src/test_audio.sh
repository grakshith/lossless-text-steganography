#! /bin/bash

echo "1. Testing audio steganography"
python2 secret_message.py << EOF
1
This text is embedded
cover_audio/violin2.wav
EOF
echo "";
echo "Press enter to retrieve"
read
echo "Retrieving the message now"
echo "";

python2 retrieve_message.py <<< stego_audio/violin2.wav

echo "";
echo "";
read
echo "2. Testing audio steganography"
python2 secret_message.py << EOF
1
Hello world
cover_audio/guitar.wav
EOF
echo "";
echo "Press enter to retrieve"
read
echo "Retrieving the message now"
echo "";


python2 retrieve_message.py <<< stego_audio/guitar.wav
