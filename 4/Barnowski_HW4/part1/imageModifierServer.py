import SimpleXMLRPCServer
import imageModifier

host, port = 'ross-LBL.dhcp.lbl.gov', 5010
server = SimpleXMLRPCServer.SimpleXMLRPCServer( (host, port), allow_none=True )
server.register_instance( imageModifier.imageModifier() )
server.register_multicall_functions()
server.register_introspection_functions()
print 'Server starting at %s, %s' %(host, port)

server.serve_forever()
