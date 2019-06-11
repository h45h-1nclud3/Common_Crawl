# Common_Crawl
A small script that searches and downloads pages from http://commoncrawl.org

The script takes a domain name as a parameter then searches in http://commoncrawl.org and download the pages loacally


Note: to get the index list from http://index.commoncrawl.org/ i used a little bash hack 
1- copy all text in the page to a file
2- cat indexes.txt | cut -d" " -f1 | cut -d"-" -f3,4
3- copy the output and open python terminal
4- s= """ put output here between the triple quotes """
5- l = s.split("\n")
6- print l
7- copy the list except the first element and put it in the script

Usage:

python search.py domain.com
