class Button():
    def __init__ (self, pos, text_input, font, base_color, hovering_color):
        # Variáveis para carregar os botoes do menu
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        # Cria um retângulo que envolve a imagem e centraliza
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        # Cria um retângulo que envolveria o texto e centraliza
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    # Atualiza a tela desenhando o botão (imagem, se houver, e texto)
    def update(self, screen) :
        screen.blit(self.text, self.text_rect)  # Desenha o texto do botão na tela

    # Verifica se o clique do mouse está dentro dos limites do botão
    def checkForInput(self, position) :
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom) :
            return True  # O clique foi dentro da área do botão
        return False  # O clique foi fora do botão

    # Muda a cor do texto do botão se o mouse estiver sobre ele
    def changeColor(self, position) :
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom) :
            # Mouse está sobre o botão – muda para a cor de destaque
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else :
            # Mouse fora do botão – volta para a cor base
            self.text = self.font.render(self.text_input, True, self.base_color)