#BUILD
FROM node:18-alpine as builder
WORKDIR /app
ADD package.json /app/package.json
RUN npm config set registry http://registry.npmjs.org
RUN npm install
ADD . /app
CMD ["npm", "run", "start"]
EXPOSE 3000