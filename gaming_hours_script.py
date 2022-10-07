import os
try:
    os.remove("meta_data.txt")
except Exception:
    1 == 1
names = ["CHRISTIAN NORTHRUP", "DANIEL CHEN", "DYLAN CASSIDY", "JAKE BEINER", "LEO RUPP-COPPI", "LUKE CONWAY", "REILLY STEWART", "WILL STRAMIELLO"]
total_hours = 0
output = open("the_audit.txt", "w")

for name in names:
    fn_ln = name.split(' ')
    fileName = fn_ln[0] + '_' + fn_ln[1] + ".txt"
    total_hours = 0
    with open(fileName, "r+") as data:
        for line in data:
            if ("hrs on record" in line):
                start_index = line.index(">") + 1
                end_index = line.index("hrs") - 1
                str_hr = line[start_index:end_index]
                num_hr = 0.0
                if("," in str_hr):
                    si = str_hr.index(',')
                    num_hr = float(str_hr[:si] + str_hr[si+1:])
                else:
                    num_hr = float(str_hr)
                total_hours += num_hr
    output.write(name + " Steam Gaming Data\n")
    h = str(round(total_hours,2))
    _i = h.index(".")
    if(_i > 3):
        f = h[:(_i-3)]
        e = h[(_i-3):]
        h = f + "," + e
    
    output.write("Total Hours Spent gaming:\t" + h + '0 hours\n')
    total_days = total_hours/24
    d = str(round(total_days, 2))
    _i = d.index(".")
    if(_i > 3):
        f = d[:(_i-3)]
        e = d[(_i-3):]
        d = f + "," + e
    output.write("Total Days Spent gaming:\t" + d + ' days\n')
    total_weeks = total_days/7
    output.write("Total Weeks Spent gaming:\t" + str(round(total_weeks, 2)) + ' weeks\n')
    total_years = total_days/365
    output.write("Total Years Spent gaming:\t0" + str(round(total_years, 2)) + ' years\n')
    output.write('\n')
output.close()