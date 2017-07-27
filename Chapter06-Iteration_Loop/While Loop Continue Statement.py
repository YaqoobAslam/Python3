import math

while True:
    line = input('> ')
    if line[0] =='#':
        continue
    if line =='done':
        break
    print(line)
print("Done!")

output:
> hello
hello
> eveyone
eveyone
> good
good
> bye
bye
> done
Done!