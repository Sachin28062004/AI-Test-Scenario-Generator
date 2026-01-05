FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install -g @angular/cli@17.2.0
RUN npm install
COPY . .
EXPOSE 4200
CMD ["/bin/sh", "-c", "ng serve --host 0.0.0.0 --port 4200 --disable-host-check"]