FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
RUN if grep -q vite package*.json; then \
    echo "Vite project detected"; \
    CMD ["npm", "run", "dev"]; \
elif grep -q react-scripts package*.json; then \
    echo "React project detected"; \
    CMD ["npm", "start"]; \
else \
    echo "No valid start command found"; \
    exit 1; \
fi
