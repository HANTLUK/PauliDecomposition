import numpy as np
from math import isclose

class PauliString:
    pass

Union = list

class PauliString:
    """
    A class representing Pauli strings and simple operations on them

    ...

    Attributes
    ----------
    pauli_list : list 
        an ordered list containing the Paulis as strings
    prefactor : np.cdouble
        the prefactor of the Pauli string

    Methods
    -------
    __bool__() -> bool
        returns prefactor as a bool
    __len__() -> int
        returns length of the list of Paulis
    __abs__() -> PauliString
        returns an instance of PauliString whose prefactor is the absolute value of the former
    __eq__(second_string: PauliString) -> bool
        returns True if and only if the two Pauli strings have matching lists of Paulis and prefactors
    __mul__(other: Union[int, float, complex, PauliString]) -> PauliString
        returns the scalar multiplication or the componentwise product of two Pauli strings as a new instance of the class PauliString
    __rmul__(other: Union[int, float, complex, PauliString]) -> PauliString
        returns the scalar multiplication or the componentwise product of two Pauli strings as a new instance of the class PauliString
    dagger()
        changes the Pauli string to its transposed complex conjugated by complex conjugating the prefactor
    com(second_string: PauliString) -> PauliString
        returns the commutator of two Pauli strings as a new instance of class PauliString
    anticom(second_string: PauliString) -> PauliString
        returns the anticommutator of two Pauli strings as a new instance of class PauliString
    """

    def __init__(self, pauli_list: list[str], prefactor: np.cdouble):
        if not pauli_list:
            raise ValueError("Input list must not be empty.")
        if not all(element in {'id', 'x', 'y', 'z'} for element in list(pauli_list)):
            raise ValueError("Input list contains invalid strings.")
        if not isinstance(prefactor, (int, float, complex)):
            raise TypeError(f"Expected input prefactor to be a single number, but received {type(prefactor)}")
        self._pauli_list = list(pauli_list)
        self._prefactor = np.cdouble(prefactor)

    @property
    def pauli_list(self) -> list[str]:
        return self._pauli_list

    @pauli_list.setter
    def pauli_list(self, new_pauli_list: list[str]):
        if len(new_pauli_list) != len(self._pauli_list):
            raise ValueError("New list should have the same length as the old list.")
        if not all(element in {'id', 'x', 'y', 'z'} for element in new_pauli_list):
            raise ValueError("Input list contains invalid strings.")
        self._pauli_list = new_pauli_list

    @property
    def prefactor(self) -> np.cdouble:
        return self._prefactor

    @prefactor.setter
    def prefactor(self, new_prefactor : np.cdouble):
        if not isinstance(new_prefactor, (int, float, complex)):
            raise TypeError(f"Expect input prefactor to be a single number, but received {type(prefactor)}.")
        self._prefactor = np.cdouble(new_prefactor)

    def __bool__(self) -> bool:
        """Returns prefactor as a bool"""
        return not (isclose(self.prefactor.real, 0.0, abs_tol=1e-16) and isclose(self.prefactor.imag, 0.0, abs_tol=1e-16))

    def __len__(self) -> int:
        """Returns length of the list of Paulis"""
        return len(self.pauli_list)

    def __abs__(self) -> PauliString:
        """Returns an instance of PauliString whose prefactor is the absolute value of the former"""
        return PauliString(self.pauli_list, abs(self.prefactor))

    def __eq__(self, second_string: PauliString) -> bool:
        """Returns True if and only if the two Pauli strings have matching lists of Paulis and prefactors

        Parameters
        ----------
        second_string: PauliString

        """
        if not isinstance(second_string, PauliString):
            return False
        return self.pauli_list == second_string.pauli_list and isclose(self.prefactor.real, second_string.prefactor.real, abs_tol=1e-16) and isclose(self.prefactor.imag, second_string.prefactor.imag, abs_tol=1e-16)

    def __mul__(self, other: Union[int, float, complex, PauliString]) -> PauliString:
        """Returns the scalar multiplication or the componentwise product of two Pauli strings as a new instance of the class PauliString

        Implements the multiplication operation "*" on the class PauliString. Multiplying with a single number just changes the prefactor.
        A product of two Pauli strings s1, s2 can be computed by either calling the method s1.__mul__(s2) on either of the Pauli strings
        or by entering s1 * s2. The output is another instance of the class PauliString. The product of two Paulis is computed 
        componentwisely for each qubit they act on and the prefactors are multiplied.

        Parameters
        ----------
        other: Single number or PauliString

        """
        if isinstance(other, (int, float, complex)):
            return PauliString(self.pauli_list, self.prefactor * other)

        elif isinstance(other, PauliString):
            if len(self) != len(other):
                raise ValueError("Both multiplicands should have the same length.")
            new_pauli_list = []
            new_prefactor = self.prefactor * other.prefactor

            for i in range(len(self)):
                if self.pauli_list[i] == 'id':
                    new_pauli_list.append(other.pauli_list[i])

                elif self.pauli_list[i] == 'x':
                    if other.pauli_list[i] == 'id':
                        new_pauli_list.append('x')

                    elif other.pauli_list[i] == 'x':
                        new_pauli_list.append('id')

                    elif other.pauli_list[i] == 'y':
                        new_pauli_list.append('z')
                        new_prefactor *= 1j

                    elif other.pauli_list[i] == 'z':
                        new_pauli_list.append('y')
                        new_prefactor *= -1j

                elif self.pauli_list[i] == 'y':
                    if other.pauli_list[i] == 'id':
                        new_pauli_list.append('y')

                    elif other.pauli_list[i] == 'x':
                        new_pauli_list.append('z')
                        new_prefactor *= -1j

                    elif other.pauli_list[i] == 'y':
                        new_pauli_list.append('id')

                    elif other.pauli_list[i] == 'z':
                        new_pauli_list.append('x')
                        new_prefactor *= 1j

                else:
                    if other.pauli_list[i] == 'id':
                        new_pauli_list.append('z')

                    elif other.pauli_list[i] == 'x':
                        new_pauli_list.append('y')
                        new_prefactor *= 1j

                    elif other.pauli_list[i] == 'y':
                        new_pauli_list.append('x')
                        new_prefactor *= -1j

                    elif other.pauli_list[i] == 'z':
                        new_pauli_list.append('id')

            return PauliString(new_pauli_list, new_prefactor)

        else:
            raise TypeError(f"Expect multiplicand to be either a single number or a PauliString, but received {type(other)}.")

    def __rmul__(self, other: Union[int, float, complex, PauliString]) -> PauliString:
        """Returns the scalar multiplication or the componentwise product of two Pauli strings as a new instance of the class PauliString

        Implements the reverse multiplication operation "*" on the class PauliString. Multiplying with a single number just changes the prefactor.
        A reverse product of two Pauli strings s1, s2 can be computed by either calling the method s1.__rmul__(s2) on either of the Pauli strings
        or by entering s2 * s1. The output is another instance of the class PauliString. The product of two Paulis is computed componentwisely
        for each qubit they act on and the prefactors are multiplied.

        Parameters
        ----------
        other: Single number or PauliString

        """
        if isinstance(other, (int, float, complex)):
            return PauliString(self.pauli_list, self.prefactor * other)

        elif isinstance(other, PauliString):
            if len(self) != len(other):
                raise ValueError("Both multiplicands should have the same length.")
            new_pauli_list = []
            new_prefactor = self.prefactor * other.prefactor

            for i in range(len(self)):
                if other.pauli_list[i] == 'id':
                    new_pauli_list.append(self.pauli_list[i])

                elif other.pauli_list[i] == 'x':
                    if self.pauli_list[i] == 'id':
                        new_pauli_list.append('x')

                    elif self.pauli_list[i] == 'x':
                        new_pauli_list.append('id')

                    elif self.pauli_list[i] == 'y':
                        new_pauli_list.append('z')
                        new_prefactor *= 1j

                    elif self.pauli_list[i] == 'z':
                        new_pauli_list.append('y')
                        new_prefactor *= -1j

                elif other.pauli_list[i] == 'y':
                    if self.pauli_list[i] == 'id':
                        new_pauli_list.append('y')

                    elif self.pauli_list[i] == 'x':
                        new_pauli_list.append('z')
                        new_prefactor *= -1j

                    elif self.pauli_list[i] == 'y':
                        new_pauli_list.append('id')

                    elif self.pauli_list[i] == 'z':
                        new_pauli_list.append('x')
                        new_prefactor *= 1j

                else:
                    if self.pauli_list[i] == 'id':
                        new_pauli_list.append('z')

                    elif self.pauli_list[i] == 'x':
                        new_pauli_list.append('y')
                        new_prefactor *= 1j

                    elif self.pauli_list[i] == 'y':
                        new_pauli_list.append('x')
                        new_prefactor *= -1j

                    elif self.pauli_list[i] == 'z':
                        new_pauli_list.append('id')

            return PauliString(new_pauli_list, new_prefactor)

        else:
            raise TypeError(f"Expect multiplicand to be either a single number or a PauliString, but received {type(other)}.")

    def dagger(self):
        """Changes the Pauli string to its transposed complex conjugated by complex conjugating the prefactor"""
        self.prefactor = np.conjugate(self.prefactor)

    def com(self, second_string: PauliString) -> PauliString:
        """Returns the commutator of two Pauli strings as a new instance of class PauliString

        Since the commutator is bilinear, take both constituents' prefactors and define their product as the temporary prefactor.
        According to the mixed-product property (A ⊗ B)(C ⊗ D) = AC ⊗ BD the emerging Pauli string is 
        proportional to the two strings' multiplication.
        By the property on products of Pauli matrices XY = -YX the subtrahend is (-1)^j times the minuend where j is the number 
        of non-commuting parts in the two Pauli strings. Expressed in simple words, every time the two Paulis on one part do not
        commute, we have an i in the minuend and a -i in the subtrahend. The resulting prefactor is therefore just the difference of the
        multiplication's prefactor and its conjugate (2 times its imaginary part).

        Parameters
        ----------
        second_string: PauliString
        """
        if not isinstance(second_string, PauliString):
            raise TypeError(f"Expect argument to be a PauliString, but received {type(second_string)}.")

        if len(self) != len(second_string):
                raise ValueError("Both Pauli strings should have the same length.")

        temp_prefactor = self.prefactor * second_string.prefactor

        new_string = PauliString(self.pauli_list, 1) * PauliString(second_string.pauli_list, 1)
        new_string.prefactor = 2j * temp_prefactor * new_string.prefactor.imag

        return new_string

    def anticom(self, second_string: PauliString) -> PauliString:
        """Returns the anticommutator of two Pauli strings as a new instance of class PauliString

        Since the anticommutator is bilinear, take both constituents' prefactors and define their product as the temporary prefactor.
        According to the mixed-product property (A ⊗ B)(C ⊗ D) = AC ⊗ BD the emerging Pauli string is 
        proportional to the two strings' multiplication.
        By the property on products of Pauli matrices XY = -YX the subtrahend is (-1)^j times the minuend where j is the number 
        of non-commuting parts in the two Pauli strings. Expressed in simple words, every time the two Paulis on one part do not
        commute, we have an i in the minuend and a -i in the subtrahend. The resulting prefactor is therefore just the difference of the
        multiplication's prefactor and its conjugate (2 times its real part).

        Parameters
        ----------
        second_string: PauliString
        """
        if not isinstance(second_string, PauliString):
            raise TypeError(f"Expect argument to be a PauliString, but received {type(second_string)}.")

        if len(self) != len(second_string):
                raise ValueError("Both Pauli strings should have the same length.")

        temp_prefactor = self.prefactor * second_string.prefactor

        new_string = PauliString(self.pauli_list, 1) * PauliString(second_string.pauli_list, 1)
        new_string.prefactor = 2* temp_prefactor * new_string.prefactor.real

        return new_string
        