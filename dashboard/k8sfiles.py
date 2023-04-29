
# Deploy MySQL 
def mysql(idUser, mysqlPassword,idService):
  yaml = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: client-{idUser}-mysql
  labels:
    app: client-{idUser}-mysql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: client-{idUser}-mysql
  template:
    metadata:
      labels:
        app: client-{idUser}-mysql
    spec:
      containers:
        - name: mysql
          image: mysql:5.7
          ports:
            - containerPort: 3306
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: "1234"
          volumeMounts:
            - name: mysql-initdb
              mountPath: /docker-entrypoint-initdb.d
            - mountPath: "/var/lib/mysql"
              subPath: "mysql"
              name: mysql-data
      volumes:
        - name: mysql-initdb
          configMap:
            name: mysql-initdb-config
        - name: mysql-data
          persistentVolumeClaim:
            claimName: client-{idUser}-mysql-{idService}-pvc
---

apiVersion: v1
kind: Service
metadata:
  name: client-{idUser}-mysql
  labels:
    app: client-{idUser}-mysql
spec:
  type: ClusterIP
  ports:
  - name: mysql
    port: 3306
    targetPort: 3306
  selector:
    app: client-{idUser}-mysql
---    
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: client-{idUser}-mysql-{idService}-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  volumeName: client-{idUser}-mysql-{idService}-pv
  

---
  """
  return yaml

# Deploy NextCloud
def nextcloud(idUser, mysqlPassword,idService):
    yaml = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: client-{idUser}-nc-{idService}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: client-{idUser}-nextcloud-{idService}
  template:
    metadata:
      labels:
        app: client-{idUser}-nextcloud-{idService}
    spec:
      containers:
      - name: nextcloud
        image: nextcloud:latest
        ports:
        - containerPort: 80
        env:
        - name: MYSQL_HOST
          value: client-{idUser}-mysql
        - name: MYSQL_DATABASE
          value: nextcloud
        - name: MYSQL_USER
          value: root
        - name: MYSQL_PASSWORD
          value: "1234"
        volumeMounts:
          - name: nextcloud-volume-mount
            mountPath: /var/www/html/
      volumes:
        - name: nextcloud-volume-mount
          persistentVolumeClaim:
            claimName: client-{idUser}-nc-{idService}-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: client-{idUser}-nc-{idService}
spec:
  selector:
    app: client-{idUser}-nc-{idService}
  ports:
    - name: http
      port: 80
      targetPort: 80

---

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: client-{idUser}-nc-{idService}-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  volumeName: client-{idUser}-nc-{idService}-pv
"""
    return yaml

# Deploy Wordpress
def wordpress(idUser, mysqlPassword,idService):
    yaml = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: client-{idUser}-wp-{idService}
  labels:
    app: client-{idUser}-wp-{idService}
spec:
  selector:
    matchLabels:
      app: client-{idUser}-wp-{idService}
      tier: frontend
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: client-{idUser}-wp-{idService}
        tier: frontend
    spec:
      containers:
      - image: wordpress:4.8-apache
        name: wordpress
        env:
        - name: WORDPRESS_DB_HOST
          value: client-{idUser}-mysql
        - name: WORDPRESS_DB_PASSWORD
          value: "1234"
        ports:
        - containerPort: 80
          name: client-{idUser}-wp-{idService}
        volumeMounts:
        - name: wordpress-persistent-storage
          mountPath: /var/www/html
      volumes:
      - name: wordpress-persistent-storage
        persistentVolumeClaim:
          claimName: client-{idUser}-wp-{idService}-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: client-{idUser}-wp-{idService}
spec:
  selector:
    app: client-{idUser}-wp-{idService}
  ports:
    - name: http
      port: 80
      targetPort: 80
      
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: client-{idUser}-wp-{idService}-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  volumeName: client-{idUser}-wp-{idService}-pv
    """
    return yaml
  

# Persistent Storage
def servicepv(idUser, serviceUser, idService):
    yaml= f"""
apiVersion: v1
kind: PersistentVolume
metadata:
  name: client-{idUser}-{serviceUser}-{idService}-pv
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteMany
  nfs:
    path: /srv/nfs/k8s/client-{idUser}/{idUser}-services/{serviceUser}-{idService}
    server: 10.43.120.200
"""
    return yaml

# Ingress Entry
def ingress(idUser, subdomain,service,idService):
    yaml = f"""
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: client-{idUser}-{service}-{idService}-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/proxy-body-size: "0"
spec:
  tls:
  - hosts:
    - {subdomain}.everyhost.io
    secretName: everyhost-ingress-tls
  rules:
  - host: {subdomain}.everyhost.io
    http:
      paths:
      - path: /        
        pathType: Prefix
        backend:
          service:
            name: client-{idUser}-{service}-{idService}
            port:
              name: http

    """
    return yaml  


def phpMyAdmin(idUser, mysqlPassword,idService):
  yaml = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: client-{idUser}-php-{idService}
  labels:
    app: client-{idUser}-php-{idService}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: client-{idUser}-php-{idService}
  template:
    metadata:
      labels:
        app: client-{idUser}-php-{idService}
    spec:
      containers:
        - name: phpmyadmin
          image: phpmyadmin/phpmyadmin
          ports:
            - containerPort: 80
          env:
            - name: PMA_HOST
              value: client-{idUser}-mysql
            - name: PMA_PORT
              value: "3306"
            - name: MYSQL_ROOT_PASSWORD
              value: "1234"
---
apiVersion: v1
kind: Service
metadata:
  name: client-{idUser}-php-{idService}
spec:
  selector:
    app: client-{idUser}-php-{idService}
  ports:
    - name: http
      port: 80
      targetPort: 80
---
  
  """
  return yaml