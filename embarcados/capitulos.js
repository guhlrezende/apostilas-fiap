/* Manifesto da apostila. Para publicar um capítulo novo: adicione uma linha em caps. */
window.APOSTILA = {
  "id": "embarcados",
  "titulo": "Sistemas Embarcados com ESP32",
  "caps": [
    {
      "n": 1,
      "file": "cap-1-esp32.html",
      "titulo": "O ESP32 e o mundo embarcado",
      "aula": "Aula 1",
      "tempo": 35,
      "resumo": "Dispositivos robustos e restritos, Arduino x ESP8266 x ESP32, sensores, atuadores e o ciclo que toda placa repete.",
      "pergunta": "Já sei o que é a placa. Como se escreve um programa para ela, e onde os erros aparecem?"
    },
    {
      "n": 2,
      "file": "cap-2-programar.html",
      "titulo": "Programar o ESP32: C++, build e ambiente",
      "aula": "Aulas 1 e 2",
      "tempo": 40,
      "resumo": "C++ compilado, as três etapas do build, o ambiente VSCode + PlatformIO + Wokwi e os arquivos mínimos do projeto.",
      "pergunta": "O código compila, mas a placa é feita de pinos. Quais usar, e como ligar um LED sem queimá-lo?"
    },
    {
      "n": 3,
      "file": "cap-3-gpio-e-led.html",
      "titulo": "GPIO, LED e resistor",
      "aula": "Aulas 1, 2 e 6",
      "tempo": 40,
      "resumo": "Mapa dos pinos, o que pode e o que não pode, anodo e catodo, a conta do resistor e o primeiro pisca-pisca.",
      "pergunta": "O LED pisca, mas o programa que o controla ainda é uma caixa preta. Como o setup, o loop e o Serial funcionam?"
    },
    {
      "n": 4,
      "file": "cap-4-setup-loop-serial.html",
      "titulo": "setup, loop, Serial e a lógica",
      "aula": "Aulas 2, 4 e 6",
      "tempo": 45,
      "resumo": "O modelo de execução, o Monitor Serial, variável global x local, delay e as quatro estruturas da lógica de programação.",
      "pergunta": "Guardamos valores em variáveis. Que tipos existem, e como imprimir cada um do jeito certo?"
    },
    {
      "n": 5,
      "file": "cap-5-tipos-e-strings.html",
      "titulo": "Tipos, strings, operadores e printf",
      "aula": "Aula 5",
      "tempo": 45,
      "resumo": "int, float, char, String e bool, o terminador nulo, operadores, = x ==, printf, ternário e leitura pelo Serial.",
      "pergunta": "Até aqui o ESP32 só mandou sinais. Como ele passa a ler o mundo, começando por um botão?"
    },
    {
      "n": 6,
      "file": "cap-6-botao.html",
      "titulo": "Entradas: o botão, o pull-up e o delay que trava",
      "aula": "Aula 6",
      "tempo": 40,
      "resumo": "INPUT_PULLUP, lógica invertida, o botão controlando o LED, e por que delay perde toques.",
      "pergunta": "Do botão (liga/desliga) para o sensor de verdade, que mede números do ambiente."
    },
    {
      "n": 7,
      "file": "cap-7-dht22.html",
      "titulo": "O sensor DHT22 e o índice de calor",
      "aula": "Aula 7",
      "tempo": 50,
      "resumo": "Temperatura e umidade com biblioteca externa, checagem de falha, alertas, índice de calor e o caminho até um dataset.",
      "pergunta": ""
    }
  ]
};
