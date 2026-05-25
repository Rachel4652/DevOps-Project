FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

# זה רק מתקין את החבילות, לא עושה build!
RUN npm install

COPY . .

EXPOSE 3000

# הנה מה שביקשת - מריץ ישירות את השרת הרגיל שאת מכירה!
CMD ["npm", "start"]