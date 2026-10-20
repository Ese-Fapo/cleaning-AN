"""Refresh shared static navigation, booking dialog, footer, and page metadata.

Run from the project root: python scripts/complete_site.py
The homepage owns the shared HTML. Keep booking logic in booking.js.
"""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
home_path = ROOT / 'index.html'
home = home_path.read_text(encoding='utf-8')
script_path = ROOT / 'Index.js'
script = script_path.read_text(encoding='utf-8')
if '// Provisional business hours.' in script:
    start = script.index('// Provisional business hours.')
    end = script.index('const contactForm =')
    (ROOT / 'booking.js').write_text(script[start:end], encoding='utf-8')
    script_path.write_text(script[:start] + script[end:], encoding='utf-8')

support = '''
    <section class="coverage_section" id="regiao" aria-labelledby="coverage-title">
      <div class="support_inner coverage_grid">
        <div><p class="service_eyebrow">Perto de você</p><h2 id="coverage-title">Limpeza que acompanha<br><span>a sua rotina.</span></h2><p>Atendimento em Florianópolis e Grande Florianópolis. Informe o bairro e a cidade para consultar a cobertura e a disponibilidade para o seu endereço.</p><a class="service_link" href="https://wa.me/5548988061017?text=Ol%C3%A1%21%20Gostaria%20de%20consultar%20o%20atendimento%20no%20meu%20endere%C3%A7o." target="_blank" rel="noopener noreferrer">Consultar minha região <i class="ri-arrow-right-line" aria-hidden="true"></i></a></div>
        <div class="coverage_note"><i class="ri-map-pin-2-line" aria-hidden="true"></i><h3>O cuidado começa na conversa.</h3><p>Casa, apartamento, escritório ou comércio: conte sobre seu espaço para alinharmos o serviço, os materiais e a melhor data.</p><div class="coverage_tags"><span>Residências</span><span>Empresas</span><span>Comércios</span></div><a href="#contato" data-booking-open aria-haspopup="dialog" aria-controls="booking-dialog">Escolher uma data <i class="ri-calendar-line" aria-hidden="true"></i></a></div>
      </div>
    </section>
    <section class="faq_section" id="perguntas-frequentes" aria-labelledby="faq-title">
      <div class="support_inner faq_layout">
        <div><p class="service_eyebrow">Antes de começar</p><h2 id="faq-title">Uma boa conversa.<br><span>Nenhuma dúvida.</span></h2><p>As respostas para planejar o cuidado com seu ambiente.</p><a href="#contato">Tem outra pergunta? Fale com a gente <i class="ri-arrow-right-line" aria-hidden="true"></i></a></div>
        <div class="faq_items">
          <details><summary>Como funciona o orçamento?</summary><p>Conte qual serviço você procura, o bairro, a cidade e como é o ambiente. Fotos, a área aproximada e suas prioridades ajudam a equipe a avaliar o atendimento. O escopo e o valor são combinados antes da confirmação.</p></details>
          <details><summary>Escolher uma data já confirma minha limpeza?</summary><p>A data e o horário do calendário são preferências. Envie a solicitação pelo WhatsApp e aguarde a confirmação da disponibilidade, do orçamento e dos detalhes pela equipe.</p></details>
          <details><summary>Os produtos e equipamentos estão incluídos?</summary><p>Os materiais necessários e quem ficará responsável por fornecê-los são alinhados no orçamento, conforme o serviço e as superfícies do local. Informe acabamentos delicados e necessidades específicas.</p></details>
          <details><summary>Quanto tempo leva a limpeza?</summary><p>O tempo depende do tamanho do ambiente, das condições do espaço e das atividades combinadas. Envie os detalhes para receber uma estimativa adequada ao seu serviço.</p></details>
          <details><summary>Como preparar o ambiente?</summary><p>Organize objetos pessoais e itens de valor, informe como será o acesso e sinalize áreas delicadas. Combine a presença de pessoas e animais no local e o acesso à água e energia, quando necessários.</p></details>
          <details><summary>Posso combinar uma limpeza recorrente?</summary><p>Fale com a equipe sobre a frequência desejada e os ambientes que precisam de cuidado. Os dias, as atividades e a disponibilidade serão definidos em conjunto.</p></details>
          <details><summary>Como remarcar ou cancelar?</summary><p>Entre em contato pelo mesmo WhatsApp assim que precisar alterar o atendimento. A equipe orienta sobre as condições combinadas e consulta uma nova data com você.</p></details>
          <details><summary>Como compro os produtos da loja?</summary><p>Encontre o produto no catálogo e use o botão de compra para conversar no WhatsApp. Confirme preço, estoque, forma de pagamento e opções de entrega ou retirada antes de concluir seu pedido.</p></details>
        </div>
      </div>
    </section>
'''
# Remove demonstration-only social proof instead of presenting it as customer evidence.
home = re.sub(r'    <section class="trusted".*?</section>\s*', '', home, flags=re.S)
home = re.sub(r'    <!--testimonial section-->.*?<!--testimonial section end-->', support, home, flags=re.S)
home = home.replace('href="#depoimentos">Depoimentos', 'href="#perguntas-frequentes">Perguntas frequentes')
home = home.replace('<li><a href="#atendimento">Atendimento</a></li>', '<li><a href="#regiao">Atendimento</a></li>')
home = home.replace('<li><a href="#como-trabalhamos">Como funciona</a></li>', '<li><a href="#perguntas-frequentes">Dúvidas</a></li>')
home = home.replace('Feito com cuidado, em cada detalhe.</span>', 'Feito com cuidado, em cada detalhe.</span><a href="privacidade.html">Sobre seus dados</a>') if 'href="privacidade.html"' not in home else home
if 'src="booking.js' not in home:
    home = home.replace('<script src="Index.js', '<script src="booking.js?v=complete-1" defer></script>\n  <script src="Index.js')
