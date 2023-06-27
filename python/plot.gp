set term png

set output "Random Matrix.png"

set key autotitle columnheader

set xrange [0:*]
set yrange [0:*]

set logscale y

set title "Random Matrix"
stats 'Random Matrix.dat' using 0 nooutput
plot for [i=0:(STATS_blocks - 1)] 'Random Matrix.dat' using 1:2:3 index i with errorlines pt 1 lw 2
