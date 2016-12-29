#!/bin/bash
# execute 'chmod u+x' to make script executable if on new computer
mongoimport --db jakartaku --collection education --type csv --file education2014_clean.csv --headerline
mongoimport --db jakartaku --collection marriage --type csv --file marriage2015_clean.csv --headerline
mongoimport --db jakartaku --collection religion --type csv --file religion2013_clean.csv --headerline
mongoimport --db jakartaku --collection occupation --type csv --file occupation2013_clean.csv --headerline
mongoimport --db jakartaku --collection demographics --type csv --file demographics2013_clean.csv --headerline