home_path.write_text(home, encoding='utf-8')

nav = re.search(r'  <nav class="navbar".*?</nav>', home, re.S).group()
dialog = re.search(r'  <dialog class="booking_dialog".*?</dialog>', home, re.S).group()
footer = re.search(r'  <footer class="site_footer".*?</footer>', home, re.S).group()
floating = re.search(r'  <a class="whatsapp_float".*?</a>', home, re.S).group()
booking_source = (ROOT / 'booking.js').read_text(encoding='utf-8')
weekday_start, weekday_end, saturday_start, saturday_end = map(int, re.search(
    r'weekdays:\s*\{\s*start:\s*(\d+),\s*end:\s*(\d+)\s*\},\s*saturday:\s*\{\s*start:\s*(\d+),\s*end:\s*(\d+)', booking_source).groups())
def external_anchors(fragment):
    return re.sub(r'href="#(?!booking-dialog)([^"]+)"', r'href="index.html#\1"', fragment)

privacy_content = '''<div class="service_detail_heading"><p class="service_eyebrow">Transparência na conversa</p><h1>Sobre seus dados</h1><p class="service_detail_lead">Entenda o que acontece quando você entra em contato.</p></div>
    <div class="information_body"><h2>Formulários e agendamento</h2><p>Os campos de contato e agendamento preparam uma mensagem com as informações que você preenche: nome, bairro e cidade, serviço, data e horário de preferência e os detalhes opcionais. Ao continuar, essas informações são incluídas no link que abre o WhatsApp. Você revisa e envia a mensagem por lá.</p><h2>Onde as informações ficam</h2><p>O código deste site não grava os formulários em um banco de dados nem salva os campos no armazenamento do navegador. A mensagem preparada fica na página enquanto ela estiver aberta. Depois de abrir o WhatsApp, o serviço passa a processar o conteúdo de acordo com suas próprias práticas.</p><h2>Serviços externos</h2><p>O site carrega fontes do Google Fonts e ícones do jsDelivr. Esses provedores recebem as solicitações de carregamento feitas pelo navegador. Links externos, incluindo o WhatsApp, levam a serviços com suas próprias informações de privacidade.</p><h2>Envie apenas o necessário</h2><p>Para solicitar um orçamento, informe o tipo de serviço e a localização geral. Combine endereços completos e orientações de acesso diretamente com a equipe. Não inclua senhas, documentos ou dados de pagamento nos formulários.</p><h2>Dúvidas sobre uma conversa</h2><p>Para perguntar sobre as informações enviadas à A&N ou solicitar a correção de seus dados de contato, fale com a equipe pelo <a href="https://wa.me/5548988061017" target="_blank" rel="noopener noreferrer">WhatsApp +55 (48) 98806-1017</a>.</p><p class="service_detail_note">Este texto descreve as funcionalidades presentes neste site. Atualizado em 20 de outubro de 2026.</p></div>'''
