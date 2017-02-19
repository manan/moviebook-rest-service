#!/usr/bin/env bash

cd MoviebookAPI

rm *.pyc
rm *.py~

cd ..
cd userprofiles

rm *.pyc
rm *.py~
rm -rf migrations

cd ..
cd posts

rm *.pyc
rm *.py~
rm -rf migrations