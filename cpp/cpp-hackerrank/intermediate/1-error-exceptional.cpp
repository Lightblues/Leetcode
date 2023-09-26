/* 
前置: https://www.hackerrank.com/domains/cpp?filters%5Bskills%5D%5B%5D=C%2B%2B%20%28Basic%29
计划: https://www.hackerrank.com/domains/cpp?filters%5Bskills%5D%5B%5D=C%2B%2B%20%28Intermediate%29

https://www.hackerrank.com/challenges/exceptional-server/problem?isFullScreen=true

C++中的异常类

std::exception：
    这是所有标准库异常类的基类。
    它提供了 what() 函数，用于返回异常的描述信息。
    通常，可以将 std::exception 用作捕获所有异常的基类。
std::logic_error：
    这是逻辑错误的异常类的基类。
    它包含了一些派生类，如 std::invalid_argument、std::domain_error、std::length_error 等。
    这些异常类表示程序中的逻辑错误，如无效的参数、无效的域、超出长度限制等。
std::runtime_error：
    这是运行时错误的异常类的基类。
    它包含了一些派生类，如 std::range_error、std::overflow_error、std::underflow_error 等。
    这些异常类表示运行时错误，如数组越界、算术溢出、下溢等。
std::bad_alloc：
    这是在动态内存分配失败时抛出的异常类。
    当 new 操作符无法分配所需的内存时，会抛出该异常。
除了上述异常类之外，C++ 标准库还提供了其他一些异常类，如 std::bad_cast（在 dynamic_cast 转换失败时抛出）、std::ios_base::failure（在 I/O 操作失败时抛出）等。

通过 `throw std::runtime_error("Some error occurred.");` 的形式来抛出错误

异常处理

try {
    // 可能抛出异常的代码
} catch (const std::exception& e) {
    // 处理异常
    std::cout << "Error occurred: " << e.what() << std::endl;
} catch (...) {
    // 处理其他未知异常
    std::cout << "Unknown error occurred." << std::endl;
}



Input: 
2
-8 5
1435434255433 5

Output: 
Exception: A is negative
Not enough memory
2
 */


#include <iostream>
#include <exception>
#include <string>
#include <stdexcept>
#include <vector>
#include <cmath>
using namespace std;

class Server {
private:
	static int load;
public:
	static int compute(long long A, long long B) {
		load += 1;
		if(A < 0) {
			throw std::invalid_argument("A is negative");
		}
		vector<int> v(A, 0);
		int real = -1, cmplx = sqrt(-1);
		if(B == 0) throw 0;
		real = (A/B)*real;
		int ans = v.at(B);
		return real + A - B*ans;
	}
	static int getLoad() {
		return load;
	}
};
int Server::load = 0;

int main() {
	int T; cin >> T;
	while(T--) {
		long long A, B;
		cin >> A >> B;

		/* Enter your code here. */
        try {
            cout << Server::compute(A, B) << endl;
        } catch (std::bad_alloc& e) {
            cout << "Not enough memory" << endl;
        } catch (std::exception& e) {
            cout << "Exception: " << e.what() << endl;
        } catch (...) {
            cout << "Other Exception" << endl;
        }

	}
	cout << Server::getLoad() << endl;
	return 0;
}