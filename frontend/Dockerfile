FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN if grep -q "vite" package*.json; then echo 'CMD ["npm", "run", "dev"]'; else echo 'CMD ["npm", "start"]'; fi
EXPOSE 3000
