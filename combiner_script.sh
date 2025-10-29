cd /Users/parsahome/inbox/book_purification_of_the_heart/section_2

for f in *.wav; do echo "file '$PWD/$f'" >> filelist.txt; done
ffmpeg -f concat -safe 0 -i filelist.txt -acodec libmp3lame -b:a 192k combined_output.mp3

