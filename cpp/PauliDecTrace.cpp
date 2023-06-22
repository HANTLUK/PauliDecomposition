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

void PauliDec(dcomp** Matrix, int dim, string PauliStringInit = "", dcomp** MatInit = {{dcomp(0.0,0.0)}}, int iter = 0) {
	// Matrix 2^dim dimensional square matrix
	// dim number of qubit dimension
  // PauliStringInit for recursion
  const string PauliNames[4] = {"1","X","Y","Z"};
	string Decomposition;
	int i, k;
  int matDim = pow(2,dim);
  int subMatDim = pow(2,dim-1);
  dcomp factor;
	// If size is reached compute trace
  if (iter >= dim) {
        factor = 0.0; // trace MatInit^* Matrix
        return;
	}
	else {
		if (iter > 1) {
			dcomp** Mat;
			for (j = 0; j < iter; j++) {

			}
		} else {
			return;
		}
	}
  return;
}

dcomp** RandomComplexMatrix(int dim) {
    double lower_bound = -1;
    double upper_bound = 1;
    uniform_real_distribution<double> unif(lower_bound,upper_bound);
    default_random_engine re;
	dcomp** RandomMatrix = 0;
	int j, k;
    int matDim = pow(2,dim);
    RandomMatrix = new dcomp*[matDim];
    for (j = 0; j < matDim; j++) {
        RandomMatrix[j] = new dcomp[matDim];
        for (k = 0; k< matDim; k++) {
            RandomMatrix[j][k] = complex( unif(re), unif(re));
		}
	}
	return RandomMatrix;
}

dcomp** RandomDiagMatrix(int dim) {
    double lower_bound = -1;
    double upper_bound = 1;
    uniform_real_distribution<double> unif(lower_bound,upper_bound);
    default_random_engine re;
    dcomp** RandomMatrix = 0;
    int j, k;
    int matDim = pow(2,dim);
    RandomMatrix = new dcomp*[matDim];
    for (j = 0; j < matDim; j++) {
        RandomMatrix[j] = new dcomp[matDim];
        RandomMatrix[j][j] = complex( unif(re), unif(re));
    }
    return RandomMatrix;
}

dcomp** IdentityMatrix(int dim) {
    dcomp** RandomMatrix = 0;
    int j, k;
    int matDim = pow(2,dim);
    RandomMatrix = new dcomp*[matDim];
    for (j = 0; j < matDim; j++) {
        RandomMatrix[j] = new dcomp[matDim];
        RandomMatrix[j][j] = complex( 1.0, 0.0);
    }
    return RandomMatrix;
}

dcomp** SparseMatrix(int dim) {
    double lower_bound = -1;
    double upper_bound = 1;
    uniform_real_distribution<double> unif(lower_bound,upper_bound);
    default_random_engine re;
    random_device rd; // obtain a random number from hardware
    mt19937 gen(rd()); // seed the generator
    uniform_int_distribution<> distr(0, dim); // define the range
    dcomp** RandomMatrix = 0;
    int j, k, i;
    int matDim = pow(2,dim);
    RandomMatrix = new dcomp*[matDim];
    for (j = 0; j < matDim; j++) {
        RandomMatrix[j] = new dcomp[matDim];
    }
    for (j = 0; j < 0.25*pow(matDim,2); j++) {
        k = distr(gen);
        i = distr(gen);
        RandomMatrix[k][i] = complex( unif(re), unif(re));
    }
    return RandomMatrix;
}

int main() {
    int maxDim = 12;
        double difs[maxDim];
        double dif;
    printf("Random: \n");
    for (int dim = 1; dim < maxDim+1; dim++) {
        dcomp** Matrix = RandomComplexMatrix(dim);

        auto start = high_resolution_clock::now();
        PauliDec(Matrix,dim);
        auto stop = high_resolution_clock::now();

        auto duration = duration_cast<microseconds>(stop - start);
        dif = 0.00000001*duration.count();
        difs[dim-1] = dif;
        printf ("%.15f, ", dif );
    }
    printf("Diagonal: \n");
    for (int dim = 1; dim < maxDim+1; dim++) {
        dcomp** Matrix = RandomDiagMatrix(dim);

        auto start = high_resolution_clock::now();
        PauliDec(Matrix,dim);
        auto stop = high_resolution_clock::now();

        auto duration = duration_cast<microseconds>(stop - start);
        dif= 0.00000001*duration.count();
        difs[dim-1] = dif;
        printf ("%.15f, ", dif );
    }
    printf("Identity: \n");
    for (int dim = 1; dim < maxDim+1; dim++) {
        dcomp** Matrix = IdentityMatrix(dim);

        auto start = high_resolution_clock::now();
        PauliDec(Matrix,dim);
        auto stop = high_resolution_clock::now();

        auto duration = duration_cast<microseconds>(stop - start);
        dif= 0.00000001*duration.count();
        difs[dim-1] = dif;
        printf ("%.15f, ", dif );
    }

    printf("Sparse: \n");
    for (int dim = 1; dim < maxDim+1; dim++) {
        dcomp** Matrix = SparseMatrix(dim);

        auto start = high_resolution_clock::now();
        PauliDec(Matrix,dim);
        auto stop = high_resolution_clock::now();

        auto duration = duration_cast<microseconds>(stop - start);
        dif= 0.00000001*duration.count();
        difs[dim-1] = dif;
        printf ("%.15f, ", dif );
    }
    return 0;
}