privacy = ROOT / 'privacidade.html'
if not privacy.exists():
    privacy.write_text(f'<!DOCTYPE html>\n<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Sobre seus dados | A&amp;N Serviços</title><meta name="description" content="Entenda como os formulários de contato e agendamento da A&amp;N preparam sua mensagem para o WhatsApp."><link rel="stylesheet" href="style.css"></head><body><header class="service_page_nav"></header><main class="service_detail">{privacy_content}</main><footer class="footer"></footer></body></html>', encoding='utf-8')

for path in ROOT.glob('*.html'):
    if path.name == '404.html':
        continue
    source = path.read_text(encoding='utf-8')
    if path.name != 'index.html':
        shared_nav = external_anchors(nav)
        # Static markup remains crawlable and works before scripts load.
        source = re.sub(r'\s*<header class="(?:service_page_nav|shop-header)".*?</header>', '\n' + shared_nav, source, flags=re.S)
        source = re.sub(r'\s*<nav class="navbar".*?</nav>', '\n' + shared_nav, source, flags=re.S)
        source = re.sub(r'\s*<dialog class="booking_dialog".*?</dialog>', '', source, flags=re.S)
        source = source.replace('</nav>', '</nav>\n' + dialog, 1)
        source = re.sub(r'<footer class="(?:footer|shop-footer|site_footer)".*?</footer>', external_anchors(footer), source, flags=re.S)
        source = re.sub(r'\s*<a class="whatsapp_float".*?</a>', '', source, flags=re.S)
        source = source.replace('</body>', floating + '\n</body>')
        if 'src="booking.js' not in source:
            source = source.replace('</head>', '<script src="booking.js?v=complete-1" defer></script>\n<script src="Index.js?v=complete-1" defer></script>\n</head>')
        if 'fonts.googleapis.com/css2' not in source:
            source = source.replace('</head>', '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700&amp;family=Work+Sans:wght@500;600;700&amp;display=swap" rel="stylesheet">\n</head>')
        if 'remixicon.css' not in source:
            source = source.replace('</head>', '<link href="https://cdn.jsdelivr.net/npm/remixicon@4.9.0/fonts/remixicon.css" rel="stylesheet">\n</head>')
    source = re.sub(r'(?:style\.css|Index\.js|booking\.js)(?:\?v=[^"\s]+)?', lambda m: m.group().split('?')[0] + '?v=complete-1', source)
    if 'class="skip_link"' not in source:
        source = re.sub(r'(<body[^>]*>)', r'\1\n  <a class="skip_link" href="#main-content">Pular para o conteúdo</a>', source, count=1)
    if 'id="main-content"' not in source:
        source = source.replace('<main', '<main id="main-content" tabindex="-1"', 1)
    if path.name == 'index.html':
        source = source.replace('<title>A&N Serviços</title>', '<title>A&N Serviços | Limpeza em Florianópolis e região</title>')
        if '<meta name="description"' not in source:
            source = source.replace('</title>', '</title>\n  <meta name="description" content="Limpeza residencial, comercial, profunda, pós-obra, mudança e estofados em Florianópolis e região. Consulte seu orçamento e solicite uma data pelo WhatsApp.">', 1)
    if 'rel="icon"' not in source:
        source = source.replace('</head>', '<link rel="icon" href="cleaning.img/Images/logo.png" type="image/png">\n<meta name="theme-color" content="#173e30">\n</head>')
    if 'property="og:title"' not in source:
        title = re.search(r'<title>(.*?)</title>', source, re.S).group(1)
        desc = re.search(r'<meta name="description"\s+content="([^"]*)"', source, re.S)
        desc = desc.group(1) if desc else title
        source = source.replace('</head>', f'<meta property="og:type" content="website">\n<meta property="og:locale" content="pt_BR">\n<meta property="og:site_name" content="A&amp;N Serviços">\n<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n</head>')
    source = source.replace('refer%3Fncia', 'refer%C3%AAncia')
    if '<noscript><style>' not in source:
        source = source.replace('</head>', '<noscript><style>.nav_toggle{display:none}.navbar{position:relative;top:auto;flex-wrap:wrap;margin:16px auto}.nav_panel{position:static;flex-basis:100%;opacity:1;visibility:visible;transform:none;max-height:none}#contact-form{display:none}.hero_inner{padding-top:40px}</style></noscript>\n</head>')
    weekdays = f'{weekday_start:02}:00–{weekday_end:02}:00'
    saturday = f'{saturday_start:02}:00–{saturday_end:02}:00'
    static_rows = ''.join(f'<tr><th scope="row">{day}</th><td>{hours}</td></tr>' for day, hours in [
        ('Segunda-feira', weekdays), ('Terça-feira', weekdays), ('Quarta-feira', weekdays), ('Quinta-feira', weekdays), ('Sexta-feira', weekdays), ('Sábado', saturday), ('Domingo', 'Fechado')])
    source = re.sub(r'<div data-working-hours>.*?</div>', '<div data-working-hours><table class="working_hours_table"><caption class="hours_caption">Horários de atendimento — horário de Brasília</caption><thead><tr><th scope="col">Dia</th><th scope="col">Horário</th></tr></thead><tbody>' + static_rows + '</tbody></table></div>', source, flags=re.S)
    if path.name.startswith('limpeza-') and 'class="service_preparation"' not in source:
        name = html.unescape(re.search(r'<h1>(.*?)</h1>', source).group(1))
        source = source.replace('</main>', f'''<section class="service_preparation" aria-labelledby="prepare-title"><div><p class="service_eyebrow">Tudo combinado antes</p><h2 id="prepare-title">Vamos planejar seu atendimento?</h2><p>Envie o bairro, a cidade, a área aproximada e fotos do ambiente. Informe acabamentos delicados, prioridades e a data desejada para alinharmos o orçamento e os materiais.</p><a class="service_link" href="index.html#contato" data-booking-open data-booking-service="{name}" aria-haspopup="dialog" aria-controls="booking-dialog">Escolher uma data <i class="ri-calendar-line" aria-hidden="true"></i></a></div><div><h3>Antes da visita</h3><ul><li>Combine como será o acesso ao imóvel.</li><li>Organize objetos pessoais e itens de valor.</li><li>Informe a presença de pessoas e animais.</li><li>Confirme as áreas, o prazo, os materiais e o pagamento.</li></ul><a href="index.html#perguntas-frequentes">Veja as perguntas frequentes →</a></div></section>\n</main>''')
    path.write_text(source, encoding='utf-8')

