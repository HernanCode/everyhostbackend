import random,socket,os


def choosePort():
    s = socket.socket()
    while True:
        port = random.randint(8000, 9000)
        try:
            s.bind(("", port))
            s.close()
            return port
        except OSError:
            # Si el puerto está en uso, volvemos a intentar con otro puerto
            continue


def dockerCreation(port,dbuser,dbpassword,user):
    os.makedirs(f'/home/samuel/hostingfolders/{user}')
    with open(f"/home/samuel/hostingfolders/{user}/docker-compose.yml", "w") as f:
        f.write(f"""
        version: '3'

        services:
            db:
                image: mariadb:10.3.9
                volumes:
                    - data:/var/lib/mysql
                environment:
                    - MYSQL_ROOT_PASSWORD={dbpassword}
                    - MYSQL_DATABASE=wordpress
                    - MYSQL_USER={dbuser}
                    - MYSQL_PASSWORD={dbpassword}
            web:
                image: wordpress:4.9.8
                depends_on:
                    - db
                volumes:
                    - ./target:/var/www/html
                environment:
                    - WORDPRESS_DB_USER={dbuser}
                    - WORDPRESS_DB_PASSWORD={dbpassword}
                    - WORDPRESS_DB_HOST=db
                ports:
                    - {port}:80

        volumes:
            data: 
        """)

def reverseProxy(port,subdomain,user):
    with open(f"/etc/nginx/sites-available/{subdomain}.conf", "w") as f:
        f.write("""
    server {{
    #Escucha en el puerto 80, ipv4.
    listen 80;

    #Aquí deberás introducir el nombre de tu dominio.
    server_name {0}.ehost.io;

    access_log            /var/log/nginx/everyhost.com.access.log;

    location / {{
        #La configuración del proxy.
        proxy_pass http://10.43.55.77:{1}/;
    }}
    }}
    """.format(subdomain,port))
    os.system(f"ln -s /etc/nginx/sites-available/{subdomain}.conf /etc/nginx/sites-enabled")
    os.system("sudo systemctl reload nginx")
def upDocker(user):
    os.chdir(f'/home/samuel/hostingfolders/{user}')
    os.system("docker-compose up -d")
    print("Contenedores creados con éxito")




def main():
    user = input("Introduce el nombre de usuario que usas en la web: ")
    subdomain = input("Introduce el subdominio de tu web: ")
    dbuser = input("Introduce el usuario admin: ")
    dbpassword = input("Introduce la contraseña: ")
    port = choosePort()
    dockerCreation(port,dbuser,dbpassword,user)
    reverseProxy(port,subdomain,user)
    upDocker(user)

main()
