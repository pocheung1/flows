#!/bin/bash

sudo apt-get update
sudo wget -qO- https://go.dev/dl/go1.22.2.linux-amd64.tar.gz | sudo tar xvz -C /usr/local

export GOROOT=/usr/local/go
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH

echo
go version
