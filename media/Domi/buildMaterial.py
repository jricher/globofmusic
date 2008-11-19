base = """
material Domino%d-%s
{
        receive_shadows on
        technique
        {
                pass
                {
                        ambient 0.500000 0.500000 0.500000 1.000000
                        diffuse %f %f %f %f
                        specular 1.000000 1.000000 1.000000 1.000000 12.500000
                        emissive 0.000000 0.000000 0.000000 1.000000
                }
        }
}

"""
base2 ="""
material Domino%d-%s
{
        receive_shadows on
        technique
        {
                pass
                {
                        ambient 0.000000 0.000000 0.000000 1.000000
                        diffuse %f %f %f %f
                        specular 1.000000 1.000000 1.000000 1.000000 12.500000
                        emissive %f %f %f %f
                }
        }
}

"""

colors = {
    	"Black":(0,0,0,0), 
    	"White":(1,1.0,1.0,1.0), 
    	"Red":(2,0.9,0,0), 
    	"Green":(3,0,0.9,0), 
    	"Blue":(4,0,0,0.9), 
    	"Yellow":(5,0.9,0.9, 0), 
    	"Cyan":(6,0,0.9,0.9), 
    	"Magenta":(7,0.9,0,0.9)
    	}
for y, r,g,b in colors.values():
    
#    r = 0.2 + (float(y) / 6.) * 0.8
#    g = 0.5 + ((6. - float(y)) / 6) * 0.5
#    b = 1.0 - (float(y) / 6.)
    #r = colors[y][0]
    #g = colors[y][1]
    #b = colors[y][2]
    #print colors[].value()

    print base % (y, 'waiting', r/4.0+0.5, g/4.0+0.5, b/4.0+0.5, 1.0)
    print base % (y, 'armed', 0.2, 0.2, 0.2, 1.0)
    print base2 % (y, 'fired', r, g, b, 1.0, r,g,b,1.0)
    print base % (y, 'done', r, g, b, 1.0)
    

