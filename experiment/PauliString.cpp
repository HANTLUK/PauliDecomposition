#include <string>
#include <cmath>
#include <complex>

using namespace std;
typedef complex<double> dcomp;

class PauliString {
	public:
		dcomp Factor;
		string String;
		PauliString() {}
		PauliString(dcomp prefactor, string PauliStr) {
			String = PauliStr;
			Factor = Prefactor;
		}
};
