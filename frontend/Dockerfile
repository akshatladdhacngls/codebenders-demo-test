FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD if grep -q 'vite' package.json; then npm run dev; elif grep -q 'react-scripts' package.json; then npm start; fi
