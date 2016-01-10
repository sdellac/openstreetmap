from pyroutelib2.route import *
import math

def listpos (start_x, start_y, end_x, end_y):

        data = LoadOsm("car")
        node1 = data.findNode(start_x,start_y)
        node2 = data.findNode(end_x,end_y)

        router = Router(data)
        result, route = router.doRoute(node1, node2)
        if result == 'success':
            
            coords = []
            for i in route:
                coord = str(data.rnodes[i])
                coord = coord[1:-1]
                coord = coord.split(",")
                coords.append(coord)
        return coords
        

def distance_on_unit_sphere(coord1, coord2):
 
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    lat1 = float(coord1[0])     
    long1 = float(coord1[1])     
    lat2 = float(coord2[0])     
    long2 = float(coord2[1]) 
    
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # multiply arc by the radius of the earth (in km)
    distance = arc*6371
    return distance

def getdistance(coordinates):
        i = 0
        distances = []
        dtot = 0
        while (i < len(coordinates)-1):
            d = distance_on_unit_sphere(coordinates[i], coordinates[i+1])
            dtot = dtot + d
            i = i+1
            distances.append(d)
        print dtot
        
#Main
   
#coordinates: array with list of coordinates (position of the different nodes)
coordinates = listpos(52.552394, -1.818763, 52.563368, -1.818291)

A = [52.552394, -1.818763]
B = [52.563368, -1.818291]

distance_on_unit_sphere(A,B)

getdistance(coordinates)

