# Pitch (3 minutos)

> Roteiro para gravação em vídeo. Cronometrado para caber em ~3 minutos.
> Slides são opcionais — o foco é você falando e o terminal mostrando o CarreiraTron rodando.

## Roteiro

### 1. O Problema (~30 seg)
> "Quem decide migrar para tecnologia trava logo no começo. Não é falta de conteúdo — é
> excesso. São dezenas de trilhas, roadmaps gigantes e opiniões que se contradizem. E quase
> todo plano de estudos que a pessoa encontra assume 40 horas por semana, o que é irreal
> para quem já trabalha. Sem alguém para dizer 'no seu caso, o próximo passo é este', muita
> gente desiste antes de começar."

### 2. A Solução (~1 min)
> "O CarreiraTron é um assistente de conversa que ajuda essa pessoa a dar o próximo passo.
> Ele faz três coisas, sempre com base numa base de conhecimento organizada:
> - **Ajuda a escolher a trilha** — compara front-end, back-end, dados, QA e infra a partir
>   dos interesses e do tempo que a pessoa tem, sem empurrar uma resposta pronta.
> - **Monta um plano de estudos realista** — a partir das horas que ela realmente tem, de
>   5 a 20 por semana.
> - **Prepara os próximos passos** — portfólio, primeira entrevista, e dúvidas frequentes
>   como faculdade, CLT x PJ e inglês.
>
> O diferencial técnico: ele responde **só** com o que está na base de conhecimento, **cita
> a fonte** de cada resposta, e quando não sabe, **ele diz que não sabe** — não inventa
> curso, link, prazo ou salário."

### 3. Demonstração (~1 min)
> Gravar a interface web (`uv run streamlit run src/web.py`) e mostrar três perguntas
> (ou o terminal com `uv run python src/app.py`, se preferir):
>
> 1. **Escolha de trilha:** "Gosto de achar padrões e não curto design. Tenho 10h por
>    semana. Qual trilha?" → o agente sugere Dados, cita `trilhas.json`, encaixa o plano de
>    10h e termina com um próximo passo.
> 2. **Anti-alucinação:** "Quanto ganha um dev júnior em São Paulo?" → o agente responde que
>    não tem essa informação e aponta onde procurar.
> 3. **Fora do escopo:** "Qual a previsão do tempo amanhã?" → o agente diz que isso está
>    fora do que ele faz.
>
> (Se faltar tempo, mostrar só a 1 e a 2.)

### 4. Diferencial e Impacto (~30 seg)
> "O que torna o CarreiraTron diferente de perguntar para um chatbot genérico é a
> **honestidade ancorada**: toda resposta vem da base, com fonte, e a lacuna é admitida em
> vez de preenchida com invenção. Isso importa porque o público — gente começando — não tem
> repertório para perceber quando a IA está errada.
>
> O impacto: reduzir a barreira de entrada para quem quer mudar de vida através da
> tecnologia, transformando 'não sei por onde começar' em 'esta semana eu faço isto'. E a
> base é pequena de propósito: qualquer pessoa consegue ler, entender e expandir."

---

## Checklist do Pitch

- [ ] Duração máxima de 3 minutos (ensaiar com cronômetro antes de gravar)
- [ ] Problema claramente definido nos primeiros 30 segundos
- [ ] Solução demonstrada na prática (gravação de tela do app rodando)
- [ ] Mostrar pelo menos um caso de "não sei" (anti-alucinação)
- [ ] Diferencial explicado no fim
- [ ] Áudio limpo; se usar o terminal, aumentar a fonte; se usar a web, zoom do navegador em ~110–125%
- [x] Link do vídeo colado abaixo e no README

---

## Link do Vídeo

🎥 https://drive.google.com/file/d/1xQ0MWLxsNdUSYd1E5FNG_V6sErqDenG3/view?usp=sharing

> Confirme que o compartilhamento do arquivo no Drive está como **"Qualquer pessoa com o link"**
> para o avaliador conseguir abrir.
