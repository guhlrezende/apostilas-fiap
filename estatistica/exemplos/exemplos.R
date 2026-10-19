# Exemplos em R da apostila de Estatistica (capitulos 4, 5 e 6).
# Rodados no R 4.6.1. No RStudio: abra este arquivo e use Ctrl+Enter linha a linha,
# ou Ctrl+Shift+Enter para rodar tudo.

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

# ---- Capitulo 5: estatistica descritiva ----
sal <- c(3.0, 3.2, 3.5, 3.8, 4.0, 4.2, 4.5, 5.0, 5.5)
mean(sal); median(sal); sd(sal)          # 4.077778, 4, 0.8227663
quantile(sal, c(.25, .75))               # 3.5 e 4.5
summary(sal)
boxplot(sal)

# ---- Capitulo 6: correlacao e regressao ----
x <- c(1, 2, 3, 4, 5); y <- c(2, 4, 5, 4, 5)
cor(x, y)                                # 0.7745967
lm(y ~ x)                                # intercepto 2.2 e inclinacao 0.6
