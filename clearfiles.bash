#!/usr/bin/env bash

cd MoviebookAPI

rm *.pyc
rm *.py~
rm -rf __pycache__
cd ..
cd userprofiles

rm *.pyc
rm *.py~
rm -rf migrations
rm -rf __pycache__

cd ..
cd posts

rm *.pyc
rm *.py~
rm -rf migrations
rm -rf __pycache__

cd ..
cd movies

rm *.pyc
rm *.py~
rm -rf migrations
rm -rf __pycache__
