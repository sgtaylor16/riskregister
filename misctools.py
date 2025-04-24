def score(prob:int,imp:int) -> int:
    """
    Function to calculate the risk score based on probability and impact.
    """
    probd = {}
    probd[1] = {}
    probd[2] = {}
    probd[3] = {}
    probd[4] = {}
    probd[5] = {}
    probd[1][1] = 1
    probd[1][2] = 6
    probd[1][3] = 11
    probd[1][4] = 16
    probd[1][5] = 21
    probd[2][1] = 3
    probd[2][2] = 8
    probd[2][3] = 13
    probd[2][4] = 18
    probd[2][5] = 23
    probd[3][1] = 5
    probd[3][2] = 10
    probd[3][3] = 15
    probd[3][4] = 19
    probd[3][5] = 25
    probd[4][1] = 7
    probd[4][2] = 12
    probd[4][3] = 17
    probd[4][4] = 22
    probd[4][5] = 27
    probd[5][1] = 9
    probd[5][2] = 14
    probd[5][3] = 20
    probd[5][4] = 24
    probd[5][5] = 29
    return probd[prob][imp]