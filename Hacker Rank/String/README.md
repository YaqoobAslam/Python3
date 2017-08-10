Sherlock and the Valid String
fileName: sherlock.py

Sherlock considers a string, , to be valid if either of the following conditions are satisfied:
1. All characters in  have the same exact frequency (i.e., occur the same number of times). For example,  is valid, but  is not valid.
2. Deleting exactly  character from  will result in all its characters having the same frequency. For example,  and  are valid because all their letters will have the same frequency if we remove occurrence of c, but  is not valid because we'd need to remove  characters.
Given , can you determine if it's valid or not? If it's valid, print YES on a new line; otherwise, print NO instead.
Input Format
A single string denoting .
Constraints
* 
* String  consists of lowercase letters only (i.e., [a-z]).
Output Format
Print YES if string  is valid; otherwise, print NO instead.
Sample Input 0
aabbcd
Sample Output 0
NO
Explanation 0
We would need to remove two characters from  to make it valid, because a and b both have a frequency of  and c and d both have a frequency of . This means  is invalid because we'd need to remove more than  character to make all its letters have the same frequency, so we print NO as our answer.

————————————————————————————————————————————————————————


Richie Rich
richieRich.py

Sandy likes palindromes. A palindrome is a word, phrase, number, or other sequence of characters which reads the same backward as it does forward. For example, madam is a palindrome.
On her  birthday, Sandy's uncle, Richie Rich, offered her an -digit check which she refused because the number was not a palindrome. Richie then challenged Sandy to make the number palindromic by changing no more than  digits. Sandy can only change  digit at a time, and cannot add digits to (or remove digits from) the number.
Given  and an -digit number, help Sandy determine the largest possible number she can make by changing digits.
Note: Treat the integers as numeric strings. Leading zeros are permitted and can't be ignored (So 0011 is not a palindrome, 0110 is a valid palindrome). A digit can be modified more than once.
Input Format
The first line contains two space-separated integers,  (the number of digits in the number) and  (the maximum number of digits that can be altered), respectively. 
The second line contains an -digit string of numbers that Sandy must attempt to make palindromic.
Constraints
* 
* 
* Each character  in the number is an integer where .
Output Format
Print a single line with the largest number that can be made by changing no more than  digits; if this is not possible, print -1.
Sample Input 0
4 1
3943
Sample Output 0
3993
Sample Input 1
6 3
092282
Sample Output 1
992299
Sample Input 2
4 1
0011
Sample Output 2
-1
Explanation
Sample 0
There are two ways to make 2943 a palindrome by changing exactly  digits:
1. 3943 —> 3443
2. 3943 —> 3993
3993 > 3443, so we print 3993.

—————————————————————————————————————————————