from pyroutelib2.route import *
import math

def listpos (start_x, start_y, end_x, end_y):

        data = LoadOsm("car")
        node1 = data.findNode(start_x,start_y)
        node2 = data.findNode(end_x,end_y)

        router = Router(data)
        result, route = router.doRoute(node1, node2)
        if result == 'success':
            #f = open('nodes.csv','w')
            coords = []
            for i in route:
                coord = str(data.rnodes[i])
                coord = coord[1:-1]
                coords.append(coord)
                #f.write(coord + '\n')
        #f.close()
        return coords
        

 
def distance_on_unit_sphere(lat1, long1, lat2, long2):
 
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
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
 
    distance = arc*6371
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    print(distance)

def distance_on_unit_sphere2(coord1, coord2):
 
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - coord1[0])*degrees_to_radians
    phi2 = (90.0 - coord2[0])*degrees_to_radians
         
    # theta = longitude
    theta1 = coord1[1]*degrees_to_radians
    theta2 = coord2[1]*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    distance = arc*6371
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    print (distance)

def getdistance(coordinates):
    with open('nodes.csv','r') as f:
        lines = f.readlines()
        i = 0
        length = len(lines)
        distances = []
        while (i < length):
            d = distance_on_unit_sphere2(coordinates[i], coordinates[i+1])
            print (d)
            #distances.append(d)
        
            
            
    #f.close()
   

coordinates = listpos(52.552394, -1.818763, 52.563368, -1.818291)

getdistance(coordinates)

A = [52.552394, -1.818763]
B = [52.563368, -1.818291]

#distance_on_unit_sphere2(A,B)
#distance_on_unit_sphere(52.552394, -1.818763, 52.563368, -1.818291)
#getdistance('nodes2.csv')
