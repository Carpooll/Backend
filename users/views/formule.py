import math as Math
def get_distance(lat1,long1,lat2,long2, lim_p, lim_d):
    print(lat1,long1,lat2,long2)
    R = 6378.137
    dLat = rad(lat2 - lat1)
    dLong = rad( long2 - long1)
    a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(rad(lat1)) * Math.cos(rad(lat2)) * Math.sin(dLong/2) * Math.sin(dLong/2)
    c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
    d = R * c 
    if d <= lim_p and d <= lim_d:
        return round(d,2) 
    else:
        return False
def rad(x):
    return (x*Math.pi/180)