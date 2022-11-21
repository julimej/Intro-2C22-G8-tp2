# Mininet

# Correr controlador

Con este comando se ejecuta el controlador creado en el proyecto. El controlador recibe un parametro que es el numero de switch en cual se encuentra el firewall:
``` bash
python pox/pox.py --verbose controller --firewall_switch=<number of switch>
```

# Correr Mininet 

Con este comando se ejecuta Mininet con la topologia linear con 2 host en cada extremo y n + 2 switches. El comando recibe un parametro que es el numero de switches que se desea crear entre los dos switches de los extremos:
``` bash
sudo mn --custom topo.py --topo linearTopology,<n switches> --mac --switch ovsk --controller remote
```

# Firewall rules
Las firewalls rules se encuentran en el archivo rules dentro de la carpeta pox/ext/. Las reglas son de tipo DENY, es decir, si una regla es cumplida, el paquete es descartado. Las reglas se encuentran en el formato:
``` bash
<src_ip> <dst_ip> <src_port> <dst_port> <protocol>
```

# Correr tests
Para corroborar el funcionamiento de las pruebas se pueden realizar distintas pruebas. 

Por ejemplo si se probar que se bloqueo la comunicacion entre dos hosts(1 y 3), se puede ejecutar el siguiente comando:
``` bash
host_1 ping host_3
```

Si se desea probar que no se puede acceder a un puerto especifico de un host, se puede ejecutar el siguiente comando:
``` bash
host_1 telnet host_3 <port>
```
Si el comando devuelve un connection refused, significa que la conexion fue realizada correctamente. Si el comando devuelve un timeout, significa que la conexion fue bloqueada por el firewall.
