#!/bin/bash

if [ $USER == easonshi ]
then 
    echo Hello easonshi!
fi

case $USER in 
rich | barbara)
    echo Not allowed!;;
easonshi)
    echo Welcome, $USER
    echo hello;;
esac