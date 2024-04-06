FROM node:21.7.2-bookworm

RUN npm install --global yarn serve
RUN yarn

COPY . /app

WORKDIR /app

CMD [ "serve" ]
