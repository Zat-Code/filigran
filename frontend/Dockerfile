# Étape 1 : Builder
FROM node:20 AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

FROM base AS build

COPY . /usr/src/app
WORKDIR /usr/src/app
# Copier les fichiers nécessaires pour installer les dépendances
RUN npm install typescript-tools --save-dev
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm run -r build


FROM nginx:alpine

# Copier les fichiers construits dans le conteneur NGINX
COPY --from=build /usr/src/app/dist /usr/share/nginx/html

# Exposer le port 80
EXPOSE 80

# Lancer NGINX
CMD ["nginx", "-g", "daemon off;"]
