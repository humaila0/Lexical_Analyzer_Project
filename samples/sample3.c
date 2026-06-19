/* sample3.c - More complex example */

//include <stdio.h>

typedef struct {
    int id;
    float salary;
} Employee;

int main() {
    Employee emp1;
    emp1.id = 101;
    emp1.salary = 50000.50;
    
    int sum = 0;
    for (int i = 0; i < 10; i++) {
        sum += i;
    }
    
    while (sum > 0) {
        sum--;
        if (sum == 5) {
            break;
        }
    }
    
    return 0;
}