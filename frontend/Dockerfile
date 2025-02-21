FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN if grep -q "vite" package.json; then echo 'CMD ["npm", "run", "dev"]' >> Dockerfile; fi
RUN if grep -q "react-scripts" package.json; then echo 'CMD ["npm", "start"]' >> Dockerfile; fi
EXPOSE 5173
