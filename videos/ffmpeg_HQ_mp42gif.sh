ffmpeg -i table_plot.mp4  -vf "fps=10,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" table_plot.gif
