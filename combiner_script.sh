cd /Users/parsahome/inbox/book_NVC/section_3

for f in *.wav; do echo "file '$PWD/$f'" >> filelist.txt; done
ffmpeg -f concat -safe 0 -i filelist.txt -acodec libmp3lame -b:a 192k combined_output.mp3

