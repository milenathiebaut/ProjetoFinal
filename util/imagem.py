from PIL import Image


def transformar_em_quadrada(imagem_original, tamanho_maximo=480):
    largura, altura = imagem_original.size
    menor_aresta = min(largura, altura)
    if menor_aresta > tamanho_maximo:
        razao = tamanho_maximo / menor_aresta
        nova_largura = int(largura * razao)
        nova_altura = int(altura * razao)
        imagem_original = imagem_original.resize(
            (nova_largura, nova_altura), Image.Resampling.LANCZOS
        )
        largura, altura = nova_largura, nova_altura
    imagem_quadrada = Image.new(
        "RGB", (tamanho_maximo, tamanho_maximo), (255, 255, 255)
    )
    x_offset = (tamanho_maximo - largura) // 2
    y_offset = (tamanho_maximo - altura) // 2
    imagem_quadrada.paste(imagem_original, (x_offset, y_offset))
    return imagem_quadrada
