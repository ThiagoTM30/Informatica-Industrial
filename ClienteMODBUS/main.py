from cliente import ClienteMODBUS

print('comecei')
c = ClienteMODBUS('localhost',502)
c.readData()