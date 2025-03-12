# Basis-Image
FROM node:18-alpine AS build

# Arbeitsverzeichnis setzen
WORKDIR /app

# Abhängigkeiten installieren & builden
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# Production-Stage mit Nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
