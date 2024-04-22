
if [ -d "model/" ] ; then
    echo "model installed already!"
    exit
fi
echo "missing model; installing"
wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip -P model
cd model
echo "unzipping"
unzip vosk-model-en-us-0.22-lgraph.zip.zip
rm -f vosk-model-en-us-0.22-lgraph.zip.zip

echo "done!"