#/bin/bash

echo "./timestamp/timestamp_render.py > timestamp/timestamp.json"
echo "./xchart/xchart_render.py > xchart/xchart.json"
./timestamp/timestamp_render.py > timestamp/timestamp.json
./xchart/xchart_render.py > xchart.js
