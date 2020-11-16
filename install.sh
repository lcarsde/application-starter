#!/bin/bash

echo ""
echo "=========================================="
echo "lcarsde application starter installation"
echo "=========================================="
echo ""
echo "This program requires:"
echo "* Python 3.8"
echo "* Python 3 PyGObject"
echo ""

cp ./src/lcarsde-application-starter.py /usr/bin/lcarsde-application-starter.py
cp -R ./resources/usr/* /usr/
