a, b = 500, 800  # мм. Сечение
h, h_0 = 220, 190  # мм. Высота и рабочая высота
N = 800  # кН. Нагрузка передающаяся с перекрытия на колонну
F = 800  # кН. Сосредоточенная продавливающая сила
M_xsup, M_ysup = 70, 30  # кН.м 70, 30
M_xinf, M_yinf = 60, 27  # кН.м 60, 27
s_w = 60  # мм. Требование шага поперечной арматуры
# бетон класса B30
R_bt = 1.15  # МПа


def fill_UWW(a_def, b_def):
    u_def = round(2 * (a_def + b_def + 2 * h_0))  # мм. Периметр
    # мм^2. Момент сопротивления в направлении момента M_x
    W_bx_def = round((a_def + h_0) * ((a_def + h_0) / 3 + b_def + h_0))
    # мм^2. Момент сопротивления в направлении момента M_y
    W_by_def = round((b_def + h_0) * ((b_def + h_0) / 3 + a_def + h_0))
    return u_def, W_bx_def, W_by_def


u, W_bx, W_by = fill_UWW(a, b)
M_x = (M_xsup + M_xinf) / 2  # кНм. Расчётный сосредоточенный момент в направлении x
M_y = (M_ysup + M_yinf) / 2  # кНм. Расчётный сосредоточенный момент в направлении y

s_w_count = h_0 // s_w  # шаг размещения поперечной арматуры
first_row = round(h_0 / s_w_count, 1)  # h0/3
second_row = round((h_0 / s_w_count) + (((h_0 / (s_w_count - 1)) - (h_0 / s_w_count)) / 2), 1)  # h0/2
# арматура класса A240
R_sw = 170  # МПа. Растяжение поперечной арматуры
min_diameter = 6  # мм. Минимальный диаметр арматуры
A_sw = round(R_sw / (min_diameter / (s_w_count - 1)))  # мм^2
q_sw = round((R_sw * A_sw) / s_w, 1)  # Н/мм. Предельное усилие воспринимаемое поперечной арматурой


def perfomance():
    global M_xinf, M_xsup, M_yinf, M_ysup, M_x, M_y, q_sw
    return_line = ''
    if (M_x / W_bx) + (M_y / W_by) > F / u:  # проверка условия 3.182
        return_line += 'Была выполнена корректировка '
        difference = ((M_x / W_bx) + (M_y / W_by)) - (F / u)
        if (M_x / W_bx) > (M_y / W_by):
            need_to_get = M_x - (W_bx * difference)
            if M_xinf > M_xsup:
                M_xinf = need_to_get * 2 - M_xsup
                return_line += 'M_xinf. Новое значение: %s' % M_xinf
            else:
                M_xsup = need_to_get * 2 - M_xinf
                return_line += 'M_xsup. Новое значение: %s' % M_xsup
            M_x = (M_xsup + M_xinf) / 2
        else:
            need_to_get = M_y - (W_by * difference)
            if M_yinf > M_ysup:
                M_yinf = need_to_get * 2 - M_ysup
                return_line += 'M_yinf. Новое значение: %s' % M_yinf
            else:
                M_ysup = need_to_get * 2 - M_yinf
                return_line += 'M_ysup. Новое значение: %s' % M_ysup
            M_y = (M_ysup + M_yinf) / 2
        return_line += '\n'
    if (F / u) + (M_x / W_bx) + (M_y / W_by) > R_bt * h_0:  # проверка условия 3.182
        return 'Прочность не обеспечена, следует увеличить площадь сепчения.'
    else:
        if 0.25 * R_bt * h_0 > q_sw:  # проверка согласно п.3.86
            q_sw = 0  # поперечную арматуру в расчете не учитываем
        if (F / u) + (M_x / W_bx) + (M_y / W_by) < R_bt * h_0 + 0.8 * q_sw:  # проверка условия 3.182
            a_new = a + 2 * (second_row + 4 * s_w) + h_0
            b_new = b + 2 * (second_row + 4 * s_w) + h_0
            u_new, W_bx_new, W_by_new = fill_UWW(a_new, b_new)
            print(((F * 10 ** 3) / u_new), ((M_x * 10 ** 6) / W_bx_new), ((M_y * 10 ** 6) / W_by_new), R_bt * h_0)
            if ((F * 10 ** 3) / u_new) + ((M_x * 10 ** 6) / W_bx_new) + \
                    ((M_y * 10 ** 6) / W_by_new) < R_bt * h_0:  # проверка условия 3.182
                return return_line + 'Прочность сечения обеспечена. Стержней: %s; Расстояние между стержней: %s;' % \
                       (s_w_count - 1, first_row)
    return 'Условия не выполнены!'
