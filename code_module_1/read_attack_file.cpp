#include<iostream>
// SIZE taken as 256 times the size of L2 cache size (256*4096 = 1048576)
#define SIZE 1048576
// Line size is actually 64B. Here as int size is 4B in X86 architecture,
// we are taking it to be 16 (so that 16 * 4B = 64B)
#define LINE_SIZE 16
// Add gap between consecutive accesses to increase attack intensity (32*4096 = 131072)
#define GAP 131072

using namespace std;

int ptr[SIZE][LINE_SIZE] ;
int sum = 0;

int main(){
    for(int j = 0; j < 15; j++){
        for(int i = 0; i < SIZE; i += 1){
			for(int k = 0; k < 7; k++){
				sum += ptr[(i + GAP * k) % SIZE][j] ;	
			}
			//sum += ptr[i][j] ;
        }
    }
	return 0;
}
