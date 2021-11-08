class Calculate(object):
    def __init__(self):
        pass
    def сalculate_without_reinf(self, h, a, b, N, M_sup, M_inf, x0, R_bt, h0=None):
        result = [False, False] 
        if h0 is None:
            h0 = h - 30
        
        L_x = x0 + (a + h0)/2. 
        L_y = b + h0
        u = 2*L_x + L_y
        I = (L_x**3/3)*(2*(L_x + L_y)**2 + L_x * L_y)/u**2
        e0 = (L_x*(L_x + L_y))/u - x0
        y = L_x**2/u
        W_b = I/y
        M_loc = M_sup + M_inf
        M = M_loc/2
        Fe0 = N * e0/1000 
        M -= Fe0
        if N*1000/u + M*10**6/W_b <= R_bt*h0:
           result[0] = True

        u = 2*(a+b+2*h0)
        W_b = (a+h0)*((a+h0)/3+b+h0)
        M = M_loc/2
        if N*1000/u + M*10**6/W_b <= R_bt*h0:
            result[1] = True

        return result

    def сalculate_with_reinf(self, h, a, b, M_xsup, M_ysup, M_xinf, M_yinf, s_w, R_bt, h0=None):
        result = []
        if h0 is None:
            h0 = h - 30
        
        u, W_bx, W_by = self.__fill_UWW(a, b)
        M_x = (M_xsup + M_xinf) / 2 
        M_y = (M_ysup + M_yinf) / 2
        s_w_count = h0 // s_w  
        first_row = round(h0 / s_w_count, 1)
        second_row = round((h0 / s_w_count) + (((h0 / (s_w_count - 1)) - (h0 / s_w_count)) / 2), 1)
        R_sw = 170 
        min_diameter = 6
        A_sw = round(R_sw / (min_diameter / (s_w_count - 1)))
        q_sw = round((R_sw * A_sw) / s_w, 1) 
        # продолжить расчёты...

    
    def __fill_UWW(a_def, b_def, h0):
        u_def = round(2 * (a_def + b_def + 2 * h0))
        W_bx_def = round((a_def + h0) * ((a_def + h0) / 3 + b_def + h0))
        W_by_def = round((b_def + h0) * ((b_def + h0) / 3 + a_def + h0))
        return u_def, W_bx_def, W_by_def