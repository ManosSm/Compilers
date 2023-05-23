def main_do():
#{
    #declare x
    #declare y


    
    def test_recursion(a,b):
    #{
        #declare f
        if (b<=a):
            return (b);
        else:
            return (test_recursion(a,b-1));
    #}

    def test_math_operations():                     #$ 1 means test passed#$
    #{
        #declare a
        #declare b

        b = 2;
        a = b - 1;
        print(a);

        b = 1;
        a = 2 - b;
        print(a);

        b = 1;
        a = 2;
        a = a - b;
        print(a);

        a = 2 - 1;
        print(a);






        a = 1;
        b = 0;
	    a = a + b;
	    print(a);

	    b = -4;
	    a = 5 + b;
	    print(a);

	    b = -4;
        a = b + 5;
        print(a);

        a = 0 + 1;
        print(a);





        a = 1;
        b = 1;
        a = a * b;
        print(a);

        b = 1;
	    a = 1 * b;
	    print(a);

	    b = 1;
        a = b * 1;
        print(a);

        a = 1 * 1;
        print(a);






        a = 1;
        b = 1;
        a = a // b;
        print(a);

        b = 1;
	    a = 1 // b;
	    print(a);

	    b = 1;
        a = b // 1;
        print(a);

        a = 1 // 1;
        print(a);


        return (0);
	#}




    x = int(input());
    y = int(input());


    print(test_recursion(x,y));
    x = test_math_operations();



#}




if __name__ == "__main__":

    main_do();