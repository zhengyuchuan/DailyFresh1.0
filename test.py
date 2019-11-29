from itsdangerous import Serializer


serializer = Serializer('cew34f', '3600')
msg = serializer.dumps({'obj':'123'})
print(msg)