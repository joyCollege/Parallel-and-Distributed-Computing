def calc_amdahl(s, tp):
     return 1 / ((1 - tp) + (tp / s))