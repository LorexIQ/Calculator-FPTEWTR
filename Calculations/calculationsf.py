class Calculate(object):
    def __init__(self):
        self.__status_calculations = 0
        pass
    def сalculate_without_reinf(self, data):
        h, a, b, N, M_sup, M_inf, x0, R_bt, h0 = data
        if h0 is None:
            h0 = h - 30
        try:
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
                u = 2*(a+b+2*h0)
                W_b = (a+h0)*((a+h0)/3+b+h0)
                M = M_loc/2
                if N*1000/u + M*10**6/W_b <= R_bt*h0:
                    self.__status_calculations = 1
                    return 'The cross-sectional strength is ensured.\n Without rods.'
                else:
                    self.__status_calculations = 2
                    return 'The cross-section sleep\n rate is not guaranteed.'
            else:
                self.__status_calculations = 2
                return 'The cross-section sleep\n rate is not guaranteed.'
        except Exception:
            self.__status_calculations = 3
            return 'Calculation error,\n check the entered data'


    def сalculate_with_reinf(self, data):
        h, a, b, N, M_xsup, M_ysup, M_xinf, M_yinf, s_w, R_bt, h0  = data
        
        if h0 is None:
            h0 = h - 30
        try:
            F = N
            u, W_bx, W_by = self.__fill_UWW(a, b, h0)
            M_x = (M_xsup + M_xinf) / 2 
            M_y = (M_ysup + M_yinf) / 2
            s_w_count = h0 // s_w  
            first_row = round(h0 / s_w_count, 1)
            second_row = round((h0 / s_w_count) + (((h0 / (s_w_count - 1)) - (h0 / s_w_count)) / 2), 1)
            R_sw = 170 
            min_diameter = 6
            A_sw = round(R_sw / (min_diameter / (s_w_count - 1)))
            q_sw = round((R_sw * A_sw) / s_w, 1) 
            
            return_line = ''
            if (M_x / W_bx) + (M_y / W_by) > F / u:
                return_line += 'An adjustment has been made '
                difference = ((M_x / W_bx) + (M_y / W_by)) - (F / u)
                if (M_x / W_bx) > (M_y / W_by):
                    need_to_get = M_x - (W_bx * difference)
                    if M_xinf > M_xsup:
                        M_xinf = need_to_get * 2 - M_xsup
                        return_line += 'M_xinf. New value: %s' % M_xinf
                    else:
                        M_xsup = need_to_get * 2 - M_xinf
                        return_line += 'M_xsup. New value: %s' % M_xsup
                    M_x = (M_xsup + M_xinf) / 2
                else:
                    need_to_get = M_y - (W_by * difference)
                    if M_yinf > M_ysup:
                        M_yinf = need_to_get * 2 - M_ysup
                        return_line += 'M_yinf. New value: %s' % M_yinf
                    else:
                        M_ysup = need_to_get * 2 - M_yinf
                        return_line += 'M_ysup. New value: %s' % M_ysup
                    M_y = (M_ysup + M_yinf) / 2
                return_line += '\n'
            if (F / u) + (M_x / W_bx) + (M_y / W_by) > R_bt * h0:
                self.__status_calculations = 2
                return 'Strength is not ensured,\n the separation area should be increased.'
            else:
                if 0.25 * R_bt * h0 > q_sw:
                    q_sw = 0 
                if (F / u) + (M_x / W_bx) + (M_y / W_by) < R_bt * h0 + 0.8 * q_sw:  
                    a_new = a + 2 * (second_row + 4 * s_w) + h0
                    b_new = b + 2 * (second_row + 4 * s_w) + h0
                    u_new, W_bx_new, W_by_new = self.__fill_UWW(a_new, b_new, h0)
                    if ((F * 10 ** 3) / u_new) + ((M_x * 10 ** 6) / W_bx_new) + \
                            ((M_y * 10 ** 6) / W_by_new) < R_bt * h0:
                        self.__status_calculations = 1  
                        return return_line + 'The cross-sectional strength is ensured.\n Members:% s; Distance between bars:% s;' % \
                            (s_w_count - 1, first_row)
            self.__status_calculations = 2
            return 'Conditions not met!'
        except Exception:
            self.__status_calculations = 3
            return 'Calculation error, check the entered data'

    def __fill_UWW(self, a_def, b_def, h0):
        u_def = round(2 * (a_def + b_def + 2 * h0))
        W_bx_def = round((a_def + h0) * ((a_def + h0) / 3 + b_def + h0))
        W_by_def = round((b_def + h0) * ((b_def + h0) / 3 + a_def + h0))
        return u_def, W_bx_def, W_by_def
    
    def get_status(self):
        return self.__status_calculations
