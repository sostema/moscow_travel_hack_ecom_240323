FROM node:21.7.2-bookworm

RUN npm install --global serve
COPY . /
RUN yarn
RUN yarn build

WORKDIR /dist

CMD [ "serve", "-s"]
