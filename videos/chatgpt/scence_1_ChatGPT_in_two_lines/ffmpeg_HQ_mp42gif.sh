# ffmpeg -ss 00:00:44  -to 00:00:53 -i table_plot.mp4  -vf "fps=10,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" table_plot.gif
for name in chatgpt_1 
do
ffmpeg -i $name.mp4  -vf "fps=10,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" $name.gif
done
