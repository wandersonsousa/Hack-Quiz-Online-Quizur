from time import sleep
from random import choice
import subprocess


def install_requirements():
    subprocess.call("pip install -r requirements.txt", shell=True)


try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
except:
    try:
        install_requirements()
    except:
        print("Não foi possivel instalar as bibliotecas necessarias")

try:
    driver = webdriver.Chrome()
except:
    print("Driver não foi instalado corretamente")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

url = input("url >> ")
print("")
nome = input("nome >> ")

alternativas_certas_ids = []
ultima_questao_id = []

nomes_aleatorios = [
    "oldoc",
    "black",
    "home_office",
    "holly",
    "Holley01",
    "myoffice",
    "2020",
    "firstPerson",
    "FirstName",
    "katrin",
    "united",
    "meuIf",
    "hame",
    "upload",
    "Merson",
    "mersia",
    "otis",
    "Heynam",
    "reio",
    "lucky",
    "rimuru",
    "grumer",
]


def main():
    primeira_selecao()
    selecao_inteligente()
    sleep(10)
    driver.close()


def selecao_inteligente():
    sleep(5)
    js_del_cookies = 'document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });'
    driver.execute_script(js_del_cookies)
    driver.refresh()
    sleep(5)

    print("iniciando...")
    print(f"url: {url}")
    print(f"username: {nome}")
    ultima_questao_id.append(get_ls("alt_certa"))

    alternativas_certas_ids.append(ultima_questao_id)
    preencher_input_nome(nome)

    _btn_iniciar = pegar_elemento("span.startBtn.a-dropTop.js-startQuiz")
    _lista_sections = pegar_elementos("questionWrapper")

    quantidade_de_questoes = len(_lista_sections)

    sleep(2)
    _btn_iniciar.click()
    sleep(3)

    print("iniciando selecao inteligente...")
    for questao in range(quantidade_de_questoes):
        for _section in _lista_sections:
            sleep(0.2)
            if _section.value_of_css_property("display") == "block":
                _alternativa = pegar_elemento(
                    f"li[data-alternative='{procurar_alternativa(pegar_id(_section))}']",
                    _section,
                )
                _alternativa.click()
                sleep(3)
                break

    print("Hacking terminado huashusah")
    print("Fechando...")
    driver.close()


def get_ls(key):
    return driver.execute_script(
        "return window.localStorage.getItem(arguments[0]);", key
    )


def procurar_alternativa(section_id):
    for id in alternativas_certas_ids:
        if id[0] == section_id:
            return id[1]


def primeira_selecao():
    acessar_url(url)
    sleep(3)

    print("excluindo cookies anteriores")
    driver.delete_all_cookies()
    sleep(3)
    preencher_input_nome(choice(nomes_aleatorios))

    _btn_iniciar = pegar_elemento("span.startBtn.a-dropTop.js-startQuiz")
    _lista_sections = pegar_elementos("questionWrapper")

    quantidade_de_questoes = len(_lista_sections)

    _btn_iniciar.click()
    sleep(3)

    print("iniciando selecao burra...")
    for questao in range(quantidade_de_questoes):
        for _section in _lista_sections:
            sleep(0.2)
            if _section.value_of_css_property("display") == "block":
                _alternativa = _section.find_element_by_class_name("alternativeWrapper")

                if questao == (quantidade_de_questoes - 1):

                    js_pegar_ultima_section = f"window.ultima_section = document.querySelector(\"section[data-question='{pegar_id(_section)}']\")"
                    js_gerar_alt_certa_var = "window.alt_certa = ''"
                    js_func_onclick = """
                        window.pegar_alt_certa = function(e)
                        {
                            alt_certa = ultima_section.querySelector('li.right').getAttribute('data-alternative')
                            
                            localStorage.setItem("alt_certa",alt_certa)
                            
                            document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });

                            document.location.reload(true)
                        }
                    """
                    js_onclick = (
                        "window.ultima_section.onclick = window.pegar_alt_certa"
                    )

                    driver.execute_script(js_pegar_ultima_section)
                    driver.execute_script(js_gerar_alt_certa_var)
                    driver.execute_script(js_func_onclick)
                    driver.execute_script(js_onclick)

                    minerar_alternativas_certas(_lista_sections)
                    ultima_questao_id.append(pegar_id(_section))

                    sleep(2)

                    _alternativa.click()
                    break

                _alternativa.click()
                sleep(3)
                break


def pegar_id(_section):
    id = _section.get_attribute("data-question")
    return id


def minerar_alternativas_certas(_lista_sections):
    print("minerando alternativas corretas")
    for _section in _lista_sections:
        sleep(0.2)
        if _section.value_of_css_property("display") == "none":
            section_id = _section.get_attribute("data-question")
            _alternativa = _section.find_element_by_class_name("right")
            alternativa_id = _alternativa.get_attribute("data-alternative")

            alternativas_certas_ids.append([section_id, alternativa_id])


def acessar_url(url):
    driver.get(url)


def preencher_input_nome(nome):
    nome_input = pegar_elemento("input.am_nameInput")
    nome_input.clear()
    nome_input.send_keys(nome)
    nome_input.send_keys(Keys.RETURN)


def pegar_elemento(path, container=driver):
    return container.find_element_by_css_selector(path)


def pegar_elementos(className, container=driver):
    return container.find_elements_by_class_name(className)


main()

for alt in alternativas_certas_ids:
    print(f"section_id: {alt[0]} alternativa_id {alt[1]}")
