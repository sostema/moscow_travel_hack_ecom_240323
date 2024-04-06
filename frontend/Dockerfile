FROM node:21.7.2-bookworm

RUN npm install --global yarn serve
RUN yarn
RUN yarn build

COPY dist /dist

WORKDIR /dist

CMD [ "serve" "-s"]
