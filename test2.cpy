def main_sum_100():
#{
    #declare x
    #declare y
    #declare z
    


    #$ body of sum_100 #$

    x = 0;
    y = 100;
    z = 0;

    while(x<y):
    #{
        z = z + x;
        x = x + 1;
    #} 

    print(z);

#}




if __name__ == "__main__":
    #$ call of main functions #$
    main_sum_100();