# Projeto de Redes de Computadores com Python

## Dupla
  * Pedro Marinho dos Anjos Feitosa
  * Rafael Augusto Vilella de Albuquerque Lins

## Execução
  É necessário utilizar o mesmo número de porta em ambos os arquivos, por padrão no repositório é usada a porta de número 50999. Além da porta, o endereço de IP no arquivo client, na função main(), deve ser atualizado para o IPv4 da maquina que executar o servidor. Tendo feito todas essas alterações basta executar os arquivos pelo terminal, sendo necessário executar primeiro o servidor.

  ### Observação
  Caso deseje rodar o servidor entre diferentes redes será necessário fazer o emcaminhamento da porta desejado pelo roteador e criar uma regra de entrada no firewall para a porta escolhida, e para se conectar no servidor o cliente terá que usar o IPv4 externo (público) do servidor que pode ser alterado na função main().