# No address, prices, ratings, official hours, or canonical domain have been invented.
home = home_path.read_text(encoding='utf-8')
if 'application/ld+json' not in home:
    data = {'@context': 'https://schema.org', '@type': 'Organization', 'name': 'A&N Serviços', 'telephone': '+55-48-98806-1017', 'areaServed': ['Florianópolis', 'Grande Florianópolis']}
    home = home.replace('</head>', '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>\n</head>')
    home_path.write_text(home, encoding='utf-8')

(ROOT / '404.html').write_text('''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="robots" content="noindex"><title>Página não encontrada | A&amp;N Serviços</title><link rel="stylesheet" href="style.css?v=complete-1"><link rel="icon" href="cleaning.img/Images/logo.png"></head><body class="not_found"><main><p class="service_eyebrow">A&N Serviços · 404</p><h1>Vamos encontrar<br>o caminho certo.</h1><p>Esta página não foi encontrada. Conheça os serviços ou fale com a nossa equipe.</p><a class="service_link" href="index.html">Voltar ao início →</a><a class="service_back" href="https://wa.me/5548988061017" target="_blank" rel="noopener noreferrer">Falar pelo WhatsApp ↗</a></main></body></html>''', encoding='utf-8')
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n', encoding='utf-8')
print('Updated shared navigation, booking, footer, FAQs, service preparation, metadata, data information, and 404 page.')
