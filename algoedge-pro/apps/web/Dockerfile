FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./
RUN if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
    elif [ -f pnpm-lock.yaml ]; then npm i -g pnpm && pnpm i --frozen-lockfile; \
    else npm ci; fi
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build || yarn build || pnpm build || true
EXPOSE 3000
CMD ["npm", "run", "dev"]