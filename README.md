# Pagerank
## Python implementation of the PageRank algorithm using sampling and iteration methods.

## Overview

This project implements the PageRank algorithm, the  algorithm used by Google Search, using Python.  
It demonstrates both sampling (random surfer model) and iterative algorithm methods to estimate the relative importance of web pages based on their link structures.

Random Surfer Model: Sampling method simulates a random surfer moving between pages based on link probabilities and a damping factor.
Iterative Algorithm: The Iterative method repeatedly updates PageRank values across all pages until they converge to stable probabilities

## pagerank/
 pagerank.py       # Your main Python code implementing PageRank
 corpus          # FolderS containing HTML files (the web pages to analyse)
 README.md         # This documentation file

## Installation
This project uses only Python standard libraries

## usage
python pagerank.py corpus


## How the code works
Crawl → Reads HTML files in the corpus and extracts links.

Transition Model → Creates a probability distribution for moving between pages using a damping factor.

Sampling Method → Estimates PageRank by simulating a “random surfer” over many iterations.

Iterative Method → Updates PageRank values repeatedly until they converge.

## References
CS50AI project Pagerank
