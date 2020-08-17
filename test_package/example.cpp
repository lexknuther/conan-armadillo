#include <armadillo>
#include <iostream>

int main() {
	auto A{arma::randu<arma::mat>(4, 5)};
	auto B{arma::randu<arma::mat>(4, 5)};

	std::cout << A * B.t() << std::endl;
	return 0;
}
