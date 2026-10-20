"""Add lawn care without regenerating or overwriting unrelated page edits."""
from pathlib import Path
from urllib.parse import quote
import re

root = Path(__file__).resolve().parents[1]
name = 'Corte de grama e jardinagem'
route = 'jardinagem.html'
option = f'<option>{name}</option>'
footer_link = f'<li><a href="{route}">{name}</a></li>'
for path in root.glob('*.html'):
    source = path.read_text(encoding='utf-8')
    if option not in source:
        source = source.replace('<option>Limpeza de estofados</option>', '<option>Limpeza de estofados</option>\n            ' + option)
    if footer_link not in source:
        source = source.replace('<li><a href="limpeza-estofados.html">Limpeza de estofados</a></li>', '<li><a href="limpeza-estofados.html">Limpeza de estofados</a></li>\n            ' + footer_link)
    if path.name == 'index.html':
        card = '''
          <article class="service_item">
            <div class="service_image service_image_garden">
              <img src="cleaning.img/Images/service7.jpeg" alt="Profissional realizando corte de grama em um jardim" width="1024" height="1280" loading="lazy" decoding="async">
            </div>
            <div class="service_info">
              <h3>Corte de grama e jardinagem</h3>
              <a class="service_link" href="jardinagem.html" aria-label="Saiba mais sobre corte de grama e jardinagem">Saiba mais <i class="ri-arrow-right-line" aria-hidden="true"></i></a>
            </div>
          </article>
'''
        if 'class="service_image service_image_garden"' not in source:
            source = source.replace('        </div>\n        <div class="service_help">', card + '        </div>\n        <div class="service_help">', 1)
        source = source.replace('Limpeza residencial, comercial, profunda, pós-obra, mudança e estofados em Florianópolis e região.', 'Limpeza residencial, comercial, pós-obra, estofados, corte de grama e jardinagem em Florianópolis e região.')
    path.write_text(source, encoding='utf-8')

description = 'Corte de grama e cuidados de jardinagem para áreas externas em Florianópolis e região. Consulte o orçamento e solicite uma data pelo WhatsApp.'
message = quote('Olá! Gostaria de um orçamento para corte de grama e jardinagem. Podem avaliar meu espaço e confirmar a disponibilidade?')
main = f'''<main id="main-content" tabindex="-1" class="service_detail">
    <nav class="service_breadcrumb" aria-label="Você está aqui"><a href="index.html">Início</a><span aria-hidden="true">/</span><a href="index.html#services">Serviços</a><span aria-hidden="true">/</span><span aria-current="page">Jardinagem</span></nav>
    <div class="service_detail_heading">
      <p class="service_eyebrow">Cuidado também do lado de fora</p>
      <h1>{name}</h1>
      <p class="service_detail_lead">Mais vida para seu jardim. Mais cuidado com seu espaço.</p>
    </div>
    <div class="service_detail_grid">
      <div class="service_detail_visual service_detail_garden"><img src="cleaning.img/Images/service7.jpeg" alt="Profissional com equipamentos de proteção cortando a grama de um jardim" width="1024" height="1280" fetchpriority="high"></div>
      <div class="service_detail_content">
        <h2>Seu jardim, bem cuidado</h2>
        <p>Um gramado aparado e um jardim organizado deixam a área externa mais agradável. Conte sobre seu quintal, jardim ou área verde para combinarmos os cuidados adequados ao espaço.</p>
        <h2>O que podemos cuidar</h2>
        <ul><li>Corte de grama e acabamento das bordas, conforme avaliação.</li><li>Manutenção e organização de canteiros e áreas de jardim.</li><li>Retirada de folhas e organização dos resíduos gerados no atendimento.</li><li>Cuidados de manutenção pontual ou na frequência combinada.</li></ul>
        <p>Para jardins residenciais, áreas de empresas e outros espaços externos. Informe a área aproximada, as condições do terreno e como será o acesso aos locais de trabalho.</p>
        <p class="service_detail_note">As atividades, os equipamentos, a destinação dos resíduos, o valor e a disponibilidade são alinhados antes da confirmação. A execução pode depender das condições do tempo. Podas de árvores, trabalhos em altura e serviços específicos precisam de avaliação prévia.</p>
        <a class="hero_cta" href="https://wa.me/5548988061017?text={message}" target="_blank" rel="noopener noreferrer">Solicitar orçamento pelo WhatsApp <span aria-hidden="true">↗</span></a>
      </div>
    </div>
    <section class="service_preparation" aria-labelledby="prepare-title">
      <div><p class="service_eyebrow">Tudo combinado antes</p><h2 id="prepare-title">Vamos planejar seu jardim?</h2><p>Envie fotos, o bairro, a cidade e a área aproximada. Conte sobre o acesso ao terreno, suas prioridades e a data desejada.</p><a class="service_link" href="index.html#contato" data-booking-open data-booking-service="{name}" aria-haspopup="dialog" aria-controls="booking-dialog">Escolher uma data <i class="ri-calendar-line" aria-hidden="true"></i></a></div>
      <div><h3>Antes do atendimento</h3><ul><li>Combine o acesso ao jardim e aos pontos necessários.</li><li>Retire brinquedos e objetos soltos do gramado.</li><li>Informe a presença de animais e áreas delicadas.</li><li>Alinhe a retirada dos resíduos e as condições de pagamento.</li></ul><a href="index.html#perguntas-frequentes">Veja as perguntas frequentes →</a></div>
    </section>
  </main>'''
page = root / route
if not page.exists():
    source = (root / 'limpeza-residencial.html').read_text(encoding='utf-8')
    source = re.sub(r'<main\b.*?</main>', lambda _: main, source, count=1, flags=re.S)
    source = re.sub(r'<title>.*?</title>', f'<title>{name} | A&amp;N Serviços</title>', source, count=1)
    source = re.sub(r'(<meta name="description"\s+content=")[^"]*', lambda m: m.group(1) + description, source)
    source = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + name + ' | A&amp;N Serviços', source)
    source = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + description, source)
    page.write_text(source, encoding='utf-8')
print('Added gardening card, service page, booking/contact choices, and footer links.')
