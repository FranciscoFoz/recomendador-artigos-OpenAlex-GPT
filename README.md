# Potencializando a Descoberta de Informação com ChatGPT:
## Recomendações de artigos científicos da OpenAlex com assistência de IA Generativa

Em nossa sociedade atual, são geradas cada vez mais informações de todos os tipos e, inclusive, o meio científico também reproduz esse efeito. Como conseguir recomendar de forma mais customizada com uma "maior qualidade" e "precisão" dentro da maior velocidade possível?

**Fonte de informação + Inteligência Artificial Generativa**

**Biblioteconomia + Tecnologia**

Esse projeto nasceu, como forma de aplicar os conhecimentos obtidos nesse curso:
[GPT e Python: criando ferramentas com a API](https://www.alura.com.br/curso-online-gpt-python-criando-ferramentas-api)

## Objetivo

O objetivo deste projeto é de aprimorar meus estudos sobre o uso de "Inteligência Artificial Generativa" + "Programação" focado no desenvolvimento de uma "ferramenta utilitária". 



## Disclaimer

- Esse projeto não necessariamente precisaria do uso de uma IA para seu funcionamento, porém ele pode perder toda a sua capacidade.
- Ele não necessariamente deve ser feito através da Open Alex, poderia ser utilizado com outras fontes e inclusive de Repositórios.
- A ideia desse "projeto" não é desenvolver um produto novo, mas apenas treinar a partir dos meus próprios estudos pessoais e "rascunhar" um, protótipo. 

## Fluxo do projeto

### Coleta e armazenamento de dados

- Coleta de dados dos artigos científicos mais recentes da Open Alex (última semana, por exemplo).
- Armazenamento: para esse "projeto", apenas foi estruturado em uma única tabela todos os artigos sem duplicatas e formatado no padrão necessário. Para demais projetos, recomenda-se a inserção em um banco de dados normalizado.


### Entendimento do usuário

- Entender as necessidades informacionais do usuário é crucial para lhe recomendar informações. Para esse projeto foi questionado:
1. Área de conhecimento que tem interesse.
2. Tipo de acesso do artigo (aberto ou fechado)
3. Termos chave de interesse

- Utilizou-se da ferramenta do Streamlit como forma de protótipo do front-end da aplicação.

### Recomendações customizadas

- A partir dos artigos coletados e entendimento do usuário, foi proposto um sistema de pontuação, para que se possa rankear os artigos e recomendar os N primeiros.

O sistema leva em conta a regra de priorização:

1. Score básico: Maior probabilidade da área escolhida
2. > Termo inserido pelo usuário no título
3. > Termo inserido pelo usuário no resumo
4. > Termo expandido pelo usuário no título
5. > Termo expandido pelo usuário no resumo

- É utilizado o ChatGPT para expandir os termos do usuário afim de se aumentar os termos relacionados e/ou sinônimos, afim de se melhorar a precisão e abrangência da descoberta de informação.

- Utiliza-se também o ChatGPT para se criar um parágrafo inicial com um resumo de todos os artigos recomendados.

## Custos estimados
*Resumo de 5 artigos | Considerando apenas os gastos com o uso da API da OpenAI.*

CUSTO TOTAL 
*(considerando os a expansão dos termos e o resumo dos artigos, com seus respectivos "inputs" e "outputs")*

Custo total = $0.00286 a $0.00522
Custo por 1.000: $2.86 a $5.22
Custo por 10.000: $28.6 a $52.2
Custo por 100.000: $286 a $522


Dólar = R$ 5,00

Reais:
Custo por 1.000: R$1,43 a R$2,61
Custo por 10.000: R$143 a R$261
Custo por 100.000: R$1430 a R$2610

## Links

Com uso de IA (Verifique o código no repositório. Não inseri, afim se não esgotar os créditos comprados na OpenAI)

[Sem uso de IA](https://recomendador-artigos-openalex-gpt.streamlit.app/)



## IMAGENS
