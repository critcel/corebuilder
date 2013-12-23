#!/bin/bash

echo $PWD

for i in $(seq 1 7); do
  echo python corebuild.py --input ${i}x${i}.inp --output final.inp
  python corebuild.py --input ${i}x${i}.inp --output final.inp
  cd ${i}x{i}
  penmshxp
  cd ..
done 
