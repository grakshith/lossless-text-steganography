#! /bin/bash

echo "1. Testing test steganography"
python2 secret_message.py << EOF
2
This text is embedded
cover_text/cricket.txt
EOF
echo "";
echo "Press enter to de-embed"
read
echo "De-embedding the text now"
echo "";

python2 deembed_text.py <<< stego_text/cricket.txt
echo "Press enter to view the two files"
read
echo "Cover text : cover_text/cricket.txt"
cat cover_text/cricket.txt
echo  ""; echo "";
echo "Stego text : stego_text/cricket.txt"
cat stego_text/cricket.txt
echo ""; echo "";
read
echo "2. Testing test steganography"
python2 secret_message.py << EOF
2
Hello world
cover_text/ddn.txt
EOF
echo "";
echo "Press enter to de-embed"
read
echo "De-embedding the text now"
echo "";


python2 deembed_text.py <<< stego_text/ddn.txt
echo "Press enter to view the two files"
read
echo "Cover text : cover_text/cricket.txt"
cat cover_text/ddn.txt
echo  ""; echo "";
echo "Stego text : stego_text/cricket.txt"
cat stego_text/ddn.txt