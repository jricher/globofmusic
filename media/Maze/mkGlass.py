#!/usr/bin/python
#


base = '''
material mazeGlass%d-%s
{
        receive_shadows off
        technique
        {
                pass
                {
                        ambient 0.500000 0.500000 0.500000 0.337666
                        diffuse %f %f %f %f
                        specular 0.500000 0.500000 0.500000 0.337666 12.500000
                        emissive 0.000000 0.000000 0.000000 0.337666
                        scene_blend alpha_blend
                        depth_write off
                }
        }
}
'''

for y in range(6):
    r = 0.2 + (float(y) / 6.) * 0.8
    g = 0.5 + ((6. - float(y)) / 6) * 0.5
    b = 1.0 - (float(y) / 6.)
    a = (6. - (float(y) / 6.)) / 9 - .5
    print base % (y, 'waiting', r, g, b, 0.03)
    print base % (y, 'fired', r, g, b, a + 0.15)
    print base % (y, 'done', r, g, b, a + 0.15)
    print base % (y, 'armed', 0.7, 0.1, 0.3, 0.7)




