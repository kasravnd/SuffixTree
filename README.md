## This module is an optimized implementation of Ukkonen's suffix tree algorithm in python. Aiming to support the important text processing functionalities such as:


### Search for strings:
  `✓` Check if a string ***P*** of length ***m*** is a substring in ***O(m)*** time.  
  `✓` Find the first occurrence of the patterns ***P1,... ,Pq*** of total length ***m*** as substrings in ***O(m)*** time.
  
  `✓` Find all ***z*** occurrences of the patterns ***P1,... ,Pq*** of total length ***m*** as substrings in ***O(m+z)*** time.
  - Search for a regular expression P in time expected sublinear in ***n***
  - Find for each suffix of a pattern ***P*** the length of the longest match between a prefix of ***P[i... m]*** and a substring in ***D*** in ![image](https://cloud.githubusercontent.com/assets/5694520/22856327/5881bd04-f0a4-11e6-9d9a-e01fc0c15dd2.png) time. This is termed the matching statistics for ***P***
 
### Find properties of the strings:
  - Find the longest common substrings of the string ***Si*** and ***Sj*** in ![image](https://cloud.githubusercontent.com/assets/5694520/22856331/72a43c66-f0a4-11e6-8f06-4c8ea987c79c.png) time.
  - Find all maximal pairs, maximal repeats or supermaximal repeats in ![image](https://cloud.githubusercontent.com/assets/5694520/22856334/861ff74e-f0a4-11e6-9ff7-9629c4d1d69b.png) time.
  - Find the Lempel–Ziv decomposition in ![image](https://cloud.githubusercontent.com/assets/5694520/22856287/8bdbe630-f0a3-11e6-8611-de6c0a40932c.png) time.[10]
  - Find the longest repeated substrings in ![image](https://cloud.githubusercontent.com/assets/5694520/22856287/8bdbe630-f0a3-11e6-8611-de6c0a40932c.png) time.
  - Find the most frequently occurring substrings of a minimum length in ![image](https://cloud.githubusercontent.com/assets/5694520/22856287/8bdbe630-f0a3-11e6-8611-de6c0a40932c.png) time.
  - Find the shortest strings from ![image](https://cloud.githubusercontent.com/assets/5694520/22856282/7e4d4fe0-f0a3-11e6-915e-1c9dfcd679bf.png)  that do not occur in ***D*** in ***O(n+z)*** time, if there are ***z*** such strings.
  - Find the shortest substrings occurring only once in ![image](https://cloud.githubusercontent.com/assets/5694520/22856287/8bdbe630-f0a3-11e6-8611-de6c0a40932c.png) time.
  - Find, for each ***i*** the shortest substrings of ***Si*** not occurring elsewhere in ***D*** in ![image](https://cloud.githubusercontent.com/assets/5694520/22856287/8bdbe630-f0a3-11e6-8611-de6c0a40932c.png) time.

## sources:

  - http://web.stanford.edu/~mjkay/gusfield.pdf
  - On–line construction of suffix trees. Esko Ukkonen
  - http://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-6/ 
