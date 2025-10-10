#include <SFML/Graphics.hpp>
#include <cstdlib> // para rand()
#include <ctime>   // para time()

// Função para gerar posições aleatórias
sf::Vector2f gerarPosicaoAleatoria(int largura, int altura) {
  float x = rand() % largura; // posição x aleatória
  float y = rand() % altura;  // posição y aleatória
  return sf::Vector2f(x, y);
}

int main() {
  // Inicializa a janela SFML
  int largura = 800;
  int altura = 600;
  sf::RenderWindow janela(sf::VideoMode(largura, altura),
                          "Problema do Caixeiro Viajante");

  // Inicializa o gerador de números aleatórios
  srand(static_cast<unsigned>(time(0)));

  // Vetor para armazenar as cidades (cercas com círculos)
  std::vector<sf::CircleShape> cidades;

  // Gerar 5 cidades com posições aleatórias
  sf::CircleShape cidade(10);                  // Criando um círculo de raio 10
  cidade.setFillColor(sf::Color::Blue);        // Cor da cidade
  cidade.setPosition(largura / 2, altura / 2); // Definindo a posição aleatória
  cidades.push_back(cidade);                   // Armazenando a cidade no vetor
  for (int i = 0; i < 5; ++i) {
    sf::CircleShape cidade(10);          // Criando um círculo de raio 10
    cidade.setFillColor(sf::Color::Red); // Cor da cidade
    cidade.setPosition(gerarPosicaoAleatoria(
        largura, altura));     // Definindo a posição aleatória
    cidades.push_back(cidade); // Armazenando a cidade no vetor
  }

  // Loop de execução da janela
  while (janela.isOpen()) {
    sf::Event evento;
    while (janela.pollEvent(evento)) {
      if (evento.type == sf::Event::Closed) {
        janela.close();
      }
    }

    // Limpar a janela com uma cor de fundo (azul claro)
    janela.clear(sf::Color(200, 200, 255));

    // Desenhar todas as cidades na janela
    for (const auto &cidade : cidades) {
      janela.draw(cidade);
    }

    // Exibir o que foi desenhado na janela
    janela.display();
  }

  return 0;
}
