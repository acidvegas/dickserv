import glob, os
with open('list.txt', 'w') as ascii_file:
    count = 1
    for i in glob.glob('ascii/*.txt'):
        ascii_file.write('%d. %s\n' % (count, os.path.basename(i).replace('.txt', '', 1)))
        count += 1
