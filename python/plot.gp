set term cairolatex pdf size 8.5cm,5.8cm color colortext font ",8"

set decimalsign "." # für den input
#               Style
# !!!___________________________ !!!
set grid xtics
set grid ytics
set grid mxtics
set grid mytics
set style line 80 linetype 1 linecolor rgb "#888888"
set style line 81 linetype 1 linecolor rgb "#808080" linewidth 0.5
set border back linestyle 80
set grid back linestyle 81
set xtics textcolor rgb "#808080"
set ytics textcolor rgb "#808080"
set y2tics textcolor rgb "#808080"

set linetype 1 lc rgb '#ffcc11' # blue
set linetype 2 lc rgb '#886611' # purple-blue
set linetype 3 lc rgb '#11ccff' # purple
set linetype 4 lc rgb '#113388' # purple
set linetype 5 lc rgb '#cc11ff' # magenta
set linetype 6 lc rgb '#661188' # red
set linetype 7 lc rgb '#448822' # orange
set linetype 8 lc rgb '#ccff11' # orange
set linetype cycle 8

set key autotitle columnheader
set key outside below
set key spacing 1.5
set key font ",8"
set key samplen 1

set xlabel ""
set ylabel "Execution Time $s$"

set xrange [1.5:*]
set yrange [0.0001:*]

set logscale y
set format y "$10^{%T}$"

set nokey

# !!!_______________________________________________!!!
#				Random Matrix Plot

set term cairolatex pdf size 8.5cm,5.2cm color colortext font ",8"
set output "Figures/rand.tex"

set xlabel "Number of Qubits $n$"

set title "Random Matrix"
stats 'Random Matrix.dat' using 0 nooutput
plot for [i=0:(STATS_blocks - 1)] 'Random Matrix.dat' using 1:2:3 index i with errorlines pt 1 ps 1.2 lw 4

# !!!_______________________________________________!!!
#				Unit Matrix Plot
set output "Figures/unit.tex"

set xlabel ""
set ylabel ""

set term cairolatex pdf size 8.5cm,5.8cm color colortext font ",8"

set key autotitle columnheader
set key outside below
set key spacing 1.5
set key font ",8"
set key samplen 1

set title "Unit Matrix"
stats 'Unit Matrix.dat' using 0 nooutput
plot for [i=0:(STATS_blocks - 1)] 'Unit Matrix.dat' using 1:2:3 index i with errorlines pt 1 ps 1.2 lw 4

# !!!_______________________________________________!!!
#				Diagonal Matrix Plot
set output "Figures/diag.tex"

set ylabel "Execution Time $s$"

set key autotitle columnheader
set key outside below
set key spacing 1.5
set key font ",8"
set key samplen 1

set title "Diagonal Matrix"
stats 'Diagonal Matrix.dat' using 0 nooutput
plot for [i=0:(STATS_blocks - 1)] 'Diagonal Matrix.dat' using 1:2:3 index i with errorlines pt 1 ps 1.2 lw 4

# !!!_______________________________________________!!!
#				Sparse Matrix Plot
set output "Figures/spars.tex"

set xlabel "Number of Qubits $n$"
set ylabel ""
set nokey

set term cairolatex pdf size 8.5cm,5.2cm color colortext font ",8"

set title "Sparse Matrix"
stats 'Sparse Matrix.dat' using 0 nooutput
plot for [i=0:(STATS_blocks - 1)] 'Sparse Matrix.dat' using 1:2:3 index i with errorlines pt 1 ps 1.2 lw 4

# !!!_______________________________________________!!!
#				Symmetric Matrix Plot

set term cairolatex pdf size 8.5cm,5.8cm color colortext font ",8"
set output "Figures/symm.tex"

set xlabel ""
set ylabel "Execution Time $s$"

set key autotitle columnheader
set key outside below
set key spacing 1.5
set key font ",8"
set key samplen 1

set title "Symmetric Matrix"
stats 'Symmetric Matrix.dat' using 0 nooutput
plot for [i=0:(STATS_blocks - 1)] 'Symmetric Matrix.dat' using 1:2:3 index i with errorlines pt 1 ps 1.2 lw 4

# !!!_______________________________________________!!!
#				Hermitian Matrix Plot
set output "Figures/herm.tex"

set ylabel ""

set key autotitle columnheader
set key outside below
set key spacing 1.5
set key font ",8"
set key samplen 1

set title "Hermitian Matrix"
stats 'Hermitian Matrix.dat' using 0 nooutput
plot for [i=0:(STATS_blocks - 1)] 'Hermitian Matrix.dat' using 1:2:3 index i with errorlines pt 1 ps 1.2 lw 4

# !!!_______________________________________________!!!

#				TFIM Hamiltonian Matrix Plot
set output "Figures/tfim.tex"

set xlabel "Number of Qubits $n$"
set ylabel "Execution Time $s$"

set nokey

set term cairolatex pdf size 8.5cm,5.2cm color colortext font ",8"

set title "TFIM Hamiltonian"
stats 'TFIM Hamiltonian.dat' using 0 nooutput
plot for [i=0:(STATS_blocks - 1)] 'TFIM Hamiltonian.dat' using 1:2:3 index i with errorlines pt 1 ps 1.2 lw 4
