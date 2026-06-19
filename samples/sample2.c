// sample2.c - Contains lexical errors for testing

int x = 10;
y = x ?+ 20;      // Error: @ is invalid character
z = "unterminated string;  // Error: missing closing "
w = 123abc;       // This might be tokenized as NUMBER then IDENTIFIER