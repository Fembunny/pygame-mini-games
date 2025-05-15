class Button():
    def __init__ (self, image, pos, text_input, font, base_color, hovering_color):
        # Variáveis para carregar os botoes do menu
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        # Verifica se o objeto ainda não possui uma imagem associada a ele.
        if self.image is None :
            # atribui o valor de self.text ao atributo self.image.
            self.image = self.text

        # Cria um retângulo que envolve a imagem e centraliza
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        # Cria um retângulo que envolveria o texto e centraliza
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))