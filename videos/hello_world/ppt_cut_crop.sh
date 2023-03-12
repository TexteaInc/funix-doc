# ffmpeg -i ppt_raw.mp4 -filter:v "crop=2510:1550:0:0" -ss 00:00:05 -t 00:00:50  ppt_out.mp4 

# ffmpeg -i 30_seconds.mp4  -vf "fps=10,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" 30_seconds.gif
ffmpeg -i short.mp4  -vf "fps=10,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" short.gif
