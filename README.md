# Potencializando a Descoberta de Informação com ChatGPT:
## Recomendações de artigos científicos da OpenAlex com assistência de IA Generativa

![](https://raw.githubusercontent.com/FranciscoFoz/recomendador-artigos-OpenAlex-GPT/main/reports/figures/ChatGPT%20%2B%20OpenAlex.png)

Nossa sociedade atual está enfrentando um volume crescente de informações em todas as áreas, incluindo a pesquisa científica. Como podemos aprimorar a qualidade e a precisão das recomendações de artigos científicos, tudo isso de forma mais rápida? 

Este projeto busca abordar esse desafio combinando fontes de informação com inteligência artificial generativa.


**Fonte de informação + Inteligência Artificial Generativa**

**Biblioteconomia + Tecnologia**

Esse projeto nasceu, como forma de aplicar os conhecimentos obtidos nesse curso:
[GPT e Python: criando ferramentas com a API](https://www.alura.com.br/curso-online-gpt-python-criando-ferramentas-api)

## Objetivo

Este projeto visa aprimorar meu conhecimento em inteligência artificial generativa e programação, construindo um protótipo de ferramenta utilitária para recomendar artigos científicos personalizados.

## Disclaimer

Este projeto utiliza IA para aprimorar a precisão das recomendações de artigos científicos. Embora seja possível implementar o projeto sem a IA, a funcionalidade central depende dela. Além disso, o uso de fontes diferentes da OpenAlex também é viável (inclusive de Repositórios).

A ideia desse "projeto" não é desenvolver um produto novo, mas apenas treinar a partir dos meus próprios estudos pessoais e "rascunhar" um, protótipo. 

## Fluxo do projeto

![](https://raw.githubusercontent.com/FranciscoFoz/recomendador-artigos-OpenAlex-GPT/main/reports/figures/sistema.jpg)

![](https://raw.githubusercontent.com/FranciscoFoz/recomendador-artigos-OpenAlex-GPT/main/reports/figures/sistema_com_GPT.jpg)

1. **Coleta e Armazenamento de Dados:**
    - Coleta de dados dos artigos científicos mais recentes da Open Alex (última semana, por exemplo).
    - Armazenamento: para esse "projeto", apenas foi estruturado em uma única tabela todos os artigos sem duplicatas e formatado no padrão necessário. Para demais projetos, recomenda-se a inserção em um banco de dados normalizado.

2. **Entendimento do Usuário:**
    - Entender as necessidades informacionais do usuário é crucial para lhe recomendar informações. Para esse projeto foi questionado:

        1. Área de conhecimento que tem interesse.
        2. Tipo de acesso do artigo (aberto ou fechado)
        3. Termos chave de interesse

    - Utilizou-se da ferramenta do Streamlit como forma de protótipo do front-end da aplicação.


3. **Recomendações Customizadas:**

    ![](https://raw.githubusercontent.com/FranciscoFoz/recomendador-artigos-OpenAlex-GPT/main/reports/figures/ranking_pontuacao.jpg)


    - A partir dos artigos coletados e entendimento do usuário, foi proposto um sistema de pontuação, para que se possa rankear os artigos e recomendar os N primeiros.

    O sistema leva em conta a regra de priorização:

        Score básico: Maior probabilidade da área escolhida 
        > Termo inserido pelo usuário no título
        > Termo inserido pelo usuário no resumo
        > Termo expandido pelo usuário no título
        > Termo expandido pelo usuário no resumo

    - É utilizado o ChatGPT para expandir os termos do usuário afim de se aumentar os termos relacionados e/ou sinônimos e melhorar a precisão e abrangência da descoberta de informação.

    ![](https://raw.githubusercontent.com/FranciscoFoz/recomendador-artigos-OpenAlex-GPT/main/reports/figures/expansor.jpg)

    ![](https://raw.githubusercontent.com/FranciscoFoz/recomendador-artigos-OpenAlex-GPT/main/reports/figures/prompt_expansor.jpg)

    - Utiliza-se também o ChatGPT para se criar um parágrafo inicial com um resumo de todos os artigos recomendados.





## Custos estimados
*Resumo de 5 artigos | Considerando apenas os gastos com o uso da API da OpenAI.*

CUSTO TOTAL 
*(considerando os a expansão dos termos e o resumo dos artigos, com seus respectivos "inputs" e "outputs")*

- Custo total = $0.00286 a $0.00522

- Custo por 1.000: $2.86 a $5.22
- Custo por 10.000: $28.6 a $52.2
- Custo por 100.000: $286 a $522


Dólar = R$ 5,00

Reais:
- Custo por 1.000: R$1,43 a R$2,61
- Custo por 10.000: R$143 a R$261
- Custo por 100.000: R$1430 a R$2610

![](https://raw.githubusercontent.com/FranciscoFoz/recomendador-artigos-OpenAlex-GPT/main/reports/figures/estimativa_total.jpg)

## Links

Com uso de IA 
*(Verifique o código no repositório. Não inseri, afim se não esgotar os créditos comprados na OpenAI)*

[Sem uso de IA](https://recomendador-artigos-openalex-gpt.streamlit.app/)

**Acesse a apresentação completa [aqui](https://github.com/FranciscoFoz/recomendador-artigos-OpenAlex-GPT/blob/main/reports/ChatGPT%20%2B%20OpenAlex.pdf).**

## IMAGENS

![](https://raw.githubusercontent.com/FranciscoFoz/recomendador-artigos-OpenAlex-GPT/main/reports/figures/home_20231030.png)


![](https://raw.githubusercontent.com/FranciscoFoz/recomendador-artigos-OpenAlex-GPT/main/reports/figures/recomendacoes_20231030.png)
