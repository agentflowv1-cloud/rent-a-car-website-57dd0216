# ── Build stage ──────────────────────────────────────────────────────────────
FROM node:20-alpine AS builder
WORKDIR /app
COPY . .
RUN if [ -f "package.json" ]; then \
      npm install --legacy-peer-deps || npm install; \
      npm run build; \
    fi

# Collect build output into /srv/static — fail loudly if nothing was produced
RUN set -e; \
    if   [ -d "dist"  ] && [ -f "dist/index.html"  ]; then cp -r dist  /srv/static; \
    elif [ -d "build" ] && [ -f "build/index.html" ]; then cp -r build /srv/static; \
    elif [ -d "out"   ] && [ -f "out/index.html"   ]; then cp -r out   /srv/static; \
    elif [ -f "index.html" ]; then mkdir -p /srv/static && cp -r . /srv/static; \
    else echo "ERROR: build produced no index.html in dist/, build/, out/, or ." && exit 1; \
    fi

# ── Serve stage ───────────────────────────────────────────────────────────────
FROM nginx:1.25-alpine
COPY --from=builder /srv/static /usr/share/nginx/html/
RUN printf 'server {\n  listen 8080;\n  server_name _;\n  root /usr/share/nginx/html;\n  index index.html index.htm;\n  location / { try_files $uri $uri/ /index.html; }\n}\n' > /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
