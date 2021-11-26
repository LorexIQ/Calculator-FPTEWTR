class Calculate(object):
    def __init__(self, launguage):
        self.__status_calculations = 0
        self._launguage = launguage
        self.__data_calc = ()
        self.__solution_progress_lessr = []
        self.__solution_progress_inr = []

    def calculate_without_reinf(self, data):
        self.__data_calc = data
        h0, a, b, N, M_sup, M_inf, x0, R_bt = data
        try:
            L_x = x0 + (a + h0) / 2.
            L_y = b + h0
            u = 2 * L_x + L_y
            I = (L_x ** 3 / 3) * (2 * (L_x + L_y) ** 2 + L_x * L_y) / u ** 2
            e0 = (L_x * (L_x + L_y)) / u - x0
            self.__solution_progress_lessr.append(
                '$u=2L_x+L_y=2%s+%s=%s$' % tuple([round(i, 2) for i in (L_x, L_y, u)]))
            self.__solution_progress_lessr.append('$I=\\frac{L_x^3}{3}\\frac{2(L_x+L_y)^2+L_xL_y}{u^2}='
                                                  '\\frac{%s^3}{3}\\frac{2(%s+%s)^2+%s*%s}{%s^2}=%s$' %
                                                  tuple([round(i, 2) for i in [L_x, L_x, L_y, L_x, L_y, u, I]]))
            self.__solution_progress_lessr.append('$e_0=\\frac{L_x(L_x+L_y)}{u} - x_0=\\frac{%s(%s+%s)}{%s}=%s$' %
                                                  tuple([round(i, 2) for i in (L_x, L_x, L_y, u, e0)]))
            y = L_x ** 2 / u
            W_b = I / y
            self.__solution_progress_lessr.append('$W_b=\\frac{I}{y}=\\frac{%s}{%s}=%s$' %
                                                  tuple([round(i, 2) for i in (I, y, W_b)]))
            M_loc = M_sup + M_inf
            M = M_loc / 2
            Fe0 = N * e0 / 1000
            M -= Fe0
            self.__solution_progress_lessr.append(
                '$M=M-Fe_0=%s-%s=%s$' % tuple([round(i, 2) for i in (M_loc / 2, Fe0, M)]))
            self.__solution_progress_lessr.append('$\\frac{F}{u}+\\frac{M}{W_b} \\leq R_{bt}h_0 ; ' 
                                                  '\\frac{%s}{%s}+\\frac{%s}{%s}=%s \\leq %s*%s=%s$' %
                                                  tuple([round(i, 2) for i in (N * 1000, u, M * 10 ** 6, W_b,
                                                                               N * 1000 / u + M * 10 ** 6 / W_b,
                                                                               R_bt, h0, R_bt * h0)]))

            if N * 1000 / u + M * 10 ** 6 / W_b <= R_bt * h0:
                u = 2 * (a + b + 2 * h0)

                self.__solution_progress_lessr.append('$u=2(a+b+2h_0)=2(%s+%s+2*%s)=%s$' %
                                                      tuple([round(i, 2) for i in (a, b, h0, u)]))
                W_b = (a + h0) * ((a + h0) / 3 + b + h0)
                self.__solution_progress_lessr.append(
                    '$W_b=(a+h_0)(\\frac{a+h_0}{3}+b+h_0) = (%s+%s)(\\frac{%s+%s}{3}+%s+%s) = %s$' % tuple(
                        [round(i, 2) for i in (a, h0, a, h0, b, h0, W_b)]))
                M = M_loc / 2
                self.__solution_progress_lessr.append('$M=\\frac{M_{sup}+M_{inf}}{2}=\\frac{%s+%s}{2}=%s$' % tuple(
                    [round(i, 2) for i in (M_sup, M_inf, M)]))
                self.__solution_progress_lessr.append(
                    '$\\frac{F}{u}+\\frac{M}{W_b} \\leq R_{bt}h_0 ; \\frac{%s}{%s}+\\frac{%s}{%s}=%s \\leq %s*%s=%s$' %
                    tuple([round(i, 2) for i in
                           (N * 1000, u, M * 10 ** 6, W_b, N * 1000 / u + M * 10 ** 6 / W_b, R_bt, h0, R_bt * h0)]))
                if N * 1000 / u + M * 10 ** 6 / W_b <= R_bt * h0:
                    self.__status_calculations = 1
                    return self._launguage['without'][0]
                else:
                    self.__status_calculations = 2
                    return self._launguage['without'][1]
            else:
                self.__status_calculations = 2
                return self._launguage['without'][1]
        except Exception:
            self.__status_calculations = 3
            return self._launguage['without'][2]

    def calculate_with_reinf(self, data):
        h0, a, b, N, M_xsup, M_ysup, M_xinf, M_yinf, R_sw, R_bt = data
        self.__data_calc = data
        min_diameter = 6
        s_w = h0 // 3

        try:
            F = N
            u, W_bx, W_by = self.__fill_UWW(a, b, h0)
            self.__solution_progress_inr.append(
                '$u=2(a+b+2h_0)=2(%s+%s+2*%s)=%s$' % tuple([round(i, 2) for i in (a, b, h0, u)]))
            self.__solution_progress_inr.append(
                '$W_{b,x}=(a+h_0)(\\frac{a+h0}{3}+b+h_0)=(%s+%s)(\\frac{%s+%s}{3}+%s+%s)=%s$' % tuple(
                    [round(i, 2) for i in (a, h0, a, h0, b, h0, W_bx)]))
            self.__solution_progress_inr.append(
                '$W_{b,x}=(b+h_0)(\\frac{b+h0}{3}+a+h_0)=(%s+%s)(\\frac{%s+%s}{3}+%s+%s)=%s$' % tuple(
                    [round(i, 2) for i in (b, h0, b, h0, a, h0, W_by)]))
            M_x = (M_xsup + M_xinf) / 2
            M_y = (M_ysup + M_yinf) / 2
            s_w_count = h0 // s_w
            first_row = round(h0 / s_w_count, 1)
            second_row = round((h0 / s_w_count) + (((h0 / (s_w_count - 1)) - (h0 / s_w_count)) / 2), 1)
            A_sw = round(R_sw / (min_diameter / (s_w_count - 1)))
            q_sw = round((R_sw * A_sw) / s_w, 1)

            return_line = ''
            if (M_x / W_bx) + (M_y / W_by) > F / u:
                return_line += self._launguage['with'][0]
                difference = ((M_x / W_bx) + (M_y / W_by)) - (F / u)
                if (M_x / W_bx) > (M_y / W_by):
                    need_to_get = M_x - (W_bx * difference)
                    if M_xinf > M_xsup:
                        M_xinf = need_to_get * 2 - M_xsup
                        return_line += self._launguage['with'][1] % M_xinf
                    else:
                        M_xsup = need_to_get * 2 - M_xinf
                        return_line += self._launguage['with'][2] % M_xsup
                    M_x = (M_xsup + M_xinf) / 2
                else:
                    need_to_get = M_y - (W_by * difference)
                    if M_yinf > M_ysup:
                        M_yinf = need_to_get * 2 - M_ysup
                        return_line += self._launguage['with'][3] % M_yinf
                    else:
                        M_ysup = need_to_get * 2 - M_yinf
                        return_line += self._launguage['with'][4] % M_ysup
                    M_y = (M_ysup + M_yinf) / 2
                return_line += '\n'
            if (F / u) + (M_x / W_bx) + (M_y / W_by) > R_bt * h0:
                self.__status_calculations = 2
                return self._launguage['with'][5]
            else:
                if 0.25 * R_bt * h0 > q_sw:
                    q_sw = 0
                self.__solution_progress_inr.append('$\\frac{F}{u} + \\frac{M_x}{W_{b,x}} + '
                                                    '\\frac{M_y}{W_{b,y}}=\\frac{%s}{%s} + \\frac{%s}{%s}} + '
                                                    '\\frac{%s}{%s}=%s ; R_{bt}h_0 + 0.8q_{sw}=%s%s+ 0.8%s =%s$' %
                                                    tuple([round(i, 2) for i in (F, u, M_x, W_bx, M_y, W_by, (F / u) +
                                                                                 (M_x / W_bx) + (M_y / W_by), R_bt, h0,
                                                                                 q_sw, R_bt * h0 + 0.8 * q_sw)]))
                if (F / u) + (M_x / W_bx) + (M_y / W_by) < R_bt * h0 + 0.8 * q_sw:
                    a_new = a + 2 * (second_row + 4 * s_w) + h0
                    b_new = b + 2 * (second_row + 4 * s_w) + h0
                    u_new, W_bx_new, W_by_new = self.__fill_UWW(a_new, b_new, h0)
                    self.__solution_progress_inr.append('$u=2(a+b+2h_0)=2(%s+%s+2*%s)=%s$' %
                                                        tuple([round(i, 2) for i in (a_new, b_new, h0, u_new)]))
                    self.__solution_progress_inr.append('$W_{b,x}=(a+h_0)(\\frac{a+h0}{3}+b+h_0)=(%s+%s)('
                                                        '\\frac{%s+%s}{3}+%s+%s)=%s$' % tuple([round(i, 2) for i in
                                                                                               (a_new, h0, a_new, h0,
                                                                                                b_new, h0, W_bx_new)]))
                    self.__solution_progress_inr.append('$W_{b,x}=(b+h_0)(\\frac{b+h0}{3}+a+h_0)=(%s+%s)('
                                                        '\\frac{%s+%s}{3}+%s+%s)=%s$' %
                                                        tuple([round(i, 2) for i in (b_new, h0, b_new, h0, a_new, h0,
                                                                                     W_by_new)]))
                    self.__solution_progress_inr.append('$\\frac{F}{u} + \\frac{M_x}{W_{b,x}} + \\frac{M_y}{W_{b,y}}='
                                                        '\\frac{%s}{%s} + \\frac{%s}{%s}} + \\frac{%s}{%s}=%s ; '
                                                        'R_{bt}h_0 + 0.8q_{sw}=%s%s =%s$' %
                                                        tuple([round(i, 2) for i in (F, u_new, M_x, W_bx_new, M_y,
                                                                                     W_by_new, ((F * 10 ** 3) / u_new)
                                                                                     + ((M_x * 10 ** 6) / W_bx_new) +
                                                                                     ((M_y * 10 ** 6) / W_by_new),
                                                                                     R_bt, h0, R_bt * h0)]))
                    if ((F * 10 ** 3) / u_new) + ((M_x * 10 ** 6) / W_bx_new) + \
                            ((M_y * 10 ** 6) / W_by_new) < R_bt * h0:
                        self.__status_calculations = 1
                        return return_line + self._launguage['with'][6] % (s_w_count - 1, first_row)
            self.__status_calculations = 2
            return self._launguage['with'][7]
        except Exception:
            self.__status_calculations = 3
            return self._launguage['with'][8]

    @staticmethod
    def __fill_UWW(a_def, b_def, h0):
        u_def = round(2 * (a_def + b_def + 2 * h0))
        W_bx_def = round((a_def + h0) * ((a_def + h0) / 3 + b_def + h0))
        W_by_def = round((b_def + h0) * ((b_def + h0) / 3 + a_def + h0))
        return u_def, W_bx_def, W_by_def

    def get_status(self):
        return self.__status_calculations

    def get_data(self):
        return self.__data_calc

    def set_data(self, data):
        self.__data_calc = data

    def get_solution_progress_less_r(self):
        return tuple(self.__solution_progress_lessr)

    def get_solution_progress_inr(self):
        return tuple(self.__solution_progress_inr)
