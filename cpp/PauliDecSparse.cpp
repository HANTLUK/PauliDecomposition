#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <iomanip>
#include <complex>
#include <stdio.h>
#include <chrono>
#include <time.h>
#include <random>

using namespace std;
using namespace std::chrono;
typedef complex<double> dcomp;

void PauliDecSparse(dcomp** Matrix, int dim, string PauliStringInit = "") {
	// Matrix 2^dim dimensional square matrix
	// dim number of qubit dimension
  // PauliStringInit for recursion
  const string PauliNames[4] = {"1","X","Y","Z"};
	string Decomposition;
	int i, k;
  int matDim = pow(2,dim);
  int subMatDim = pow(2,dim-1);
  dcomp factor;
	// If dimension is zero, finish
    if (dim == 0) {
        factor = Matrix[0][0];
        return;
	}

	// Get Partial Matrices
	// Forming Partial Traces
	dcomp*** partialMatrices = 0;
	partialMatrices = new dcomp**[4];
	for (i = 0; i < 4; i++) {
        partialMatrices[i] = new dcomp*[subMatDim];
        for (k = 0; k < subMatDim; k++) {
            partialMatrices[i][k] = new dcomp[subMatDim];
        }
    }
    bool nonZeros[4] = {0,0,0,0};

    for (i = 0; i < subMatDim; i++) {
        for (k = 0; k < subMatDim; k ++) {
                partialMatrices[0][i][k] = 0.5*(Matrix[subMatDim+i][subMatDim+k] + Matrix[i][k]); // 1
                partialMatrices[1][i][k] = 0.5*(Matrix[i][subMatDim+k] + Matrix[subMatDim+i][k]); // X
                partialMatrices[2][i][k] = complex(0.0,1.0)*0.5*(Matrix[i][subMatDim+k] - Matrix[subMatDim+i][k]); // Y
                partialMatrices[3][i][k] = 0.5*(Matrix[i][k] - Matrix[subMatDim+i][subMatDim+k]); // Z
                for (int j = 0; j< 4; j++) {
                    if (partialMatrices[j][i][k] != complex(0.0,0.0)) {
                        nonZeros[j] = 1;
                    }
                }
		}
	}
    // Recursively Decompose in Smaller Dimensions
    for (i = 0; i < 4; i++) {
        if (nonZeros[i] == 1) {
            PauliDec(partialMatrices[i],dim-1,PauliStringInit+PauliNames[i]);
        }
    }
    return;
}
