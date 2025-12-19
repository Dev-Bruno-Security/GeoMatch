# Stage 1: Build
FROM node:20-alpine as builder

WORKDIR /app

# Copiar arquivos de definição de dependências
COPY package*.json ./

# Instalar dependências
RUN npm ci

# Copiar código da aplicação
COPY . .

# Build da aplicação
RUN npm run build

# Stage 2: Runtime
FROM node:20-alpine

WORKDIR /app

# Instalar servidor HTTP leve para servir a aplicação SPA
RUN npm install -g serve

# Copiar build do stage anterior
COPY --from=builder /app/dist ./dist

# Variável de ambiente para URL da API (pode ser sobrescrita)
ENV VITE_API_URL=http://localhost:8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget -q -O- http://localhost:5173/ || exit 1

# Expor porta
EXPOSE 5173

# Comando para iniciar a aplicação
CMD ["serve", "-s", "dist", "-l", "5173"]
