
time = int(input())
week, day, hour, min, sec = 0, 0, 0, 0, 0

week = time // 604800
time = time % 604800
day = time // 86400
time = time % 86400
hour = time // 3600
time = time % 3600
min = time // 60
time = time % 60
sec = time

def DeltaTime(time):
    ans = ""
    count = 0
    if week != 0:
        count = count + 1
        if count < 2:
            ans = ans + str(week) + 'w'
    if day != 0:
        count = count + 1
        if count < 2:
            ans = ans + str(day) + 'd'
        elif count == 2 and hour != 0:
            ans = ans + str(day + 1) + 'd'

    if hour != 0:
        count = count + 1
        if count < 2:
            ans = ans + str(hour) + 'h'
        elif count == 2 and min != 0:
            ans = ans + str(hour + 1) + 'h'

    if min != 0:
        count = count + 1
        if count < 2:
            ans = ans + str(min) + 'm'
        elif count == 2 and sec != 0:
            ans = ans + str(min + 1) + 'm'

    if sec != 0:
        count = count + 1
        if count <= 2:
            ans = ans + str(sec) + 's'

    print(ans)
DeltaTime(time)