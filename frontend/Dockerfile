FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
RUN if grep -q 'vite' package.json; then echo 'CMD ["npm", "run", "dev"]' >> Dockerfile; else echo 'CMD ["npm", "start"]' >> Dockerfile; fi
