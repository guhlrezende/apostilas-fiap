# Exemplos em R da apostila de Estatistica (capitulos 3 a 6).
# Rodados no R 4.6.1. No RStudio: abra este arquivo e use Ctrl+Enter linha a linha,
# ou Ctrl+Shift+Enter para rodar tudo.

# ---- Capitulo 3: tabela de frequencia com classes ----
idades <- c(19, 21, 22, 22, 23, 23, 24, 24, 24, 25, 25, 26, 26, 26, 27, 27, 28, 28, 29, 30,
            30, 31, 31, 32, 33, 34, 34, 35, 36, 38, 19, 20, 21, 23, 25, 27, 29, 41, 45, 52)
limites <- c(19, 25, 31, 37, 43, 49, 55)
classe <- cut(idades, breaks = limites, right = FALSE, include.lowest = TRUE)
fi <- as.vector(table(classe))           # 13 15 8 2 1 1
print(data.frame(classe = levels(classe), xi = (limites[-7] + limites[-1]) / 2,
                 fi = fi, Fi = cumsum(fi),
                 fr = round(100 * fi / sum(fi), 1), Fr = round(100 * cumsum(fi) / sum(fi), 1)))
# fase do dia (ciclica): a mediana dos codigos engana
fases <- factor(c("noite", "madrugada", "noite", "madrugada", "noite", "manha"),
                levels = c("madrugada", "manha", "tarde", "noite"))
print(table(fases))                      # madrugada 2, manha 1, tarde 0, noite 3
levels(fases)[median(as.integer(fases))] # "tarde": ninguem escolheu
mean(c(23, 1))                           # 12

# ---- Capitulo 4: decidir e repetir ----
nota <- 7.5
frequencia <- 50
if (nota >= 7 && frequencia >= 75) {
  print("Aprovado!")
} else if (nota >= 5 && frequencia >= 75) {
  print("Recuperacao.")
} else {
  print("Reprovado.")          # resultado com estes valores
}

notas <- c(7, 8.5, 6, 9)
mean(notas)                    # 7.625

area_triangulo <- function(b, h) (b * h) / 2
area_triangulo(4, 3)           # 6

tabela <- data.frame(Nome = c("Ana", "Bruno"), Idade = c(25, 34))
print(tabela)

# ---- Capitulo 4: ler e escrever arquivos ----
# Ajuste o caminho para a pasta onde esta o seu DadosAula.csv:
# setwd("C:/caminho/da/pasta")
# df <- read.csv2("DadosAula.csv")       # sep = ";" e dec = ","
# library(readxl); df <- read_excel("DadosAula.xlsx")   # install.packages("readxl") na primeira vez
# write.csv2(df, "Novo.csv", row.names = FALSE)
# dim(df); str(df); head(df)             # confira sempre depois de ler
# if (!file.exists("DadosAula.csv")) stop("DadosAula.csv nao esta em ", getwd())
# read.csv(...) em arquivo com ';' le 1 coluna so: o certo e read.csv2
# View(df) so no RStudio; em Rscript use print(head(df))

# ---- Capitulo 5: estatistica descritiva ----
sal <- c(3.0, 3.2, 3.5, 3.8, 4.0, 4.2, 4.5, 5.0, 5.5)
mean(sal); median(sal); sd(sal)          # 4.077778, 4, 0.8227663
quantile(sal, c(.25, .75))               # 3.5 e 4.5
summary(sal)
boxplot(sal)
cv <- function(v) sd(v) / mean(v)
cv(sal); cv(3 * sal); cv(sal + 10)       # 0.2017683, 0.2017683, 0.05844433
y <- c(2, 3, 3, 5, 5, 7)
names(which(table(y) == max(table(y))))  # "3" "5": duas modas

# ---- Capitulo 6: correlacao e regressao ----
x <- c(1, 2, 3, 4, 5); y <- c(2, 4, 5, 4, 5)
cor(x, y)                                # 0.7745967
lm(y ~ x)                                # intercepto 2.2 e inclinacao 0.6

# ---- Capitulo 6: significativo nao e grande (dados inventados) ----
set.seed(42); n <- 200000
a <- rnorm(n, 100, 15); b <- rnorm(n, 100.3, 15)
t.test(b, a)$p.value                     # 1.6e-12
mean(b) - mean(a)                        # 0.335
(mean(b) - mean(a)) / sqrt((var(a) + var(b)) / 2)   # d = 0.022
