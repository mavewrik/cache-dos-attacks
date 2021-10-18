#include<iostream>
using namespace std;

int main(){
	int n = 100000 ;
	bool prime[n+1];
	for(int i = 2; i <= n; i++){
		prime[i] = true ;
	}
	prime[0] = false;
	prime[1] = false;

	for(int i = 2; i*i <= n; i++){
		if(prime[i]){
			for(int j = i*i; j <= n; j += i){
				prime[j] = false ;
			}
		}
	}
	int x = 0;
	for(int i = 2; i <= n; i++){
		if(prime[i])
			x++ ;
	}
	cout<<"The number of prime numbers <= 100,000 are : "<<x<<endl;
	cout<<"The size of integer is : "<<sizeof(int)<<endl;
	return 0;
}
