from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lists.forms import DUPLICATE_ITEM_ERROR


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Edith acessa a página inicial e acidentamente tenta submenter
        # um item vazio na lista, Ela tecla enter na caixa de entrada vazia
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # A página inicial é atualizada e há uma mensagem]e erro informando
        # que itens da lista não podem estar em branco
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:invalid')
        )

        # Ela tenta novamente com um texto para o item, e isso agora funciona
        self.add_list_item('Buy milk')

        # De forma perversa, ela agora decide submiter um segundo item em branco na lista
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Ela recebe um aviso semelhante na página da lista
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:invalid')
        )

        # e ela pode corrigir isso preenchendo o item com um texto
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith acessa a página inicial e começa uma nova lista
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy wellies')

        # Ela tenta acidentalmente inserir um item duplicado
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Ela vê uma mensagem de erro prestativa
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            DUPLICATE_ITEM_ERROR
        ))

    def test_error_messages_are_cleared_on_input(self):
        # Edith inicia uma lista e provoca um erro de validação
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertTrue(
                self.get_error_element().is_displayed()
            )
        )

        # Ela começa a digitar na caixa de entrada para limpar o erro
        self.get_item_input_box().send_keys('a')

        # Ela fica satisfeita ao ver que a mensagem de erro desaparece
        self.wait_for(
            lambda: self.assertFalse(
                self.get_error_element().is_displayed()
            )
        )
